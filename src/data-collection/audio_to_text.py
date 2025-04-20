import whisper
import librosa
import json
from pathlib import Path

def transcribe_audio(audio_path, model):
    try:
        audio, _ = librosa.load(audio_path, sr=16000)
        
        result = model.transcribe(audio)
        print(f"Transcription successful for {audio_path}")
        return result['text']
    except Exception as e:
        print(f"Error transcribing audio {audio_path}: {e}")
        return None

def main():
    ROOT_DIR = Path(__file__).resolve().parents[2]
    AUDIO_DIR = ROOT_DIR / "data" / "audio"
    TEXT_DIR = ROOT_DIR / "data" / "text"
    
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    
    model = whisper.load_model("base")

    audio_files = [f for f in AUDIO_DIR.iterdir() if f.suffix == '.wav']

    transcripts = {}

    for audio_file in audio_files:
        transcription = transcribe_audio(audio_file, model)
        
        if transcription:
            transcripts[audio_file.stem] = transcription

    transcript_file = TEXT_DIR / 'transcripts.json'
    with open(transcript_file, 'w', encoding='utf-8') as f:
        json.dump(transcripts, f, ensure_ascii=False, indent=4)
    print(f"Transcript file saved at: {transcript_file}")

if __name__ == "__main__":
    main()