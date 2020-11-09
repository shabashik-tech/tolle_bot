import random


def random_citate():
    with open('res_book.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return random.choice(content)