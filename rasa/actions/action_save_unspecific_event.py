from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

import ast

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import globals, settings
from googledistancematrix.querent import Querent

class ActionSaveUnspecificEvent(Action):
    def name(self) -> Text:
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        return "action_save_unspecific_event"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userid = tracker.current_state()["sender_id"]
        place = self.__querent.get_place_address(tracker.get_slot('place'))
        duration = int(ast.literal_eval(tracker.get_slot('duration'))['additional_info']['normalized']['value']/60)

        event_name = tracker.latest_message['text']

        if place:
            planner = ph.restore(userid)
            planner.add_event(Event(
                event_name,
                Event.EventType.UNSPECIFIC,
                duration=duration,
                place=place)
            )
            ph.store(userid, planner)

            (hours,minutes) = globals.to_hours(duration)
            if hours == 0:
                duration = str(minutes) + " minutes"
            elif minutes > 0:
                duration = str(hours) + " hours and " + str(minutes) + " minutes"
            else:
                duration = str(hours) + " hours"

            response = ("Alright. I'm planning the event "
                + event_name
                + " at "+ place
                + " which will take "  + str(duration) + ".")

            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("I'm sorry but I couldn't find the place you entered :(")

        return []
