from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from rasa.core.trackers import DialogueStateTracker

import datetime

from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import globals, settings, iso8601, ast
from googledistancematrix.querent import Querent


class IntroductionForm(FormAction):

    def name(self):
        settings.init_api_keys()
        self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
        self.__storage_path = "../storage/schedules/"
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

        userid = tracker.current_state()["sender_id"]
        place = str(tracker.get_slot("place"))
        time = ast.literal_eval(str(tracker.get_slot("time")))

        time_start = iso8601.parse_date(str(time['from']))
        time_end = iso8601.parse_date(str(time['to']))

        planner = ph.restore(self.__storage_path, userid)
        planner.set_home(place)
        planner.set_planning_times(
            globals.to_minutes(time_start.hour, time_start.minute),
            globals.to_minutes(time_end.hour, time_end.minute))
        ph.store(self.__storage_path, userid, planner)

        dispatcher.utter_message("Thank you! I have set your home location to " + place
            + " and will plan your day between " + time_start.strftime("%I:%M %p")
            + " and " + time_end.strftime("%I:%M %p") + ".")

        return []


    def validate_place(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        place = str(tracker.get_slot("place"))

        if not place:
            dispatcher.utter_message("Looks like there was an error with extracting the location.")
            return {"place": None}

        place = self.__querent.get_place_address(place)
        if not place:
            dispatcher_utter_message("The following location couldn't be found: " + tracker.get_slot("place"))
            return {"place": None}

        return {"place": str(place)}


    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        time = str(tracker.get_slot("time"))

        try:
            time = dict(value)
            if 'to' in time and 'from' in time:
                start_time = iso8601.parse_date(time['from'])
                end_time = iso8601.parse_date(time['to']) - datetime.timedelta(hours=1)
                if start_time < end_time:
                    time['to'] = str(end_time.isoformat())
                    return {"time": str(time)}
                else:
                    dispatcher.utter_message("It would be better to begin a day before ending it.")
        except:
            pass
        dispatcher.utter_message("Please tell me a time interval ranging from 12:00 AM to 23:59 PM.")
        return {"time": None}
