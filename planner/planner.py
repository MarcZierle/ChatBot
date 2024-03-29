import datetime as dt
import numpy as np
import icalendar

from planner.event import Event
from planner.day import Day

from googledistancematrix.querent_parser import QuerentParser

import globals

class Planner():

    def __init__(self):
        self.__time_begin_day = globals.to_minutes(8, 0)    # 8 A.M.
        self.__time_end_day   = globals.to_minutes(20, 0)   # 8 P.M.
        self.__days = []
        self.__events = []
        self.__unplanned_events = []    # list of events that need to be planned
        self.__home = "Berlin"          # start everday at this location
        self.__max_events = 99          # maximum number of events per day
        self.__round_travel_time = 15   # arrival and departure times will be rounded to the next quarter hours


    def set_home(self, home):
        self.__home = home


    def set_planning_times(self, start_time, end_time):
        self.__time_begin_day = start_time
        self.__time_end_day = end_time


    def set_max_events(self, max):
        self.__max_events = max


    def add_day(self, day, month, year):
        day = Day(day, month, year)
        self.__days.append(day)
        self.__days.sort(key=lambda d: ( d.get_day(), d.get_month(), d.get_year() ) )
        return day


    def add_event(self, event, date=None):
        if event.is_specific():
            if not date:
                raise Exception("Adding a specific event needs a day!")

            day = self.get_day(date[0], date[1], date[2])[0]
            day.remove_unspecific()
            day.add_event(event)

        self.__events.append(event)

    ########################################################################
    #  PLANNING-ALGORITHM -- START                                         #
    ########################################################################
    def replan(self, querent):
        globals.debug("Replaning all events...")
        # remove all previously planned (unspecific) events
        [d.remove_unspecific() for d in self.__days]

        # mark all events as unplanned
        self.__unplanned_events = [e for e in self.__events if not e.is_specific()]
        globals.debug("removed all previously planned events")

        for currDay in self.__get_next_day():
            globals.debug("planning events on day " + str(currDay.get_day())+"/"+str(currDay.get_month())+"/"+str(currDay.get_year()))

            if currDay.num_specific_events() > 0:
                globals.debug("day has at least on specific event")

                first_it = True
                for sp_event in currDay.get_next_specific_event():
                    self.__unplanned_events = self.__insert_events_to_day(
                        querent,
                        self.__unplanned_events,
                        currDay,
                        sp_event,
                        first_it
                    )

                    if first_it:
                        first_it = False
            else:
                globals.debug("day has no specific events")
                # no specific events for current day
                self.__unplanned_events = self.__insert_events_to_day(
                    querent,
                    self.__unplanned_events,
                    currDay,
                    Event(
                        "Home",
                        Event.EventType.SPECIFIC,
                        self.__time_begin_day-10,
                        self.__time_begin_day,
                        place = self.__home
                    ),
                    insert_before=False
                )

            if not self.__unplanned_events:
                break

        globals.debug("finished planning for all events")
        #unplanned_events_str = ["- " + e.get_name() for e in self.__unplanned_events]
        #if not unplanned_events_str:
        #    print("All events could be planned!")
        #else:
        #    print("Still unplanned events:")
        #    for s in unplanned_events_str:
        #        print("    " + s)
        #print("\n")
        globals.debug("Replaning Done!")


    # trys to insert given events after/before given first_event
    # exits after first collision in day or time_end_day/time_start_day has been reached
    # returns all events that could not be planned
    # Note: Distance calculations will be done; max_events will be considered
    def __insert_events_to_day(self, querent, events, day, first_event, insert_before=True):
        last_event = first_event

        globals.debug("evolving from event " + first_event.get_name())
        if insert_before:
            globals.debug("inserting next events before")
        else:
            globals.debug("inserting next events after")

        while events:
            if day.num_events() >= self.__max_events:
                break

            event_places = [e.get_place() for e in events]
            last_place = last_event.get_place()

            globals.debug("starting api query...")
            if insert_before:
                arr_time = last_event.get_start() - (last_event.get_start()%15)
                results = QuerentParser(querent.get_travel_details(
                    origins=event_places,
                    destinations=last_place,
                    arrival_time=dt.datetime(
                        day.get_year(), day.get_month(), day.get_day(),
                        globals.to_hours(arr_time)[0], globals.to_hours(arr_time)[1]
                    )
                ))
            else:
                dep_time = last_event.get_end() + (15-(last_event.get_start()%15))
                results = QuerentParser(querent.get_travel_details(
                    origins=last_place,
                    destinations=event_places,
                    departure_time=dt.datetime(
                        day.get_year(), day.get_month(), day.get_day(),
                        globals.to_hours(dep_time)[0], globals.to_hours(dep_time)[1]
                    )
                ))
            globals.debug("received api response!")

            durations = results.get_durations()

            for i in range(len(durations)):
                globals.debug("durations: " + str(durations))

                closest_event = durations.index(min(durations))
                travel_time = results.get_durations()[closest_event]

                if insert_before:
                    end_time = arr_time - travel_time
                    start_time = end_time - events[closest_event].get_duration()
                    travel_start = end_time
                    events[closest_event].set_place(results.get_origins()[closest_event])
                else:
                    start_time = dep_time + travel_time
                    end_time = start_time + events[closest_event].get_duration()
                    travel_start = dep_time
                    events[closest_event].set_place(results.get_destinations()[closest_event])

                if (end_time >= self.__time_end_day
                or start_time < self.__time_begin_day):
                    globals.debug("reached daily time limits!")
                    durations[closest_event] = float("inf")
                    if min(durations) == float("inf"):
                        globals.debug("no event fits between other event and time limits!")
                        return events
                    continue

                try:
                    globals.debug("trying to insert event " + events[closest_event].get_name())

                    day.add_event(
                        events[closest_event],
                        start_time,
                        end_time
                    )

                    globals.debug("inserted event!")

                    if travel_time > 0:
                        day.add_event(
                            Event(
                                "[... travelling ("+ str(travel_time) +"min) ...]",
                                Event.EventType.TRAVELLING,
                                start=travel_start,
                                end=travel_start + travel_time,
                                place=""
                            ),
                            travel_start,
                            travel_start + travel_time
                        )

                    globals.debug("removing inserted event")
                    last_event = events[closest_event]
                    del events[closest_event]

                    break

                except:
                    # collision exception while adding new event
                    globals.debug("two events collided! trying to insert next best event")
                    durations[closest_event] = float("inf")
                    if min(durations) == float("inf"):
                        globals.debug("no event fits between other events!")
                        return events
                    continue

        return events
    ########################################################################
    #  PLANNING-ALGORITHM -- END                                           #
    ########################################################################


    def import_ics(self, path):
        globals.debug("importing ics file from " + path + " ...")
        ics_file = open(path,'rb')
        ical = icalendar.Calendar.from_ical(ics_file.read())

        for ics_event in ical.walk():
            if ics_event.name == "VEVENT":
                title = ics_event.get('summary')
                start = ics_event.decoded('dtstart')
                end   = ics_event.decoded('dtend')
                place = ics_event.get('location')

                globals.debug("importing event " + title)

                #print(ics_event.decoded('dtstamp'))
                rrule = ics_event.get('rrule')
                if rrule:
                    rrule_last = rrule['UNTIL'][0]
                    curr_day = start

                    new_event = Event(
                        title,
                        Event.EventType.SPECIFIC,
                        start=globals.to_minutes(start.hour, start.minute),
                        end=globals.to_minutes(end.hour, end.minute),
                        place=place
                    )

                    while curr_day <= rrule_last:
                        # try/except bc of colliding events -> should at least raise an error msg or sth.
                        globals.debug("importing recurring event " + title + " on " + str(curr_day))
                        try:
                            self.add_event(new_event, [curr_day.day, curr_day.month, curr_day.year])
                        except Exception:
                            pass
                        finally:
                            if 'WEEKLY' in rrule['FREQ'][0]:
                                curr_day = curr_day + dt.timedelta(days=7)
                            else:
                                break
                else:
                    # try/except bc of colliding events -> should at least raise an error msg or sth.
                    try:
                        self.add_event(new_event, [start.day, start.month, start.year])
                    except:
                        continue

        ics_file.close()
        globals.debug("finished import!")


    def export_ics(self, path):
        globals.debug("exporting ics file to " + path + " ...")
        cal = icalendar.Calendar()

        for d in self.__days:
            for event in d.get_next_event():
                cal_event = icalendar.Event()

                cal_event.add('summary', event.get_name())
                cal_event.add('dtstart', dt.datetime(
                    d.get_year(), d.get_month(), d.get_day(),
                    globals.to_hours(event.get_start())[0], globals.to_hours(event.get_start())[1]
                ))
                cal_event.add('dtend', dt.datetime(
                    d.get_year(), d.get_month(), d.get_day(),
                    globals.to_hours(event.get_end())[0], globals.to_hours(event.get_end())[1]
                ))
                cal_event.add('location', event.get_place())

                cal.add_component(cal_event)

        ics_file = open(path, 'wb')
        ics_file.write(cal.to_ical())
        ics_file.close()
        globals.debug("finished export!")


    def get_time_begin_day(self):
        return self.__time_begin_day


    def get_time_end_day(self):
        return self.__time_end_day


    def get_day(self, day, month, year):
        for d in self.__days:
            if d.get_day() == day and d.get_month() == month and d.get_year() == year:
                return [d]
        return [self.add_day(day, month, year)]


    def get_day_event_names(self, day, month, year):
        return self.__get_day_event_names(self.get_day(day, month, year)[0])


    def __get_day_event_names(self, day):
        if not day.num_events():
            return None
        return day.get_event_names()


    def remove_event_from_day(self, day, month, year, event_nr):
        return self.__remove_event_from_day(self.get_day(day, month, year)[0], event_nr)


    def __remove_event_from_day(self, day, event_nr):
        event_id = day.remove_event(event_nr)
        return self.__remove_event(event_id)


    def __remove_event(self, event_id):
        if not event_id:
            return

        for i in range(len(self.__events)):
            e = self.__events[i]
            if e.get_id() == event_id:
                event_name = self.__events[i].get_name()
                del self.__events[i]
                return event_name


    def __get_next_day(self):
        currDay = dt.datetime.today() + dt.timedelta(days=1) #tomorrow
        while True:
            yield self.get_day(currDay.day, currDay.month, currDay.year)[0]
            currDay += dt.timedelta(days=1)


    def __str__(self):
        retString = ""

        for day in self.__days:
            retString = retString + ">> " + str(day) + " | " + day.get_dow() + " ["+ str(day.num_events()) +" Events]:\n"

            for event in day.get_next_event():
                retString = retString + str(event) + ".\n"

            retString = retString + "\n"

        return retString
