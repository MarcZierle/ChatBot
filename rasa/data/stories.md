## being polite to the user
* greet
    - utter_greet

## user asks for information about bot
* get_infos
	- utter_infos

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

## remove event from day
* remove_event
    - remove_event_form
    - form{"name":"remove_event_form"}
	- form{"name": null}
	- action_restart

## introducing new users to JANUS
* introduction
    - utter_welcome
    - utter_introduction
    - utter_explain_home_and_interval
    - introduction_form
    - form{"name":"introduction_form"}
	- form{"name": null}
    - utter_introduction_end
	- action_restart

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
