from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import settings, globals
settings.init()

gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.set_travel_mode(querent.TravelMode.TRANSIT)

p = Planner()

p.set_home("Str d Pariser Kommune 30")
p.set_planning_times(
    globals.to_minutes(8, 0),
    globals.to_minutes(20, 0)
)
p.set_max_events(3)

p.add_event(Event(
    "Kuchenbacken",
    Event.EventType.SPECIFIC,
    start=globals.to_minutes(17,45),
    end=globals.to_minutes(19,00),
    place="Str d Pariser Kommune 30"),
[30,6,2019])

p.add_event(Event(
    "Buch lesen",
    Event.EventType.SPECIFIC,
    start=globals.to_minutes(13,20),
    end=globals.to_minutes(14,00),
    place="Erwin Schrödinger Zentrum"),
[29,6,2019])

p.add_event(Event(
    "Konzert",
    Event.EventType.SPECIFIC,
    start=globals.to_minutes(19,00),
    end=globals.to_minutes(20,00),
    place="Philharmonie Berlin"),
[26,6,2019])

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

p.replan(gdm_querent)

print(p)

#p.export_ics("import_planner_draw.ics")

print(p.get_day_event_names(6,7,2019))
p.remove_event_from_day(6,7,2019, 1)

print(p)

print("Used GDM-API - Calls: " + str(gdm_querent.get_api_count()))
