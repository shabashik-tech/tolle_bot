import random


def random_citate():
    with open('book.txt', 'r') as f:
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