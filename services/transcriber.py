import os
import whisper
import yt_dlp
import uuid
import json
import shutil
import imageio_ffmpeg

from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai.errors import ServerError

from templates.prompt_template import prompt_template


load_dotenv()
model = whisper.load_model("base") #turbo | base


def customized_ffmpeg_exe():
    ORIGINAL_FFMPEG_EXE = Path(imageio_ffmpeg.get_ffmpeg_exe())
    KOPIE_OF_ORIGINAL_FFMPEG_EXE = Path("tools/ffmpeg.exe")

    if not KOPIE_OF_ORIGINAL_FFMPEG_EXE.exists():
        KOPIE_OF_ORIGINAL_FFMPEG_EXE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ORIGINAL_FFMPEG_EXE, KOPIE_OF_ORIGINAL_FFMPEG_EXE)

    ffmpeg_dir = Path("tools").resolve()
    os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ["PATH"]


def download_and_transcribe(url):
    customized_ffmpeg_exe()
    download_audio_output = download_audio(url)

    if download_audio_output.get("is_audio_download_error") == True:
        return download_audio_output

    result = model.transcribe(download_audio_output.get("filename"))
    transcribe = (result["text"])
    
    if os.path.isfile(download_audio_output.get("filename")):
        os.remove(download_audio_output.get("filename"))

    return ai_create_quiz(transcribe)


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temporary_audio_file_create(),
        "quiet": True,
        "noplaylist": True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {"is_audio_download_error": False, "filename": ydl.prepare_filename(info)}
    except yt_dlp.utils.DownloadError:
        return {"is_audio_download_error": True}


def temporary_audio_file_create():
    FOLDER = "media/tmpl_audios/"
    
    random_id = uuid.uuid4().hex[:6]
    tmp_filename = f"{FOLDER}audio_{random_id}.%(ext)s"

    return tmp_filename


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