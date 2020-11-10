import pickle


def count_users():
    with open('user_id.pickle', 'rb') as f:
        users = pickle.load(f)
        print(users)
        print(f'Всего пользователей: {len(users)}')


count_users()