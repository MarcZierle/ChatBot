from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from rasa.core.trackers import DialogueStateTracker

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import iso8601


class RemoveEventForm(FormAction):

    def name(self):
        return "remove_event_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["time"]


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        time = str(tracker.get_slot("time"))
        dispatcher.utter_message("/remove_event" + time)

        return []


    def validate_place(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        time = str(tracker.get_slot("time"))
        try:
            time = iso8601.parse_date(time)
            return {"time" : str(time)}
        except:
            dispatcher.utter_message("Please give me just a day.")
            return {"time" : None}
