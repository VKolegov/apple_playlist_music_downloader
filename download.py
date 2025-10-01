import os
import pandas as pd
import subprocess
import time
import random
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

BASE_OUTPUT_DIR = "downloads"

def sanitize_filename(s: str) -> str:
    """Убирает недопустимые символы для файловой системы"""
    return "".join(c for c in s if c not in '\\/:*?"<>|').strip()

def add_metadata(filepath: str, title: str, artist: str, album: str = "", genre: str = "", year: str = ""):
    """
    Добавляет метаданные к MP3 файлу
    """
    try:
        try:
            audio = EasyID3(filepath)
        except ID3NoHeaderError:
            # Создаём ID3 тег если его нет
            audio = EasyID3()
            audio.save(filepath)
            audio = EasyID3(filepath)

        if title:
            audio['title'] = title
        if artist:
            audio['artist'] = artist
        if album:
            audio['album'] = album
        if genre:
            audio['genre'] = genre
        if year:
            audio['date'] = year

        audio.save()
        print(f"   📝 Метаданные добавлены")
    except Exception as e:
        print(f"   ⚠️ Ошибка при добавлении метаданных: {e}")

def download_track(title: str, artist: str, output_path: str, album: str = "", genre: str = "", year: str = ""):
    """
    Скачивает трек с YouTube (первый результат поиска) в mp3
    """
    query = f"{title} {artist} audio"
    filename = sanitize_filename(f"{artist} - {title}.mp3")
    filepath = os.path.join(output_path, filename)

    # если уже существует — пропускаем
    if os.path.exists(filepath):
        print(f"⏭ Пропущено (уже есть): {filename}")
        return

    try:
        cmd = [
            "yt-dlp",
            f"ytsearch1:{query}",   # поиск и взять только первый результат
            "-x",                  # извлечь аудио
            "--audio-format", "mp3",
            "-o", filepath,
            "--quiet",             # меньше лишнего текста
            "--no-warnings",
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ {filename}")

        # Добавляем метаданные
        add_metadata(filepath, title, artist, album, genre, year)
    except subprocess.CalledProcessError:
        print(f"❌ Ошибка при загрузке: {query}")

def main():
    # ищем все csv в папке
    csv_files = [f for f in os.listdir(".") if f.lower().endswith(".csv")]
    if not csv_files:
        print("❌ Не найдено .csv файлов в текущей папке.")
        return

    print("Найденные CSV файлы:")
    for i, f in enumerate(csv_files, start=1):
        print(f"{i}. {f}")

    choice = input("Введите номер файла для обработки: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(csv_files):
            print("❌ Неверный выбор")
            return
    except ValueError:
        print("❌ Нужно ввести число")
        return

    input_file = csv_files[idx]
    playlist_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(BASE_OUTPUT_DIR, playlist_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"📂 Работаем с плейлистом: {playlist_name}")

    # читаем CSV
    df = pd.read_csv(input_file, sep=";", encoding="utf-8-sig")

    for _, row in df.iterrows():
        title = str(row.get("Название", "")).strip()
        artist = str(row.get("Артист", "")).strip()
        album = str(row.get("Альбом", "")).strip() if "Альбом" in row and pd.notna(row.get("Альбом")) else ""
        genre = str(row.get("Жанр", "")).strip() if "Жанр" in row and pd.notna(row.get("Жанр")) else ""
        year = str(row.get("Год", "")).strip() if "Год" in row and pd.notna(row.get("Год")) else ""
        if not title:
            continue

        download_track(title, artist, output_dir, album, genre, year)

        # задержка 5-10 секунд
        delay = random.randint(5, 10)
        print(f"⏳ Ждём {delay} секунд перед следующим треком...")
        time.sleep(delay)

if __name__ == "__main__":
    main()

