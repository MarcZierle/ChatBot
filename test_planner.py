from planner.day import Day
from planner.event import Event
import planner.scheduler as scheduler
from planner.scheduler import Scheduler

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import settings
settings.init()

gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.set_travel_mode(Querent.TravelMode.TRANSIT)

p = Scheduler(gdm_querent)

p.set_home("Str d Pariser Kommune 30")
p.set_planning_times(
    scheduler.to_minutes(8, 0),
    scheduler.to_minutes(20, 0)
)
p.set_max_events(8)

p.add_event(Event(
    "Kuchenbacken",
    Event.EventType.SPECIFIC,
    start=scheduler.to_minutes(17,45),
    end=scheduler.to_minutes(19,00),
    place="Str d Pariser Kommune 30"),
[8,6,2019])

p.add_event(Event(
    "Buch lesen",
    Event.EventType.SPECIFIC,
    start=scheduler.to_minutes(13,20),
    end=scheduler.to_minutes(14,00),
    place="Erwin Schrödinger Zentrum"),
[8,6,2019])

p.add_event(Event(
    "Konzert",
    Event.EventType.SPECIFIC,
    start=scheduler.to_minutes(19,00),
    end=scheduler.to_minutes(20,00),
    place="Philharmonie Berlin"),
[22,6,2019])

p.add_event(Event(
    "Einkaufen",
    Event.EventType.UNSPECIFIC,
    duration=105,
    place="Kaufland Storkower Str")
)

p.add_event(Event(
    "Spazierengehen",
    Event.EventType.UNSPECIFIC,
    duration=45,
    place="Volkspark Friedrichshain Berlin")
)

p.add_event(Event(
    "Sport",
    Event.EventType.UNSPECIFIC,
    duration=60,
    place="Alexanderplatz 7")
)

p.add_event(Event(
    "Klausurvorbereitung",
    Event.EventType.UNSPECIFIC,
    duration=4*60,
    place="Erwin Schrödinger Zentrum Berlin")
)

p.add_event(Event(
    "Train Spotting I",
    Event.EventType.UNSPECIFIC,
    duration=10,
    place="Adlershof Berlin")
)

p.add_event(Event(
    "Train Spotting II",
    Event.EventType.UNSPECIFIC,
    duration=60,
    place="Adlershof Berlin")
)

p.replan()

print(p)

print("Used GDM-API - Calls: " + str(gdm_querent.get_api_count()))
