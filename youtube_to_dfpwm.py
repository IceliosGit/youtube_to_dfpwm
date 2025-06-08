#!/usr/bin/env python3
#allow CLI to find python

import os
import sys
import argparse
import subprocess
import platform
from yt_dlp import YoutubeDL

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.txt") #create a config.txt in the folder where your script is

def load_config():
    config = {
        "directory": os.path.join(os.path.dirname(__file__), 'downloaded_dfpwm'),
        "auto_open": "true"
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                key, _, value = line.partition("=")
                if key and value:
                    config[key.strip()] = value.strip()
    return config

def save_config(directory=None, auto_open=None):
    config = load_config()
    if directory is not None:
        config["directory"] = directory.strip()
    if auto_open is not None:
        config["auto_open"] = auto_open.strip().lower()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

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

    config_parser.add_argument(
    '-a', '--auto-open',
    choices=['true', 'false'],
    help='Enable (true) or disable (false) automatic folder opening after download'
)

    return parser

def main():
    parser = create_arg_parser()

    # If no arguments at all, show help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # If first arg is not a known subcommand, treat as download
    if sys.argv[1] not in ('download', 'config'):
        sys.argv.insert(1, 'download')

    args = parser.parse_args()

    if args.command == 'config':
        if args.directory or args.auto_open:
            save_config(directory=args.directory, auto_open=args.auto_open)
            print("Configuration updated:")
            if args.directory:
                print(f"- Default directory set to: {os.path.abspath(args.directory)}")
            if args.auto_open:
                print(f"- Auto-open after download: {args.auto_open}")
        else:
            config = load_config()
            print(f"Current default directory: {config['directory']}")
            print(f"Auto-open after download: {config['auto_open']}")
        return

    if args.command == 'download' or args.command is None:
        queries = args.query  # list of queries/URLs

        config = load_config()
        output_dir = os.path.abspath(args.directory) if args.directory else config["directory"]

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
            'default_search': 'ytsearch',
        }

        with YoutubeDL(ydl_opts) as ydl:
            for query in queries:
                try:
                    if not query.startswith(("http://", "https://", "ytsearch:", "ytsearch1:")):
                        query = f"ytsearch:{query}"
                    ydl.download([query])
                    print(f"\nDownload complete! Saved in: {output_dir}")

                    # Convert newest mp3 after each download
                    mp3_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.mp3')]
                    if not mp3_files:
                        print("No mp3 files found to convert.")
                    else:
                        mp3_files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
                        newest_mp3 = os.path.join(output_dir, mp3_files[0])
                        convert_to_dfpwm(newest_mp3)

                except Exception as e:
                    print(f"Error during download of '{query}': {e}")

        if config.get("auto_open", "true") == "true":
            open_folder(output_dir)



if __name__ == '__main__':
    main()
