import os
import pandas as pd

# нужные колонки
KEEP_COLUMNS = ["Название", "Артист", "Автор", "Альбом", "Группа", "Жанр", "Год"]

def sanitize_playlist(input_file, output_file):
    # пробуем сначала UTF-8, потом UTF-16
    try:
        df = pd.read_csv(input_file, sep="\t", encoding="utf-8", dtype=str)
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, sep="\t", encoding="utf-16", dtype=str)

    # оставляем только нужные столбцы
    keep = [col for col in KEEP_COLUMNS if col in df.columns]
    clean_df = df[keep]

    # добавляем пустую колонку для YouTube URL (можно заполнить вручную)
    clean_df["YouTube URL"] = ""

    # сохраняем в CSV с ; как разделителем
    clean_df.to_csv(output_file, sep=";", index=False, encoding="utf-8-sig")
    print(f"✅ Санитизированный плейлист сохранён в {output_file}")
    print(f"💡 Вы можете добавить прямые ссылки YouTube в колонку 'YouTube URL' для нужных треков")

def main():
    # ищем все .txt в текущей папке
    txt_files = [f for f in os.listdir(".") if f.lower().endswith(".txt")]
    if not txt_files:
        print("❌ Не найдено .txt файлов в текущей папке.")
        return

    print("Найденные файлы:")
    for i, f in enumerate(txt_files, start=1):
        print(f"{i}. {f}")

    choice = input("Введите номер файла для обработки: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(txt_files):
            print("❌ Неверный выбор")
            return
    except ValueError:
        print("❌ Нужно ввести число")
        return

    input_file = txt_files[idx]
    output_file = os.path.splitext(input_file)[0] + "_clean.csv"
    sanitize_playlist(input_file, output_file)

if __name__ == "__main__":
    main()

