from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

import json
from datetime import datetime as dt

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import globals, settings
from googledistancematrix.querent import Querent

class ActionSaveSpecificEvent(Action):
    def name(self) -> Text:
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        return "action_save_specific_event"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userid = str(tracker.current_state()["sender_id"])
        place = self.__querent.get_place_address(tracker.get_slot('place'))

        time = json.loads(tracker.get_slot('time').replace("'", '"'))
        if time['additional_info']['type'] == 'interval':
            time_start   = dt.strptime(str(time['additional_info']['from']['value']), '%Y-%m-%dT%H:%M:%S.000+02:00')
            time_end     = dt.strptime(str(time['additional_info']['to']['value']), '%Y-%m-%dT%H:%M:%S.000+02:00')
        else:
            dispatcher.utter_message("For planning events using an exact time frame I need a start and an end time.")

        event_name = tracker.latest_message['text']


        if place:
            planner = ph.restore(userid)
            planner.add_event(Event(
                event_name,
                Event.EventType.SPECIFIC,
                start=globals.to_minutes(time_start.hour, time_start.minute),
                end=globals.to_minutes(time_end.hour, time_end.minute),
                place=place),
            [time_start.day, time_start.month, time_start.year])
            ph.store(userid, planner)

            response = ("Alright. I'm planning the event "
                + event_name
                + " at "+ place
                + " on " + time_start.strftime("%A") + ", " + time_start.strftime("%d.%m.%y")
                + " from " + time_start.strftime("%I:%M %p") + " to " + time_end.strftime("%I:%M %p") + ".")

            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("I'm sorry but I couldn't find the place you entered :(")

        return []
