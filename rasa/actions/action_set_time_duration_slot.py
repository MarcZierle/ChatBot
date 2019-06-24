from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker
from rasa.core.events import SlotSet

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner

import globals, settings
from googledistancematrix.querent import Querent

class ActionSetTimeDurationSlot(Action):
    def name(self) -> Text:
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        return "action_set_time_duration_slot"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message("action_set_time_duration_slot")

        #dispatcher.utter_message("UserID: " + str(tracker.current_state()["sender_id"]))

        time_entity     = next((e for e in tracker.latest_message['entities'] if e['entity'] == 'time'), None)
        duration_entity = next((e for e in tracker.latest_message['entities'] if e['entity'] == 'duration'), None)

        slot = None

        if time_entity:
            #dispatcher.utter_message("Found time: " + str(time_entity))
            slot = SlotSet('time', str(time_entity))

        if duration_entity:
            #dispatcher.utter_message("Found duration: " + str(duration_entity))
            slot = SlotSet('duration', str(duration_entity))

        return [slot]
