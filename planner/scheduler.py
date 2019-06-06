import logging, datetime as dt

from planner.event import Event
from planner.day import Day

from googledistancematrix.querent_parser import QuerentParser

class Scheduler():

    def __init__(self, querent):
        self.__querent = querent
        self.__time_begin_day = to_minutes(8, 0)    # 8 A.M.
        self.__time_end_day   = to_minutes(20, 0)   # 8 P.M.
        self.__days = []
        self.__events = []
        self.__unplanned_events = []    # list of events that need to be planned
        self.__home = "Berlin"      # start everday at this location
        self.__max_events = 99       # maximum number of events per day
        self.__round_travel_time = 15 # arrival and departure times will be rounded to the next quarter hours


    def set_home(self, home):
        self.__home = home


    def set_planning_times(self, start_time, end_time):
        self.__time_begin_day = start_time
        self.__time_end_day = end_time


    def add_day(self, day, month, year):
        day = Day(day, month, year)
        self.__days.append(day)
        return day


    def add_event(self, event, date=None):
        if event.is_specific():
            if not date:
                raise Exception("Adding a specific event needs a day!")

            day = self.__get_day(date[0], date[1], date[2])[0]
            if not day:
                day = self.add_day(date[0], date[1], date[2])
            day.add_event(event)

        self.__events.append(event)

    ########################
    #  PLANNING-ALGORITHM  #
    ########################
    def replan(self):
        # remove all previously planned (unspecific) events
        [d.remove_unspecific() for d in self.__days]

        # mark all events as unplanned
        self.__unplanned_events = [e for e in self.__events if not e.is_specific()]

        #lastTime = self.__time_begin_day

        daysGen = self.__get_next_day()
        currDay = daysGen.__next__()

        for currDay in self.__get_next_day():
            if currDay.num_specific_events() > 0:
                for sp_event, is_last_event in lookahead(currDay.get_next_specific_event()):
                    self.__unplanned_events = self.__insert_events_to_day(
                        self.__unplanned_events,
                        currDay,
                        sp_event,
                        not is_last_event
                    )
            else:
                # no specific events for current day
                self.__unplanned_events = self.__insert_events_to_day(
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

        unplanned_events_str = ["- " + e.get_name() for e in self.__unplanned_events]
        if not unplanned_events_str:
            print("All events could be planned!")
        else:
            print("Still unplanned events:")
            for s in unplanned_events_str:
                print("    " + s)
        print("\n")


    # trys to insert given events after/before given first_event
    # exits after first collision in day or time_end_day/time_start_day has been reached
    # returns all events that could not be planned
    # Note: Distance calculations will be done; max_events will be considered
    def __insert_events_to_day(self, events, day, first_event, insert_before=True):
        last_event = first_event

        while events:
            if day.num_events() >= self.__max_events:
                break

            event_places = [e.get_place() for e in events]

            last_place = last_event.get_place()

            if insert_before:
                arr_time = last_event.get_start() - (last_event.get_start()%15)
                results = QuerentParser(self.__querent.get_travel_details(
                    origins=event_places,
                    destinations=last_place,
                    arrival_time=dt.datetime(
                        day.get_year(), day.get_month(), day.get_day(),
                        to_hours(arr_time)[0], to_hours(arr_time)[1]
                    )
                ))
            else:
                dep_time = last_event.get_end() + (15-(last_event.get_start()%15))
                results = QuerentParser(self.__querent.get_travel_details(
                    origins=last_place,
                    destinations=event_places,
                    departure_time=dt.datetime(
                        day.get_year(), day.get_month(), day.get_day(),
                        to_hours(dep_time)[0], to_hours(dep_time)[1]
                    )
                ))

            closest_event = results.get_durations().index(min(results.get_durations()))
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
                break

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

            day.add_event(
                events[closest_event],
                start_time,
                end_time
            )

            last_event = events[closest_event]
            del events[closest_event]

        return events


    def restore(self, path):
        pass


    def store(self, path):
        pass


    def __get_day(self, day, month, year):
        for d in self.__days:
            if d.get_day() == day and d.get_month() == month and d.get_year() == year:
                return [d]
        return [None]


    def __get_next_day(self):
        for day in self.__days:
            yield day


    global to_minutes
    def to_minutes(hours, minutes):
        return hours*60 + minutes


    global to_hours
    def to_hours(minutes):
        return [int(minutes/60), minutes%60]


    def __str__(self):
        retString = ""

        for day in self.__days:
            retString = retString + ">> " + str(day) + " ["+ str(day.num_events()) +" Events]:\n"

            for event in day.get_next_event():
                retString = retString + str(event) + ".\n"

            retString = retString + "\n"

        return retString


    global lookahead
    def lookahead(iterable):
        """Pass through all values from the given iterable, augmented by the
        information if there are more values to come after the current one
        (False), or if it is the last value (True).
        """
        # Get an iterator and pull the first value.
        it = iter(iterable)
        last = next(it)
        # Run the iterator to exhaustion (starting from the second value).
        for val in it:
            # Report the *previous* value (more to come).
            yield last, False
            last = val
        # Report the last value.
        yield last, True
