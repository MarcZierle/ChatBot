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

## remove event from day
* remove_event
    - remove_event_form
    - form{"name":"remove_event_form"}
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
