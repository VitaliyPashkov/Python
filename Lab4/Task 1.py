import os
import argparse
import struct
from mutagen.id3 import ID3, ID3NoHeaderError

# Объявление аргументов командной строки
parser = argparse.ArgumentParser(description='Read ID3v1 tags of all MP3 files in a directory.')
parser.add_argument('directory', type=str, help='Directory containing MP3 files')
parser.add_argument('-d', action='store_true', help='Print 16-bit tag dump')
parser.add_argument('--genre', type=int, help='ID of genre')

# Парсинг аргументов командной строки

arg = [ "C://Users/Phoenix/jupyter/music", "-d","--genre", "4"]
args = parser.parse_args(arg)

# Проверка, что директория существует
if not os.path.isdir(args.directory):
    print(f"{args.directory} is not a valid directory")
    exit()

# Получение списка всех MP3-файлов в директории
mp3_files = [f for f in os.listdir(args.directory) if f.endswith('.mp3')]

# Цикл по всем MP3-файлам
for file in mp3_files:
    path = os.path.join(args.directory, file)
    try:
        # Чтение ID3v1-тега
        id3 = ID3(path)
        artist = id3.get('artist', [''])[0]
        title = id3.get('title', [''])[0]
        album = id3.get('album', [''])[0]

        # Проверка наличия номера трека
        track_number = id3.get('tracknumber', [''])[0]
        if not track_number:
            track_number = '1/1'
            id3.add(id='TRCK', text=track_number)

        # Проверка наличия жанра
        genre_id = id3.get('genre', [None])[0]
        if not genre_id and args.genre is not None:
            id3.add(id='TCON', text=[str(args.genre)])

        # Сохранение изменений в файле
        id3.save()

        # Вывод информации о файле
        print(f'{artist} - {title} - {album}')
        if args.d:
            print(struct.unpack('3s30s30s4s28s1s', id3.file.getvalue()[-128:]))

    except ID3NoHeaderError:
        print(f"No ID3 tag found in {file}")
