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

import globals, settings
from googledistancematrix.querent import Querent

class SetHomeForm(FormAction):

	def name(self):
		settings.init_api_keys()
		self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
		self.__storage_path = "../storage/schedules/"
		return "set_home_form"
		
	
	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		return ["place"]
		
	
	def submit(
		self,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> List[Dict]:
	
		place = str(tracker.get_slot("place"))
		userid 	= str(tracker.current_state()["sender_id"])
		
		planner = ph.restore(self.__storage_path, userid)
		planner.set_home(place)
		ph.store(self.__storage_path, userid, planner)
		
		dispatcher.utter_message("Home set to " + place)
		return []
		
		
	def validate_place(
		self,
		value: Text,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> Optional[Text]:
		place 	= str(tracker.get_slot("place"))
		place = self.__querent.get_place_address(place)
		if place:
			return {"place": str(place)}
		else:
			return{"place": None}
		
		
		