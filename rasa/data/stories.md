## being polite to the user
* greet
    - utter_greet

## user asks for information about bot
* get_infos
	- utter_infos
	
<!--------------------------->
<!-- START: EVENT PLANNING -->
<!--------------------------->
## plan event form
* plan_event
	- plan_event_form
	- form{"name": "plan_event_form"}
	- form{"name": null}
	- action_save_event
	- action_restart

## set home form
* set_home
	- set_home_form
	- form{"name":"set_home_form"}
	- form{"name": null}
	- action_restart
	
<!------------------------->
<!-- END: EVENT PLANNING -->
<!------------------------->

## user requests the generated plan
* show_plan
    - utter_show_plan
    - action_show_plan
    - action_restart


## fallback story
* out_of_scope
    - action_default_fallback


<!-- Small-Talk -->
## how are you - good
* how_are_you
	- utter_im_fine
* feeling_good
	- utter_good
	
## how are you - bad
* how_are_you
	- utter_im_fine
* feeling_bad
	- utter_cheer_up
	
## okay
* okay
	- utter_okay
	
## goodbye
* goodbye
	- utter_goodbye
	
## whats up
* whats_up
	- utter_not_much
	
## talk_to_me
* talk_to_me
	-utter_talk
	
## weather
* weather
	-utter_weather
	
## small-talk
* small-talk
	-utter_small-talk
	
## emoji
* emoji
	-utter_emoji

## interactive_story_1
* greet
    - utter_greet
* how_are_you
    - utter_im_fine
* feeling_good
    - utter_good
* goodbye
    - utter_goodbye

## interactive_story_1
* help
    - utter_infos
* plan_event{"place": "unter den linden 6", "time": "{'to': '2019-08-30T16:01:00.000+02:00', 'from': '2019-08-30T14:00:00.000+02:00'}"}
    - slot{"place": "unter den linden 6"}
    - slot{"time": "{'to': '2019-08-30T16:01:00.000+02:00', 'from': '2019-08-30T14:00:00.000+02:00'}"}
    - plan_event_form
    - form{"name": "plan_event_form"}
    - slot{"place": "unter den linden 6"}
    - slot{"place": "unter den linden 6"}
    - slot{"requested_slot": "event_name"}
* form: plan_event{"event_name": "Das ist ein Test-Event"}
    - slot{"event_name": "Das ist ein Test-Event"}
    - form: plan_event_form
    - slot{"event_name": "Das ist ein Test-Event"}
    - slot{"requested_slot": "is_specific"}
* form: affirm
    - form: plan_event_form
    - slot{"is_specific": "True"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_save_event
    - action_restart
