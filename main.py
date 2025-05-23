import os
import queue
import threading
import datetime
import sounddevice as sd
import numpy as np
import keyboard
from vosk import Model, KaldiRecognizer
import json
import re

AUDIO_DIR = "audio"
NOTES_DIR = "D:/Obsidian/Professional"
MODEL_PATH = "vosk-model-en-us-0.22"
SAMPLE_RATE = 16000
CHANNELS = 1

# Setup
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(NOTES_DIR, exist_ok=True)
model = Model(MODEL_PATH)

recording = False
q = queue.Queue()
audio_data = []


def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata.copy())


def record_audio():
    global audio_data
    audio_data = []
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', callback=callback):
        while recording:
            audio_data.append(q.get())


def save_wav(filename, data):
    from scipy.io.wavfile import write
    audio_np = np.concatenate(data, axis=0)
    write(filename, SAMPLE_RATE, audio_np)


def basic_formatting(text):
    text = text.strip()
    if not text:
        return "Untitled"
    # Capitalize the first letter of each sentence and fix " i "
    text = re.sub(r'\bi\b', 'I', text)
    text = re.sub(r'(?<=[.!?]) +([a-z])', lambda m: m.group(1).upper(), text.capitalize())
    if not text.endswith('.'):
        text += '.'
    return text


def transcribe_with_vosk(wav_path):
    import wave
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res.get("text", ""))
    final_res = json.loads(rec.FinalResult())
    results.append(final_res.get("text", ""))

    return " ".join([r.strip() for r in results if r.strip()])


def save_transcript(text):
    clean_text = basic_formatting(text)
    title_line = clean_text.split(".")[0].strip()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp} - {title_line[:50].replace('/', '-')}.md"
    with open(os.path.join(NOTES_DIR, filename), "w", encoding="utf-8") as f:
        f.write(clean_text)
    print(f"Saved note: {filename}")


def toggle_recording():
    global recording
    if not recording:
        print("[START] Recording...")
        recording = True
        threading.Thread(target=record_audio).start()
    else:
        print("[STOP] Recording")
        recording = False
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = os.path.join(AUDIO_DIR, f"recording_{now}.wav")
        save_wav(wav_path, audio_data)
        text = transcribe_with_vosk(wav_path)
        save_transcript(text)


print("Press F9 to toggle dictation")
keyboard.add_hotkey("f9", toggle_recording)
keyboard.wait()
