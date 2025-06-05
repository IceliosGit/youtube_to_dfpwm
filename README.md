# 🎵 YouTube to DFPWM Converter

A simple Python script that downloads a song or video from YouTube and converts it to the `.dfpwm` audio format — great for Minecraft mods like ComputerCraft, OpenComputers, or custom audio playback systems.

---

## 📦 Features

- Accepts a YouTube URL or search term
- Downloads the audio as an `.mp3`
- Converts it to `.dfpwm` using `ffmpeg`
- Automatically deletes the `.mp3` after conversion

---

## 🖥️ Requirements

Before running the script, you need:

### ✅ 1. Python (3.7 or later)

[Download Python here](https://www.python.org/downloads/) if you don’t already have it.

You can check your version in a terminal or command prompt:
python --version

### ✅ 2. FFmpeg (4.0 or later)

[Download FFmpeg here](https://ffmpeg.org/download.html) if you don’t already have it.

You can check your version in a terminal or command prompt:
ffmpeg -version

### ✅ 3. Python dependencies

Before running the script, install the required Python packages (yt-dlp):
pip install -r requirements.txt

You can check your version in a terminal or command prompt:
yt-dlp --version

## ▶️ How to use
1. Open your terminal or command prompt.
2. Install the package by running:
pip install git+https://github.com/IceliosGit/youtube_to_dfpwm.git
3. Run the program with the command:
youtube-to-dfpwm
4. When prompted, enter the YouTube URL, song name, or video title.
5. The program will download the audio, convert it to DFPWM format, and then open the folder containing the downloaded files.






