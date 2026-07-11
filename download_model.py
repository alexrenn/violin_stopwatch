"""Script to download the YAMNet TFLite model"""
import os
import urllib.request

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yamnet.tflite")
MODEL_URL = "https://www.kaggle.com/api/v1/models/google/yamnet/tfLite/classification-tflite/1/download"

if not os.path.exists(MODEL_PATH):
    print(f"Downloading model to: {MODEL_PATH}")
    # Add headers to avoid 403
    request = urllib.request.Request(MODEL_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request) as response:
        with open(MODEL_PATH, 'wb') as f:
            f.write(response.read())
    print("Model downloaded successfully!")
else:
    print("Model already exists.")
