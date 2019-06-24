from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import globals, settings
from googledistancematrix.querent import Querent

class ActionShowPlan(Action):
    def name(self) -> Text:
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        return "action_show_plan"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userid = str(tracker.current_state()["sender_id"])

        planner = ph.restore(userid)
        planner.replan(self.__querent)
        ph.store(userid, planner)

        dispatcher.utter_message(str(planner))

        return []
