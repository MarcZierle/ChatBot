import logging, datetime as dt

from scheduler.day import Day
from scheduler.event import Event

class Scheduler():

    def __init__(self, querent):
        self.__querent = querent
        self.__time_begin_day = Scheduler.to_minutes(8, 0)    # 8 A.M.
        self.__time_end_day   = Scheduler.to_minutes(20, 0)   # 8 P.M.
        self.__days = []
        self.__events = []


    def add_event(self, event):
        pass


    def replan(self):
        pass


    def restore(self, path):
        pass


    def store(self, path):
        pass


    def to_minutes(hours, minutes):
        return hours*60 + minutes


    def to_hours(minutes):
        return [int(minutes/60), minutes%60]
