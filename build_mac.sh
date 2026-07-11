#!/bin/bash
# Build for macOS

# First run the app once to download the model
python3 microphone.py &
PID=$!
sleep 30
kill $PID 2>/dev/null

# Build the app
pyinstaller --onefile --windowed \
  --name "Violin Stopwatch" \
  --add-data "yamnet_class_map.csv:." \
  --add-data "model_cache:model_cache" \
  --icon "icon.icns" \
  microphone.py

echo "App built at: dist/Violin Stopwatch.app"
