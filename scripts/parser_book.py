import random
import os


def random_citate():
    with open('scripts/book.txt', 'r', encoding='utf-8') as f:
        book_list = []
        content = f.readlines()
        for i in content:
            book_list.append(i.rstrip())
        book_str = ''.join(book_list)
        book_str = book_str.split('~')
        result = []
        for i in book_str:
            if len(i) > 10:
                result.append(i)
        return random.choice(result)


def random_image():
    directory = 'img'
    files = os.listdir(directory)
    random_image_path = random.choice(files)
    path = f'img/{random_image_path}'
    return path


def list_audio():
    list_audio_files = []
    directory = 'audio'
    files = os.listdir(directory)
    for file in files:
        path = f'audio/{file}'
        list_audio_files.append(path)
    return list_audio_files


def power_of_now():
    list_audio_files = []
    directory = 'audio_books/power'
    files = os.listdir(directory)
    for file in files:
        path = f'audio_books/power/{file}'
        list_audio_files.append(path)
    return list_audio_files


def white_noise():
    list_audio_files = []
    directory = 'audio_books/white'
    files = os.listdir(directory)
    for file in files:
        path = f'audio_books/white/{file}'
        list_audio_files.append(path)
    return list_audio_files
