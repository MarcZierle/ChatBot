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
        self.__max_events = 8       # maximum number of events per day
        self.__max_rest_time = 30   # maximum amount of time (min) for a break btw events
        self.__min_rest_time = 5    # minimum amount of time (min) for a break btw events


    def set_home(self, home):
        self.__home = home


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
                    if is_last_event:
                        self.__unplanned_events = self.__insert_after_events_to_day(
                            self.__unplanned_events,
                            currDay,
                            sp_event
                        )
                    else:
                        self.__unplanned_events = self.__insert_before_events_to_day(
                            self.__unplanned_events,
                            currDay,
                            sp_event
                        )
            else:
                # no specific events for current day
                self.__unplanned_events = self.__insert_after_events_to_day(
                    self.__unplanned_events,
                    currDay,
                    Event(
                        "Home",
                        Event.EventType.SPECIFIC,
                        self.__time_begin_day-10,
                        self.__time_begin_day,
                        place = self.__home
                    )
                )


    # trys to insert given events before given end_event
    # exits after first collision in day or time_begin_day has been reached
    # returns all events that could not be planned
    # Note: Distance calculations will be done; max_events will be considered
    def __insert_before_events_to_day(self, events, day, end_event):
        dest_place = end_event.get_place()
        last_event = end_event

        while events:
            if day.num_events() >= self.__max_events:
                break

            event_places = [e.get_place() for e in events]
            results = QuerentParser(self.__querent.get_travel_details(
                event_places,
                dest_place,
                arrival_time=dt.datetime(
                    day.get_year(), day.get_month(), day.get_day(),
                    to_hours(last_event.get_start())[0], to_hours(last_event.get_start())[1]
                )
            ))

            closest_event = results.get_duations().index(min(results.get_duations()))
            travel_time = results.get_duations()[closest_event]

            end_time = last_event.get_start() - travel_time
            start_time = end_time - events[closest_event].get_duration()

            if start_time < self.__time_begin_day:
                break

            day.add_event(
                events[closest_event],
                start_time,
                end_time
            )

            last_event = events[closest_event]
            del events[closest_event]

        return events


    # trys to insert given events after given start_event
    # exits after first collision in day or time_end_day has been reached
    # returns all events that could not be planned
    # Note: Distance calculations will be done; max_events will be considered
    def __insert_after_events_to_day(self, events, day, start_event):
        dest_place = start_event.get_place()
        last_event = start_event

        while events:
            if day.num_events() >= self.__max_events:
                break

            event_places = [e.get_place() for e in events]
            results = QuerentParser(self.__querent.get_travel_details(
                event_places,
                dest_place,
                departure_time=dt.datetime(
                    day.get_year(), day.get_month(), day.get_day(),
                    to_hours(last_event.get_end())[0], to_hours(last_event.get_end())[1]
                )
            ))

            closest_event = results.get_duations().index(min(results.get_duations()))
            travel_time = results.get_duations()[closest_event]

            start_time = last_event.get_end() + travel_time
            end_time = start_time + events[closest_event].get_duration()

            if end_time >= self.__time_end_day:
                break

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
            retString = retString + ">> " + str(day) + ":\n"

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
