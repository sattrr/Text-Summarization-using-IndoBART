import shutil
import uuid
import json
import whisper
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from app.services.video_audio_converter import extract_audio_from_video
from app.services.speech_to_text import transcribe_audio

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
TEXT_DIR = Path("data/text")
    
TEXT_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_AUDIO_VIDEO_TYPES = {".mp3", ".wav", ".aac", ".m4a", ".mp4", ".mkv", ".mov"}
VIDEO_TYPES = {".mp4", ".mkv", ".mov"}

model = whisper.load_model("base")

@router.post("/transcribe")
async def transcribe_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_AUDIO_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    uid = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{uid}{ext}"
    with input_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if ext in VIDEO_TYPES:
        audio_path = UPLOAD_DIR / f"{uid}.wav"
        success = extract_audio_from_video(input_path, audio_path)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to extract audio from video")
    else:
        audio_path = input_path

    transcription = transcribe_audio(audio_path, model)
    if transcription is None:
        raise HTTPException(status_code=500, detail="Transcription failed")

    return {"text": transcription}

@router.get("/transcribe/latest")
def get_latest_transcription():
    transcript_file = TEXT_DIR / 'transcripts.json'
    if not transcript_file.exists():
        raise HTTPException(status_code=404, detail="Transcript file not found")

    with open(transcript_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {"text": data}