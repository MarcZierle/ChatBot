from scheduler.event import Event

class Day():

    def __init__(self, day, month, year):
        self.__day    = day
        self.__month  = month
        self.__year   = year
        self.__events = []


    def get_date(self):
        return [self.__day, self.__month, self.__year]


    def get_next_event(self, time):
        pass


    def add_event(self, event):
        self.__events.append(event)
        self.__events.sort(key=lambda e: e.get_start())
