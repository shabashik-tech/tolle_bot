import random

def menu():
    print(
        '1. Случайная фраза    2. Вся книга'
        '\n3. Выход'
    )
    user = int(input('Ваш выбор: '))

    if user == 1:
        random_citate()
    elif user == 2:
        book()
    elif user == 3:
        quit()


def random_citate():
    with open('silence.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    print(random.choice(content))
    menu()


def book():
    with open('silence.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    print(content)
    menu()


print('Тишина говорит. Э.Толле')
menu()