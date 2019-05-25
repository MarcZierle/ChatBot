from enum import Enum, auto

class Event():

    class EventType(Enum):
        # useing auto() where exact value is unimportant 
        SPECIFIC = auto()
        UNSPECIFIC = auto()


    def __init__(self, type):
        self.__type = EventType.UNSPECIFIC
        self.__time_start = 0
        self.__time_end   = 0


    def get_start(self):
        return self.__time_start

    def get_end(self):
        return self.__time_end
