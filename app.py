from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import subprocess
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Allow frontend fetch() from other ports

# Hardcoded paths and timestamps
VIDEO_PATH = "gurney_clip.mp4"  # Make sure this is trimmed to just the clip
FIGHT_DURATION = 0.6  # Duration of the word "fight", in seconds
FIRST_TIMESTAMP = 3.0  # First "fight"
SECOND_TIMESTAMP = 6.0  # Second "fight"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    word = request.json.get("word", "").strip()
    if not word:
        return "Missing word", 400

    with tempfile.TemporaryDirectory() as tmp:
        # 1. Generate TTS audio
        tts_path = os.path.join(tmp, "tts.mp3")
        tts = gTTS(word)
        tts.save(tts_path)

        # 2. Convert to wav and trim
        tts_audio = AudioSegment.from_file(tts_path)
        tts_audio = tts_audio.set_channels(1).set_frame_rate(44100)
        tts_audio = tts_audio[: FIGHT_DURATION * 1000].fade_out(200)

        # 3. Extract base audio from video
        base_audio_path = os.path.join(tmp, "base_audio.wav")
        out_audio_path = os.path.join(tmp, "new_audio.wav")
        out_video_path = os.path.join(tmp, "out.mp4")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                VIDEO_PATH,
                "-q:a",
                "0",
                "-map",
                "a",
                base_audio_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 4. Build new audio with both replacements
        base_audio = AudioSegment.from_file(base_audio_path)

        pre1 = base_audio[: int(FIRST_TIMESTAMP * 1000)]
        mid = base_audio[
            int((FIRST_TIMESTAMP + FIGHT_DURATION) * 1000) : int(
                SECOND_TIMESTAMP * 1000
            )
        ]
        post = base_audio[int((SECOND_TIMESTAMP + FIGHT_DURATION) * 1000) :]

        final_audio = pre1 + tts_audio + mid + tts_audio + post
        final_audio.export(out_audio_path, format="wav")

        # 5. Combine video + new audio
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                VIDEO_PATH,
                "-i",
                out_audio_path,
                "-c:v",
                "copy",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-shortest",
                out_video_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return send_file(out_video_path, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(debug=True)
