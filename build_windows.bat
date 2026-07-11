@echo off
REM Build for Windows

REM First run the app once to download the model
echo Downloading model (wait ~30 seconds)...
start /B python microphone.py
timeout /t 30 /nobreak
taskkill /IM python.exe /F 2>nul

REM Build the app
pyinstaller --onefile --windowed ^
  --name "Violin Stopwatch" ^
  --add-data "yamnet_class_map.csv;." ^
  --add-data "model_cache;model_cache" ^
  --icon "icon.ico" ^
  microphone.py

echo App built at: dist\Violin Stopwatch.exe
