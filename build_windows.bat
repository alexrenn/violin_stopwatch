@echo off
REM Build for Windows

REM Download the model
python download_model.py

REM Build the app
pyinstaller --onefile --windowed ^
  --name "Violin Stopwatch" ^
  --add-data "yamnet_class_map.csv;." ^
  --add-data "yamnet.tflite;." ^
  microphone.py

echo App built at: dist\Violin Stopwatch.exe
