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

## slot filling no recognized
* save_event
    - utter_location_not_found
    - action_restart

## fallback story
* out_of_scope
    - action_default_fallback
