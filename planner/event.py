from enum import Enum, auto

class Event():

    class EventType(Enum):
        # useing auto() where exact value is unimportant
        SPECIFIC = auto()
        UNSPECIFIC = auto()


    def __init__(self, name, type, start=0, end=0, duration=0, place="Berlin"):
        self.__name = name
        self.__type = type
        self.__start = start
        self.__end   = end

        if start > 0 and end > 0:
            self.__duration = end - start
        else:
            self.__duration = duration;

        if self.__start >= self.__end and self.__type == Event.EventType.SPECIFIC:
            raise Exception("End time must be after start time!")

        if self.__duration == 0 and self.__type == Event.EventType.UNSPECIFIC:
            raise Exception("Unspecific event must have a duration!")

        if self.__end == 0 and self.__type == Event.EventType.SPECIFIC:
            raise Exception("Specific event must have start and end time > 0!")

        self.__place = place


    def get_start(self):
        return self.__time_start

    def get_end(self):
        return self.__time_end
