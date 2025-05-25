from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil, uuid, json
import whisper
from app.services.speech_to_text import transcribe_audio, convert_to_wav
from app.services.video_audio_converter import extract_audio_from_video
from app.services.summarizer import summarize_text

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
TEXT_DIR = Path("data/text")
TEMP_DIR = Path("data/temp")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_AUDIO_VIDEO_TYPES = {".mp3", ".wav", ".aac", ".m4a", ".mp4", ".mkv", ".mov"}
VIDEO_TYPES = {".mp4", ".mkv", ".mov"}

model = whisper.load_model('base')

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

    if audio_path.suffix.lower() != '.wav':
        wav_path = TEMP_DIR / f"{uid}.wav"
        converted_path = convert_to_wav(audio_path, wav_path)
        if not converted_path:
            raise HTTPException(status_code=500, detail="Audio conversion failed")
        audio_path = converted_path

    transcription = transcribe_audio(audio_path, model)
    if transcription is None:
        raise HTTPException(status_code=500, detail="Transcription failed")

    summary = summarize_text(transcription)

    transcript_file = TEXT_DIR / f'transcript_{uid}.json'
    with open(transcript_file, 'w', encoding='utf-8') as f:
        json.dump({"summary": summary}, f, ensure_ascii=False, indent=4)

    return {"summary": summary}

@router.get("/transcribe/latest")
def get_latest_transcription():
    transcript_files = sorted(
        [f for f in TEXT_DIR.iterdir() if f.name.startswith("transcript_") and f.suffix == ".json"],
        key=os.path.getmtime,
        reverse=True
    )
    if not transcript_files:
        raise HTTPException(status_code=404, detail="No transcription found")

    latest_file = transcript_files[0]
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {"text": data.get("text", "")}