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
import planner.scheduler as scheduler
from planner.scheduler import Scheduler

import globals

class ActionUtterConfirm(Action):
    def name(self) -> Text:
        return "action_utter_confirm"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')
        dispatcher.utter_message("Scheduled event at " + location)


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_python_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # p = Scheduler()
        #
        # p.set_home("Str d Pariser Kommune 30")
        # p.set_planning_times(
        #     globals.to_minutes(8, 0),
        #     globals.to_minutes(20, 0)
        # )
        # p.set_max_events(8)
        #
        # p.add_event(Event(
        #     "Kuchenbacken",
        #     Event.EventType.SPECIFIC,
        #     start=globals.to_minutes(17,45),
        #     end=globals.to_minutes(19,00),
        #     place="Str d Pariser Kommune 30"),
        # [8,6,2019])
        #
        # print(p)

        # dispatcher.utter_message("copying tracker...")
        # tracker_copy = tracker.copy()
        #
        # dispatcher.utter_message("storing copy...")
        # globals.store_object(tracker_copy, "models/stored_models/", "marc_tracker")
        #
        dispatcher.utter_message("executed custom action")
        dispatcher.utter_message("UserID: " + str(tracker.current_state()["sender_id"]))

        return []
