"""Script to download and cache the YAMNet model (no GUI needed)"""
import os
import sys

# Set up cache directory
if getattr(sys, 'frozen', False):
    CACHE_DIR = os.path.join(os.path.dirname(sys.executable), "model_cache")
else:
    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_cache")

os.makedirs(CACHE_DIR, exist_ok=True)
os.environ["TFHUB_CACHE_DIR"] = CACHE_DIR

print(f"Downloading model to: {CACHE_DIR}")

import tensorflow_hub as hub
model = hub.load("https://tfhub.dev/google/yamnet/1")

print("Model downloaded successfully!")
