from planner.day import Day
from planner.event import Event
from planner.scheduler import Scheduler

p = Scheduler(None)

p.add_day(1, 6, 2019)
p.add_day(2, 6, 2019)

p.add_event(Event(
    "Kuchenbacken",
    Event.EventType.SPECIFIC,
    start=Scheduler.to_minutes(15,30),
    end=Scheduler.to_minutes(16,45),
    place="here"),
[2,6,2019])

p.add_event(Event(
    "Buch lesen",
    Event.EventType.SPECIFIC,
    start=Scheduler.to_minutes(15,20),
    end=Scheduler.to_minutes(15,30),
    place="here"),
[2,6,2019])

p.add_event(Event(
    "Einkaufen",
    Event.EventType.UNSPECIFIC,
    duration=105,
    place="here")
)

p.add_event(Event(
    "Spazierengehen",
    Event.EventType.UNSPECIFIC,
    duration=45,
    place="here")
)

p.replan()

print(p)
