import os
from pathlib import Path
import whisper
import yt_dlp
import uuid
from google import genai

from templates.prompt_template import prompt_template


ffmpeg_dir = Path("tools").resolve()
os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ["PATH"]

model = whisper.load_model("base")

def download_and_transcribe(url = "https://www.youtube.com/watch?v=YE7VzlLtp-4"):
    FOLDER = "media/tmpl_audios/"

    random_id = uuid.uuid4().hex[:6]
    tmp_filename = f"{FOLDER}audio_{random_id}.%(ext)s"
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmp_filename,
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    result = model.transcribe(filename)
    transcribe = (result["text"])


    if os.path.isfile(filename):
        os.remove(filename)

    