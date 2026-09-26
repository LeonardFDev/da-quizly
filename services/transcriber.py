import os
import whisper
import yt_dlp
import uuid
import json
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai.errors import ServerError

from templates.prompt_template import prompt_template


load_dotenv()

ffmpeg_dir = Path("tools").resolve()
os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ["PATH"]

model = whisper.load_model("base") #turbo | base

def download_and_transcribe(url):
    FOLDER = "media/tmpl_audios/"

    random_id = uuid.uuid4().hex[:6]
    tmp_filename = f"{FOLDER}audio_{random_id}.%(ext)s"
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmp_filename,
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError:
        return {"is_audio_download_error": True}


    result = model.transcribe(filename)
    transcribe = (result["text"])


    if os.path.isfile(filename):
        os.remove(filename)

    return ai_create_quiz(transcribe)


def ai_create_quiz(transcribe):
    client = genai.Client()
    tmp_prompt = prompt_template

    try:
        response = client.models.generate_content(model='gemini-3.5-flash-lite', contents= tmp_prompt + transcribe)
        return try_string_to_json(response)   
    except ServerError as e:
        return {"is_ai_error": True, "ai_output_error": e, "transcribe": transcribe}

def try_string_to_json(response):
    try:
        remove_markdown_text = response.text.replace("```json", "").replace("```", "")
        string_to_json = json.loads(remove_markdown_text)
        return string_to_json
    except:
        return {"is_json_error": True, "ai_output": response.text}