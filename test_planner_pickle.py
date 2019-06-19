from planner.day import Day
from planner.event import Event
import planner.scheduler as scheduler
from planner.scheduler import Scheduler

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import pickle

import settings
settings.init()

unpickle = True

gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.set_travel_mode(Querent.TravelMode.TRANSIT)

if not unpickle:
    # create new planner object and pickle it
    p = Scheduler()

    p.set_home("Str d Pariser Kommune 30")
    p.set_planning_times(
        scheduler.to_minutes(8, 0),
        scheduler.to_minutes(20, 0)
    )
    p.set_max_events(8)

    p.import_ics("marc_uni.ics")

    pickle.dump(p, open("planner_pickle.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
else:
    # try to load an existing pickled planner object
    try :
        p = pickle.load(open("planner_pickle.pkl","rb"))
    except FileNotFoundError :
        logging.error("Test Planner Pickle: Restore File or Folder not found.")
        exit()


print(p)

print("Used GDM-API - Calls: " + str(gdm_querent.get_api_count()))
