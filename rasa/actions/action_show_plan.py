from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph
from planner.plannertoimage import PlannerToImage

import globals, settings
from googledistancematrix.querent import Querent

from datetime import datetime as dt

class ActionShowPlan(Action):
    def name(self) -> Text:
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        self.__storage_path = "../storage/schedules/"
        return "action_show_plan"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userid = str(tracker.current_state()["sender_id"])

        planner = ph.restore(self.__storage_path, userid)
        planner.replan(self.__querent)
        ph.store(self.__storage_path, userid, planner)

        PlannerToImage(planner, dt.today()).draw_image("../storage/schedule_images/"+str(userid)+'.png')
        dispatcher.utter_message("/show_plan")

        return []
