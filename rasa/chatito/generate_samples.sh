#!/bin/bash
npx chatito main.chatito --format=rasa --outputPath=./out/ --trainingFileName=training_samples.json --testingFileName=testing_samples.json
#mv training_samples.json train
#mv testing_samples.json test
