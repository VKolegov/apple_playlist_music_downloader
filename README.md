# Apple Music Playlist Downloader

A two-stage tool for downloading Apple Music playlists from YouTube with proper metadata.

## Overview

This project helps you download your Apple Music playlists as MP3 files with full metadata. It works in two stages:

1. **Sanitize** - Cleans exported Apple Music playlist files into a standardized CSV format
2. **Download** - Downloads tracks from YouTube and adds ID3 metadata tags

## Requirements

- Python 3.x
- Dependencies (install via `pip install -r requirements.txt`):
  - `pandas` - Data processing
  - `mutagen` - MP3 metadata editing
- **yt-dlp** - YouTube downloader (install separately: `pip install yt-dlp`)

## Installation

```bash
pip install -r requirements.txt
pip install yt-dlp
```

## Usage

### Stage 1: Sanitize Playlist Export

Export your playlist from Apple Music as a `.txt` file, then run:

```bash
python app.py
```

The script will:
- Show all `.txt` files in the current directory
- Prompt you to select a file
- Extract columns: Title, Artist, Author, Album, Band, Genre, Year
- Create a clean CSV file with `_clean.csv` suffix

**Supported formats**: UTF-8 or UTF-16 encoded tab-separated text files

### Stage 2: Download Tracks

```bash
python download.py
```

The script will:
- Show all CSV files in the current directory
- Prompt you to select a sanitized playlist file
- Create `downloads/<playlist_name>/` directory
- Download each track from YouTube as MP3
- Add ID3 metadata (title, artist, album, genre, year)
- Skip already downloaded files
- Use random 5-10 second delays between downloads

**Output format**: `Artist - Title.mp3`

## Project Structure

```
.
├── app.py              # Stage 1: Playlist sanitization
├── download.py         # Stage 2: Track downloading
├── requirements.txt    # Python dependencies
├── downloads/          # Downloaded MP3 files (created automatically)
│   └── <playlist_name>/
└── *.txt              # Your Apple Music exports
```

## Features

- Handles UTF-8 and UTF-16 encoded playlist files
- Sanitizes filenames (removes invalid characters: `\/:*?"<>|`)
- Preserves full metadata: title, artist, album, genre, year
- Skips already downloaded tracks
- Rate limiting with random delays (5-10 seconds)
- Downloads first YouTube search result per track

## Notes

- User interface messages are in Russian
- CSV files use semicolon (`;`) as separator
- Output encoding is UTF-8 with BOM (UTF-8-sig)

## License

This project is for personal use. Respect copyright laws when downloading music.
