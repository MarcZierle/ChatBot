## beginning
* greet
    - utter_greet
    - utter_ask
> check_ask

## action ok
> check_ask
* affirm
    - action_python_test
    - utter_end
> check_end

## action nope
> check_ask
* deny
    - utter_end
> check_end

## end conversation
> check_end
* goodbye
    - utter_goodbye
    - action_restart
