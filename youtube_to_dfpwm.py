#!/usr/bin/env python3
#allow CLI to find python

import os
import sys
import argparse
import subprocess
import platform
from yt_dlp import YoutubeDL

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.txt") #create a config.txt in the folder where your script is

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

def create_arg_parser():
    parser = argparse.ArgumentParser(
        description="Download YouTube audio and convert to DFPWM"
    )
    
    subparsers = parser.add_subparsers(dest='command', required=False)

    # Default download behavior
    download_parser = subparsers.add_parser('download', help="Download YouTube audio")
    download_parser.add_argument(
        'query',
        nargs='+',
        help='YouTube URL or search keywords'
    )
    download_parser.add_argument(
        '-d', '--directory',
        type=str,
        default=None,
        help='Optional output directory (does NOT change saved default)'
    )

    # Config command to set default directory
    config_parser = subparsers.add_parser('config', help="Set or view default directory")
    config_parser.add_argument(
        '-d', '--directory',
        type=str,
        help='Set a new default output directory'
    )

    return parser

def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    
    # If no arguments at all, show help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.command == 'config':
        if args.directory:
            path = os.path.abspath(args.directory)
            save_output_dir(path)
            print(f"Default directory set to: {path}")
        else:
            current = load_output_dir()
            print(f"Current default directory: {current}")
        return

    # Handle download
    if args.command == 'download' or args.command is None:
        query = ' '.join(args.query)

        if args.directory:
            output_dir = os.path.abspath(args.directory)
        else:
            output_dir = load_output_dir()

        os.makedirs(output_dir, exist_ok=True)

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
