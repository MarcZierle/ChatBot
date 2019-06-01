import logging, datetime as dt

from planner.event import Event
from planner.day import Day

class Scheduler():

    def __init__(self, querent):
        self.__querent = querent
        self.__time_begin_day = Scheduler.to_minutes(8, 0)    # 8 A.M.
        self.__time_end_day   = Scheduler.to_minutes(20, 0)   # 8 P.M.
        self.__days = []
        self.__events = []
        self.__unplanned_events = []    # list of events that need to be planned
        self.__home = "Berlin"      # start everday at this location
        self.__max_events = 5       # maximum number of events per day
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

        # 1. calc shortest distance btw. all events and home, rank them
        # 2. if day has specific events:
        #   2.1 check for first element that fits btw first specific event and home
        # else:
        #   2.2 add nearest event
        # [2.1 / 2.2: take rest times into account]
        # 

        lastTime = self.__time_begin_day

        daysGen = self.__get_next_day()
        currDay = daysGen.__next__()

        for event in self.__events:
            if not event.is_specific():

                if lastTime+event.get_duration() >= self.__time_end_day:
                    currDay = daysGen.__next__()

                currDay.add_event(event, lastTime, lastTime+event.get_duration())
                lastTime = lastTime + event.get_duration()


    def restore(self, path):
        pass


    def store(self, path):
        pass


    def to_minutes(hours, minutes):
        return hours*60 + minutes


    def to_hours(minutes):
        return [int(minutes/60), minutes%60]


    def __get_day(self, day, month, year):
        for d in self.__days:
            if d.get_day() == day and d.get_month() == month and d.get_year() == year:
                return [d]
        return [None]


    def __get_next_day(self):
        for day in self.__days:
            yield day


    def __str__(self):
        retString = ""

        for day in self.__days:
            retString = retString + ">> " + str(day) + ":\n"

            for event in day.get_next_event():
                retString = retString + str(event) + ".\n"

            retString = retString + "\n"

        return retString
