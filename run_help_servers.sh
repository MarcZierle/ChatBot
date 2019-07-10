#!/bin/bash
cd duckling
../stack/stack exec duckling-example-exe &

cd ../rasa/
rasa run actions --actions actions

pkill duckling
