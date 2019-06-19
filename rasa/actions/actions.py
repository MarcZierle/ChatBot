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

#from .. import test
from planner.day import Day
from planner.event import Event
import planner.scheduler as scheduler
from planner.scheduler import Scheduler


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_python_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        p = Scheduler(None)

        p.set_home("Str d Pariser Kommune 30")
        p.set_planning_times(
            scheduler.to_minutes(8, 0),
            scheduler.to_minutes(20, 0)
        )
        p.set_max_events(8)

        p.add_event(Event(
            "Kuchenbacken",
            Event.EventType.SPECIFIC,
            start=scheduler.to_minutes(17,45),
            end=scheduler.to_minutes(19,00),
            place="Str d Pariser Kommune 30"),
        [8,6,2019])

        print(p)

        dispatcher.utter_message("Hello Planner!")

        return []
