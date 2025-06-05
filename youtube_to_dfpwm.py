#!/usr/bin/env python3

import os
import sys
import subprocess
import platform
from yt_dlp import YoutubeDL

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.txt")

def load_output_dir():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            path = f.read().strip()
            if path:
                return path
    return os.path.join(os.path.dirname(__file__), 'downloaded_dfpwm')

def save_output_dir(path):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(path.strip())

def open_folder(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux and others
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"Could not open folder automatically: {e}")

def convert_to_dfpwm(mp3_path):
    output_file = os.path.splitext(mp3_path)[0] + '.dfpwm'
    command = [
        "ffmpeg",
        "-i", mp3_path,
        "-ar", "48000",
        "-ac", "1",
        "-c:a", "dfpwm",
        output_file
    ]
    try:
        print(f"Converting {mp3_path} to {output_file}...")
        subprocess.run(command, check=True)
        print("Conversion complete!")
        os.remove(mp3_path)
        print(f"Deleted original mp3: {mp3_path}")
    except subprocess.CalledProcessError as e:
        print("Error during conversion:", e)
    except FileNotFoundError:
        print("FFmpeg not found. Is it installed and in your PATH?")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    # Check command-line arguments
    args = sys.argv[1:]

    if not args:
        query = input("Enter YouTube URL or song name: ").strip()
    else:
        query = args[0]

    # Use custom path if provided
    if len(args) > 1:
        output_dir = os.path.abspath(args[1])
        save_output_dir(output_dir)  # Save the new path to config
    else:
        output_dir = load_output_dir()

    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'default_search': 'ytsearch1',
    }

    # Download and convert
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([query])
            print(f"\nDownload complete! Saved in: {output_dir}")
            open_folder(output_dir)

            mp3_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.mp3')]
            if not mp3_files:
                print("No mp3 files found to convert.")
            else:
                mp3_files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
                newest_mp3 = os.path.join(output_dir, mp3_files[0])
                convert_to_dfpwm(newest_mp3)

        except Exception as e:
            print(f"Error during download: {e}")

if __name__ == '__main__':
    main()
