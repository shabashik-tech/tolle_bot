import random
import os


def random_citate():
    with open('book.txt', 'r', encoding='utf-8') as f:
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


def random_audio():
    directory = 'audio'
    files = os.listdir(directory)
    random_audio_path = random.choice(files)
    path = f'audio/{random_audio_path}'
    return path