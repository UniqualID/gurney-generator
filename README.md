SAMPLE DEPLOYMENT HERE: https://gurney-gurney-halleck.fly.dev/

# Gurney Generator 🔊⚔️

> “Mood? What’s mood got to do with it? You fight when the necessity arises... now **_fight!_**”

This is a cursed meme generator that takes the iconic Gurney Halleck line from *Dune* and replaces the word **"fight"** with any word you type — using low-effort TTS for maximum absurdity.

---

## 💡 Features

- Replace **both instances** of “fight” in the clip
- Instant video preview in browser
- Custom TTS voiceovers (Google TTS)
- Minimal frontend, Flask-powered backend
- Deployable to Fly.io

---

## 🖥️ Local Setup

### 🔧 Requirements

- Python 3.10+
- ffmpeg installed (`sudo apt install ffmpeg` or `brew install ffmpeg`)

### ▶️ Run Locally

```bash
pip install -r requirements.txt
python app.py
