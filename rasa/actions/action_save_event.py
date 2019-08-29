from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa.core.trackers import DialogueStateTracker

import json
import datetime
from datetime import datetime as dt

import ast, iso8601
from planner.day import Day
from planner.event import Event
import planner.planner as planner
from planner.planner import Planner
from planner import plannerhandler as ph

import globals, settings
from googledistancematrix.querent import Querent


class ActionSaveEvent(Action):
	
	def name(self) -> Text:
		settings.init_api_keys()
		self.__querent = Querent(settings.GOOGLE_DISTANCE_MATRIX_API_KEY)
		self.__storage_path = "../storage/schedules/"
		return "action_save_event"
		

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		userid 	= tracker.current_state()["sender_id"]
		
		place 		= str(tracker.get_slot("place"))
		event_name 	= str(tracker.get_slot("event_name"))
		is_specific	= tracker.get_slot("is_specific")
		
		time 		= tracker.get_slot("time")
		duration	= tracker.get_slot("duration")
		
		if not place or not event_name:
			dispatcher.utter_message("Looks like there was an error with extracting the location or event name")
			return []
		
		place = self.__querent.get_place_address(place)
		if not place:
			dispatcher.utter_message("The following location couldn't be found: " + tracker.get_slot("place"))
			return []
		if not (is_specific == None):
			is_specific = (is_specific == "True")
			if is_specific:
				#save_specific_event
				self.save_specific_event(dispatcher, tracker, userid, place, event_name, time)
			else:
				#save_unspecific_event
				self.save_unspecific_event(dispatcher, tracker, userid, place, event_name, duration)
		else:
			#missing is_specific state
			if (not time == None) != (not duration == None):
				#either time or duration is set, so valid state
				if time:
					#save_specific_event
					self.save_specific_event(dispatcher, tracker, userid, place, event_name, time)
				elif duration:
					#save_unspecific_event
					self.save_unspecific_event(dispatcher, tracker, userid, place, event_name, duration)
			else:
				dispatcher.utter_message("Event time or duration couldn't be extracted correctly.")
		return []	
	
	
	def save_specific_event(self, dispatcher: CollectingDispatcher, tracker: Tracker, userid, place, event_name, time):
		time = ast.literal_eval(time)
		time_start 	= iso8601.parse_date(str(time["from"]))
		time_end 	= iso8601.parse_date(str(time["to"]))
		planner = ph.restore(self.__storage_path, userid)
		try:
			planner.add_event(Event(
				event_name,
				Event.EventType.SPECIFIC,
				start=globals.to_minutes(time_start.hour, time_start.minute),
				end=globals.to_minutes(time_end.hour, time_end.minute),
				place=place),
			[time_start.day, time_start.month, time_start.year])
		except Exception:
			dispatcher.utter_message("It seems like you already planned an event at this time.")
			return []
		ph.store(self.__storage_path, userid, planner)

		response = ("Alright. I'm planning the event "
			+ event_name
			+ " at "+ place
			+ " on " + time_start.strftime("%A") + ", " + time_start.strftime("%d.%m.%y")
			+ " from " + time_start.strftime("%I:%M %p") + " to " + time_end.strftime("%I:%M %p") + ".")

		dispatcher.utter_message(response)
		
		
	def save_unspecific_event(self, dispatcher: CollectingDispatcher, tracker: Tracker, userid, place, event_name, duration):
		
		duration = int(duration)
		planner = ph.restore(self.__storage_path, userid)
		planner.add_event(Event(
				event_name,
				Event.EventType.UNSPECIFIC,
				duration=duration,
				place=place)
		)
		ph.store(self.__storage_path, userid, planner)

		(hours,minutes) = globals.to_hours(duration)
		if hours == 0:
			duration = str(minutes) + " minutes"
		elif minutes > 0:
			if hours > 1:
				duration = str(hours) + " hours and " + str(minutes) + " minutes"
			else:
				duration = str(hours) + " hour and " + str(minutes) + " minutes"
		else:
			if hours > 1:
				duration = str(hours) + " hours"
			else:
				duration = str(hours) + " hour"

		response = ("Alright. I'm planning the event "
			+ event_name
			+ " at "+ place
			+ " which will take "  + str(duration) + ".")

		dispatcher.utter_message(response)
