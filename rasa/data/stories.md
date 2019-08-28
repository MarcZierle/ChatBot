## being polite to the user
* greet
    - utter_greet

<!--------------------------->
<!-- START: EVENT PLANNING -->
<!--------------------------->
## FromActions Test
* plan_event
	- plan_event_form
	- form{"name": "plan_event_form"}
	- form{"name": null}
	- action_save_event
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
