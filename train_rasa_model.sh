#!/bin/bash
cd rasa
rm models/*.tar.gz

echo "Generating new RASA model..."
rasa train #--data data/ chatito/out/training_samples.json
echo "Done!"
echo ""

cd models

echo "Removing old model and moving the new one into place..."
rm -rf basic_model/*
cp *.tar.gz basic_model/current_model.tar.gz
echo "Done!"
echo ""

cd basic_model

echo "Extracting new model and removing archive..."
tar -xvzf current_model.tar.gz
rm current_model.tar.gz
echo "Done!"
echo ""
echo "Finished!"
