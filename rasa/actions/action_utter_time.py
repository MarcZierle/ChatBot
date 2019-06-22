# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

#from .. import test
from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner

import globals

class ActionUtterTime(Action):
    def name(self) -> Text:
        return "action_utter_time"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #time = next(tracker.get_latest_entity_values("time"), None)

        time_entity = next((e for e in tracker.latest_message['entities'] if e['entity'] == 'time'), None)
        #time_entity = tracker.latest_message['entities']
        dispatcher.utter_message("Found time: " + str(time_entity))
