#!/usr/bin/env python3

import os
import subprocess
import platform
from yt_dlp import YoutubeDL

def main():
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'downloaded_dfpwm')
    os.makedirs(output_dir, exist_ok=True)

    # Ask for input
    query = input("Enter YouTube URL or song name: ").strip()

    # Configure yt_dlp to download mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # save mp3 here
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'default_search': 'ytsearch1',
    }

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

            # Delete the mp3 after successful conversion
            os.remove(mp3_path)
            print(f"Deleted original mp3: {mp3_path}")

        except subprocess.CalledProcessError as e:
            print("Error during conversion:", e)
        except FileNotFoundError:
            print("FFmpeg not found. Is it installed and in your PATH?")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Download audio
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([query])
            print(f"\nDownload complete! Saved in: {output_dir}")

            # Open the folder in the system file explorer
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_dir])
            else:  # Linux and others
                subprocess.run(["xdg-open", output_dir])

            # Find the mp3 file just downloaded:
            mp3_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.mp3')]
            if not mp3_files:
                print("No mp3 files found to convert.")
            else:
                # Take the most recently modified mp3 file (likely the downloaded one)
                mp3_files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
                newest_mp3 = os.path.join(output_dir, mp3_files[0])
                convert_to_dfpwm(newest_mp3)

        except Exception as e:
            print(f"Error during download: {e}")

if __name__ == '__main__':
    main()
