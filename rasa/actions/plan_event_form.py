from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from rasa.core.trackers import DialogueStateTracker

import ast, json, datetime
from datetime import datetime as dt


class PlanEventForm(FormAction):

    def name(self):
        return "plan_event_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        slots = ["place","event_name"]
        if tracker.get_slot("is_specific")== "True":
            slots.append("time")
        elif tracker.get_slot("is_specific")== "False":
            slots.append("duration")
        else :
            slots.append("is_specific")
        return slots


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        return []


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
            "time": self.from_entity(entity="time"),
            "duration": self.from_entity(entity="duration"),
            "is_specific": [
                self.from_entity(entity="is_specific"),
                self.from_intent(intent="affirm", value="True"),
                self.from_intent(intent="deny", value="False"),
            ],
            "event_name": self.from_text()
            }


    def validate_duration(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        duration_entity = str(next((e for e in tracker.latest_message["entities"] if e["entity"] == "duration"), None))
        if duration_entity:
            duration_in_sec = int(ast.literal_eval(duration_entity)['additional_info']['normalized']['value']/60)
            return {"duration": str(duration_in_sec)}
        else:
            return {"duration": None}


    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        try:
            time = dict(value)#json.loads(str(value).replace("'", '"'))
            if 'to' in time or 'from' in time:
                return {"time": str(time)}
        except:
            pass
        return {"time": None}
