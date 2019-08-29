from planner.event import Event

from datetime import datetime

class Day():

    def __init__(self, day, month, year):
        self.__day    = day
        self.__month  = month
        self.__year   = year
        self.__events = []


    def get_date(self):
        return [self.__day, self.__month, self.__year]


    def get_day(self):
        return self.__day


    def get_month(self):
        return self.__month


    def get_year(self):
        return self.__year


    def num_events(self):
        return len([e for e in self.__events if not e.is_travelling()])


    def get_next_event(self):
        for event in self.__events:
            yield event


    def get_next_specific_event(self):
        sp_events = [e for e in self.__events if e.is_specific()]
        for e in sp_events:
            yield e


    def num_specific_events(self):
        return len([e for e in self.__events if e.is_specific()])


    # checks whether time[2] = [start, end] and any planned event falls together
    def does_collide(self, time):
        pass


    def remove_unspecific(self):
        self.__events = [e for e in self.__events if e.is_specific()]


    # returns the day of week (monday, tuesday, etc.)
    def get_dow(self):
        return datetime(self.__year, self.__month, self.__day).strftime("%A")


    def get_event_names(self):
        return [e.get_name() for e in self.__events if not e.is_travelling()]


    def remove_event(self, event_nr):
        #try:
        print([e.get_id() for e in self.__events if not e.is_travelling()])
        event_id = [e.get_id() for e in self.__events if not e.is_travelling()][event_nr]
        for i in range(len(self.__events)):
            e = self.__events[i]
            if e.get_id() == event_id:
                del self.__events[i]
                break
        return event_id
        #except Exception:
        #    return None


    def add_event(self, event, start=None, end=None):
        if not event.is_specific():
            if not start or not end:
                raise Exception("Adding unspecific events requires start and end time!")
            event.set_time(start, end)
        elif not start or not end:
            start = event.get_start()
            end = event.get_end()

        for other in self.__events:
            if (not start or not end or
            not other.get_start() or not other.get_end()):
                continue

            if (( start >= other.get_start() and start < other.get_end() )
            or ( end > other.get_start() and end <= other.get_end() )
            or ( start >= other.get_start() and end <= other.get_end())
            or ( start < other.get_start() and end > other.get_end()) ):
                raise Exception(
                    "Events " + str(event) + " and " + str(other)
                    + " are overlapping! Cannot add new event on day " + str(self)
                )

        self.__events.append(event)
        self.__events.sort(key=lambda e: e.get_start())


    def __str__(self):
        return str(self.__day) + "/" + str(self.__month) + "/" + str(self.__year)
