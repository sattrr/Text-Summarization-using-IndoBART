from moviepy import *
from pathlib import Path

def extract_audio_from_video(video_path, output_audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(output_audio_path)
        print(f"Audio file saved: {output_audio_path}")
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    VIDEO_DIR = ROOT_DIR / "data" / "video"
    AUDIO_DIR = ROOT_DIR / "data" / "audio"

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    video_files = [f for f in VIDEO_DIR.iterdir() if f.suffix == '.mp4']

    for video_file in video_files:
        audio_file = video_file.stem + '.wav'
        audio_path = AUDIO_DIR / audio_file
        
        extract_audio_from_video(video_file, audio_path)