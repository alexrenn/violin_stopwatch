#!/bin/bash
# Build for macOS

# Download the model
python3 download_model.py

# Build the app
pyinstaller --onefile --windowed \
  --name "Violin Stopwatch" \
  --add-data "yamnet_class_map.csv:." \
  --add-data "yamnet.tflite:." \
  microphone.py

echo "App built at: dist/Violin Stopwatch.app"
