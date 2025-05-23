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
    AUDIO_DIR = Path("data/uploads")
    TEXT_DIR = Path("data/text")

    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    model = whisper.load_model("base")

    allowed_exts = ('.wav', '.mp3', '.aac', '.m4a')

    audio_files = [f for f in AUDIO_DIR.iterdir() if f.suffix.lower() in allowed_exts]

    for audio_file in audio_files:
        transcription = transcribe_audio(audio_file, model)

        if transcription:
            transcript_data = {"text": transcription}
            transcript_file = TEXT_DIR / f'transcript_{audio_file.stem}.json'

            try:
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    json.dump(transcript_data, f, ensure_ascii=False, indent=4)
                print(f"Transcript file saved at: {transcript_file}")
            except Exception as e:
                print(f"Error saving transcript for {audio_file.name}: {e}")
        else:
            print(f"No transcription for {audio_file.name}")

if __name__ == "__main__":
    main()