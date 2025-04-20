import os
import yt_dlp
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data" / "video"
DATA_DIR.mkdir(exist_ok=True)

def download_tiktok_video(url: str) -> str:
    try:
        ydl_opts = {
            'outtmpl': str(DATA_DIR / '%(id)s.%(ext)s'),
            'format': 'mp4',
            'cookiefile': str(ROOT_DIR / "cookies.txt"),
            'verbose': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading TikTok Video...")
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            print(f"Video saved as: {filename}")
            return filename
    except Exception as e:
        print("Gagal mengunduh video:", e)
        return None

def upload_local_video(file_path: str) -> str:
    filename = os.path.basename(file_path)
    dest_path = DATA_DIR / filename
    shutil.copy(file_path, dest_path)
    print("Local video copied to: {dest_path}")
    return str(dest_path)

def main():
    print("=== TikTok Video Loader ===")
    print("1. Paste link from TikTok")
    print("2. Upload video from local")
    choice = input("Select option (1/2): ")

    if choice == "1":
        url = input("Paste TikTok URL video: ")
        video_path = download_tiktok_video(url)
    elif choice == "2":
        file_path = input("Upload file path: ")
        if not Path(file_path).exists():
            print("File not found")
            return
        video_path = upload_local_video(file_path)
    else:
        print("Input not valid")
        return
    
    print(f"\n Video saved at: {video_path}")

if __name__ == "__main__":
    main()