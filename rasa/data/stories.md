## beginning
* greet
    - utter_greet

## simple request for showing the generated plan
* show_plan
    - utter_show_plan
    - action_restart

## TEST: slot filling locations (location recognized)
* save_event{"location": "loc"}
    - action_utter_confirm
    - action_restart

## TEST: slot filling no recognized
* save_event
    - utter_location_not_found
    - action_restart

## TEST: time entity
* get_time{"time": "set"}
    - action_utter_time
    - action_restart

## TEST: duration entity
* get_duration{"duration": "set"}
    - action_utter_duration
    - action_restart

## fallback story
* out_of_scope
    - action_default_fallback
