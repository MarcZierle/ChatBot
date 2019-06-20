#!/bin/bash
cd rasa

echo "Generating new RASA model..."
rasa train --fixed-model-name current_model
echo "Done!"
echo ""

cd models

echo "Removing old model and moving the new one into place..."
rm -rf basic_model/*
mv current_model.tar.gz basic_model/
echo "Done!"
echo ""

cd basic_model

echo "Extracting new model and removing archive..."
tar -xvzf current_model.tar.gz
rm current_model.tar.gz
echo "Done!"
echo ""
echo "Finished!"
