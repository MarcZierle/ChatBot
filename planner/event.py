from enum import Enum, auto

class Event():

    class EventType(Enum):
        # useing auto() where exact value is unimportant
        SPECIFIC = auto()
        UNSPECIFIC = auto()
        TRAVELLING = auto()


    num_all_events = 0


    def __init__(self, name, type, start=0, end=0, duration=0, place="Berlin"):
        self.__name = name
        self.__type = type
        self.__start = start
        self.__end   = end

        if type == Event.EventType.SPECIFIC and duration:
            raise Exception("Specific event needs no duration!")

        if start > 0 and end > 0:
            self.__duration = end - start
        else:
            self.__duration = duration;

        if self.__start >= self.__end and self.__type == Event.EventType.SPECIFIC:
            raise Exception("End time must be after start time! (start: "+str(start)+"; end: "+str(end)+")")

        if not self.__duration and self.__type == Event.EventType.UNSPECIFIC:
            raise Exception("Unspecific event must have a duration!")

        if self.__end == 0 and self.__type == Event.EventType.SPECIFIC:
            raise Exception("Specific event must have start and end time > 0!")

        self.__place = place

        self.__id = Event.num_all_events
        Event.num_all_events = Event.num_all_events + 1


    def get_id(self):
        return self.__id


    def get_name(self):
        return self.__name


    def get_start(self):
        return self.__start


    def get_end(self):
        return self.__end


    def get_duration(self):
        return self.__duration


    def get_place(self):
        return self.__place


    def set_place(self, place):
        self.__place = place


    def is_specific(self):
        if self.__type == Event.EventType.SPECIFIC:
            return True
        else:
            return False


    def is_travelling(self):
        if self.__type == Event.EventType.TRAVELLING:
            return True
        else:
            return False


    def set_time(self, start, end):
        if start >= end:
            raise Exception("End time must be after start time!")
        self.__duration = end - start
        self.__start = start
        self.__end = end


    def __str__(self):
        [startH, startM] = [int(self.__start/60), self.__start%60]
        [endH, endM] = [int(self.__end/60), self.__end%60]

        return (
            str(startH).zfill(2)+":"+str(startM).zfill(2)
            +"   -   "
            +str(endH).zfill(2)+":"+str(endM).zfill(2)
            +"\t"+
            self.__name
            +"\t"+
            self.__place
        )
