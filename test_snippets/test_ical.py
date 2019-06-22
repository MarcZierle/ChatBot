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
p.set_max_events(8)


#p.import_ics('marc_uni.ics')
p.import_ics('exported_calendar.ics')

#p.export_ics('exported_calendar.ics')


print(p)
print("Used GDM-API - Calls: " + str(gdm_querent.get_api_count()))
