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

def download_track(title: str, artist: str, output_path: str, album: str = "", genre: str = "", year: str = "", youtube_url: str = ""):
    """
    Скачивает трек с YouTube в mp3
    Если указан youtube_url, использует прямую ссылку, иначе ищет по запросу

    Возвращает True если файл был скачан, False если был пропущен
    """
    filename = sanitize_filename(f"{artist} - {title}.mp3")
    filepath = os.path.join(output_path, filename)

    # если уже существует — пропускаем
    if os.path.exists(filepath):
        print(f"⏭ Пропущено (уже есть): {filename}")
        return False

    try:
        # Если есть прямая ссылка, используем её
        if youtube_url and youtube_url.strip():
            source = youtube_url.strip()
            print(f"🔗 Загрузка по прямой ссылке: {filename}")
        else:
            # Иначе ищем на YouTube
            query = f"{title} {artist} audio"
            source = f"ytsearch1:{query}"
            print(f"🔍 Поиск и загрузка: {filename}")

        cmd = [
            "yt-dlp",
            source,
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
        return True
    except subprocess.CalledProcessError:
        if youtube_url and youtube_url.strip():
            print(f"❌ Ошибка при загрузке по ссылке: {youtube_url}")
        else:
            print(f"❌ Ошибка при загрузке: {title} {artist}")
        return False

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

    # Нормализуем названия колонок к нижнему регистру
    df.columns = df.columns.str.lower().str.strip()

    for _, row in df.iterrows():
        title = str(row.get("название", "")).strip()
        artist = str(row.get("артист", "")).strip()
        album = str(row.get("альбом", "")).strip() if "альбом" in row and pd.notna(row.get("альбом")) else ""
        genre = str(row.get("жанр", "")).strip() if "жанр" in row and pd.notna(row.get("жанр")) else ""
        year = str(row.get("год", "")).strip() if "год" in row and pd.notna(row.get("год")) else ""
        youtube_url = str(row.get("youtube url", "")).strip() if "youtube url" in row and pd.notna(row.get("youtube url")) else ""
        if not title:
            continue

        was_downloaded = download_track(title, artist, output_dir, album, genre, year, youtube_url)

        # задержка 5-10 секунд только если файл был реально скачан
        if was_downloaded:
            delay = random.randint(5, 10)
            print(f"⏳ Ждём {delay} секунд перед следующим треком...")
            time.sleep(delay)

if __name__ == "__main__":
    main()

