import time
import threading
import tkinter as tk
import os
import sys

import sounddevice as sd
import numpy as np
import tensorflow_hub as hub
import pandas as pd

# Set up paths for bundled app
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = sys._MEIPASS
    CACHE_DIR = os.path.join(os.path.dirname(sys.executable), "model_cache")
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CACHE_DIR = os.path.join(BASE_DIR, "model_cache")

# Set TensorFlow Hub cache directory
os.environ["TFHUB_CACHE_DIR"] = CACHE_DIR

print("Loading YAMNet model...")
model = hub.load("https://tfhub.dev/google/yamnet/1")
labels = pd.read_csv(os.path.join(BASE_DIR, "yamnet_class_map.csv"))
violin_idx = labels[labels['display_name'] == 'Violin, fiddle'].index[0]
print("Model loaded!")

# Stopwatch state
is_playing = False
start_time = None
total_elapsed = 0.0
running = True


def run_microphone():
    global is_playing, start_time, total_elapsed

    SAMPLE_RATE = 16000
    DURATION = 0.5

    while running:
        try:
            audio = sd.rec(
                int(SAMPLE_RATE * DURATION),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32"
            )
            sd.wait()

            waveform = np.squeeze(audio)
            scores, _, _ = model(waveform)
            mean_scores = scores.numpy().mean(axis=0)
            confidence = mean_scores[violin_idx]

            print(f"Violin confidence: {confidence:.4f}")

            if confidence > 0.001:
                if not is_playing:
                    is_playing = True
                    start_time = time.time()
                    print("▶ Stopwatch started")
            else:
                if is_playing:
                    is_playing = False
                    total_elapsed += time.time() - start_time
                    print("⏸ Stopwatch paused")

        except Exception as e:
            print(f"Audio error: {e}")
            time.sleep(0.1)


def main():
    global running

    root = tk.Tk()
    root.title("Violin Stopwatch")

    time_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
    time_label.pack(pady=20)

    status_label = tk.Label(root, text="Waiting...", font=("Helvetica", 16))
    status_label.pack(pady=10)

    def reset():
        global total_elapsed, start_time
        total_elapsed = 0.0
        if is_playing:
            start_time = time.time()
        
    reset_btn = tk.Button(root, text="Reset", font=("Helvetica", 14), command=reset)
    reset_btn.pack(pady=10)

    def update_time():
        if is_playing:
            current_elapsed = total_elapsed + (time.time() - start_time)
            status_label.config(text="🎻 Playing!", fg="green")
        else:
            current_elapsed = total_elapsed
            status_label.config(text="Waiting...", fg="gray")
        
        mins, secs = divmod(int(current_elapsed), 60)
        time_label.config(text=f"{mins:02d}:{secs:02d}")
        root.after(100, update_time)

    def on_close():
        global running
        running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start audio thread
    audio_thread = threading.Thread(target=run_microphone, daemon=True)
    audio_thread.start()

    update_time()
    root.mainloop()


if __name__ == "__main__":
    main()
