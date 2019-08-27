from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from rasa.core.trackers import DialogueStateTracker
from rasa.core.events import SlotSet

class PlanEventForm(FormAction):

    user_duration_replacements = {}

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

        user_id = str(tracker.current_state()["sender_id"])

        if not user_id in PlanEventForm.user_duration_replacements:
            PlanEventForm.user_duration_replacements[user_id] = None
        
        if not PlanEventForm.user_duration_replacements[user_id] and tracker.get_slot("duration"):
            duration_entity = next((e for e in tracker.latest_message["entities"] if e["entity"] == "duration"), None)
            if duration_entity:
                PlanEventForm.user_duration_replacements[user_id] = str(duration_entity)
        
        return slots


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message("Event planned.")
        
        user_id = str(tracker.current_state()["sender_id"])
        slot_value = PlanEventForm.user_duration_replacements[user_id]
        del PlanEventForm.user_duration_replacements[user_id]
        return [SlotSet("duration", slot_value)]

    
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
