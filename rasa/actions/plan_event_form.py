from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from rasa.core.trackers import DialogueStateTracker

class PlanEventForm(FormAction):


    def name(self):
        return "plan_event_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["place", "time", "event_name"]


    def submit(self):
        dispatcher.utter_message("Event planned.")
        return []
