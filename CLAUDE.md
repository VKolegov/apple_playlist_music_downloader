# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Apple Music playlist downloader that:
1. Sanitizes exported Apple Music playlists (tab-separated `.txt` files) into clean CSV files
2. Downloads tracks from YouTube as MP3 files with metadata

## Architecture

The project consists of two main scripts with a two-stage workflow:

### Stage 1: Playlist Sanitization (`app.py`)
- **Input**: Apple Music playlist export (`.txt` file, tab-separated, UTF-8 or UTF-16)
- **Process**: Extracts specific columns: Название, Артист, Автор, Альбом, Группа, Жанр, Год
- **Output**: Clean CSV file with semicolon separator (`_clean.csv`)

### Stage 2: Track Download (`download.py`)
- **Input**: Sanitized CSV from Stage 1 (semicolon-separated)
- **Process**:
  - Uses `yt-dlp` to search YouTube and download first match as MP3
  - Adds ID3 metadata (title, artist, album, genre, year) using `mutagen`
  - Implements 5-10 second random delays between downloads
  - Skips existing files
- **Output**: MP3 files in `downloads/<playlist_name>/` directory structure

## Commands

### Sanitize Playlist
```bash
python app.py
```
Interactive: prompts to select a `.txt` file from current directory.

### Download Tracks
```bash
python download.py
```
Interactive: prompts to select a CSV file from current directory.

### Dependencies
The project requires:
- `pandas` - CSV/data processing
- `yt-dlp` - YouTube download tool (must be installed separately)
- `mutagen` - MP3 metadata editing

## Key Conventions

- All user-facing messages are in Russian (Cyrillic)
- File encoding: Input files may be UTF-8 or UTF-16; output is UTF-8-sig
- CSV separator for sanitized files: semicolon (`;`)
- Download filenames: `{artist} - {title}.mp3`
- Invalid filename characters are stripped: `\/:*?"<>|`
