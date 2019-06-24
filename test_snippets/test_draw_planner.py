from planner.plannertoimage import PlannerToImage
from planner.planner import Planner

import globals

from datetime import datetime as dt

if __name__ == "__main__":
    planner = Planner()

    planner.set_home("Str d Pariser Kommune 30")
    planner.set_planning_times(
        globals.to_minutes(8, 0),
        globals.to_minutes(20, 0)
    )
    planner.set_max_events(8)

    planner.import_ics('import_planner_draw.ics')
    #planner.import_ics('exported_calendar.ics')
    print(planner)

    PlannerToImage(planner, dt.today()).draw_image('test_image.png')
    #PlannerToImage(planner, dt(2019,4,11)).draw_image('test_image.png')
