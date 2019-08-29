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


class IntroductionForm(FormAction):

    def name(self):
        return "introduction_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["place", "time"]


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        return []


    def validate_place(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        return {"place" : None}


    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        try:
            time = dict(value)
            if 'to' in time and 'from' in time:
                start_time = iso8601.parse_date(time['from'])
                end_time = iso8601.parse_date(time['to'])
                if start_time < end_time:
                    return {"time": str(time)}
                else:
                    dispatcher.utter_message("It would be better to begin a day before ending it.")
        except:
            pass
        dispatcher.utter_message("Please tell me a time interval ranging from 12:00 AM to 23:59 PM.")
        return {"time": None}
