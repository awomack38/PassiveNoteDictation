# 🎙️ Obsidian Dictation Logger

A simple Python script to dictate notes throughout your day using a hotkey. It records your voice, transcribes it locally using Vosk, and saves the output directly into your Obsidian vault.

---

## 🚀 Features

- Hotkey toggle (default: `F9`) to start/stop voice recording
- Local transcription using [Vosk](https://alphacephei.com/vosk/)
- Saves each note as a Markdown file using the first sentence as the title
- Fully offline, no API required
- Designed for quick note capture while working

---

## ⚙️ Requirements

- **Python 3.10**
- Vosk model

---
## Vosk

- Download your model of choice here: https://alphacephei.com/vosk/models
- Extract the folder to your project directory alongside main/requirements
- Update MODEL_PATH to your chosen model (default is vosk-model-en-us-0.22)

## Obsidian

- Point NOTES_DIR to where you want your notes to go after transcription

## Other

- Change the hotkey utilized (or combination) at keyboard.add_hotkey()
