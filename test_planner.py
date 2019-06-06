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
gdm_querent.settravelmode(Querent.TravelMode.TRANSIT)

p = Scheduler(gdm_querent)

p.add_day(7, 6, 2019)
p.add_day(8, 6, 2019)

p.add_event(Event(
    "Kuchenbacken",
    Event.EventType.SPECIFIC,
    start=scheduler.to_minutes(15,30),
    end=scheduler.to_minutes(16,45),
    place="Str d Pariser Kommune 30"),
[7,6,2019])

p.add_event(Event(
    "Buch lesen",
    Event.EventType.SPECIFIC,
    start=scheduler.to_minutes(13,20),
    end=scheduler.to_minutes(14,00),
    place="Erwin Schrödinger Zentrum"),
[7,6,2019])

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

p.replan()

print(p)
