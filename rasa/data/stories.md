## being polite to the user
* greet
    - utter_greet

<!--------------------------->
<!-- START: EVENT PLANNING -->
<!--------------------------->
## SP_EV: user gives all infos for a specific event
* save_event{"place":"set", "time":"set"}
    - action_set_time_duration_slot
    - utter_ask_event_name
* gives_event_name
    - action_save_specific_event
    - action_restart

## USP_EV: user gives all infos for an unspecific event
* save_event{"place":"set", "duration":"set"}
    - action_set_time_duration_slot
    - utter_ask_event_name
* gives_event_name
    - action_save_unspecific_event
    - action_restart

## SP_EV: user gives place and later time for a specific event
* save_event{"place":"set"}
    - utter_ask_time_known
* affirm
    - utter_ask_time
* gives_time{"time":"set"}
    - action_set_time_duration_slot
    - utter_ask_event_name
* gives_event_name
    - action_save_specific_event
    - action_restart

## SP_EV: user gives time and later place for a specific event
* save_event{"time":"set"}
    - action_set_time_duration_slot
    - utter_ask_place
* gives_place{"place":"set"}
    - utter_ask_event_name
* gives_event_name
    - action_save_specific_event
    - action_restart

## SP_EV: user gives place and later duration for an unspecific event
* save_event{"place":"set"}
    - utter_ask_time_known
* deny
    - utter_ask_duration
* gives_duration{"duration":"set"}
    - action_set_time_duration_slot
    - utter_ask_event_name
* gives_event_name
    - action_save_unspecific_event
    - action_restart

## SP_EV: user gives duration and later place for ab unspecific event
* save_event{"duration":"set"}
    - action_set_time_duration_slot
    - utter_ask_place
* gives_place{"place":"set"}
    - utter_ask_event_name
* gives_event_name
    - action_save_unspecific_event
    - action_restart

## user gives too few infos for planning events
* save_event
    - utter_need_more_infos
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
