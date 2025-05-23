# app/services/video_audio_converter.py
from moviepy import *
from pathlib import Path

def extract_audio_from_video(video_path: Path, output_audio_path: Path) -> bool:
    try:
        video = VideoFileClip(str(video_path))
        audio = video.audio
        audio.write_audiofile(str(output_audio_path))
        print(f"Audio extracted: {output_audio_path}")
        return True
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
        return False