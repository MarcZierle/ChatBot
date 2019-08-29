#!/bin/bash
cd ./ChatBot/duckling
../stack/stack exec duckling-example-exe &

cd ../rasa/
../../bin/python -m rasa run actions --actions actions

pkill duckling
