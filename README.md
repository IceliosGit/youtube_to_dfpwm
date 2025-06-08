# 🎵 YouTube to DFPWM Converter

A simple Python script that downloads a song or video from YouTube and converts it to the `.dfpwm` audio format — great for Minecraft mods like ComputerCraft, OpenComputers, or custom audio playback systems.

```bash
ytd [OPTIONS] QUERY [QUERY...]
ytd config [--directory DIR] [--auto-open true|false]
```
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
```bash
python --version
```

### ✅ 2. FFmpeg (4.0 or later)

[Download FFmpeg here](https://ffmpeg.org/download.html) if you don’t already have it.

You can check your version in a terminal or command prompt:
```bash
ffmpeg -version
```

---

## ▶️ How to use

### Install the package  
Run this command to install directly from GitHub:  
```bash
pip install git+https://github.com/IceliosGit/youtube_to_dfpwm.git
```

### Download and convert music into DFPWM  
Use the `ytd` command followed by **one or multiple** song names or YouTube URLs:  
```bash
ytd "song name"
ytd "song name" "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
ytd "https://youtu.be/example" "song name" "another title"
```

### 📂 Output Directory Behavior

By default, downloads are saved in a folder named `downloaded_dfpwm` located next to the script. After a successful conversion, the folder opens automatically unless disabled.

#### 🔧 Change the default download folder
Set a permanent custom output folder:
```bash
ytd config --directory "/your/custom/path"
```

#### 📥 Download to a specific folder (without changing the default)
Override the output folder for a single use:
```bash
ytd "song name" --directory "/temporary/path"
```

#### 🚫 Disable or ✅ enable automatic folder opening
Toggle whether the folder opens after each download:
```bash
ytd config --auto-open false   # Disable
ytd config --auto-open true    # Enable
```
