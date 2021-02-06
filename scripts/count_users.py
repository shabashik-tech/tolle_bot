import pickle


def count_users():
    with open('scripts/user_id.pickle', 'rb') as f:
        users = pickle.load(f)
        print(users)
        print(f'Всего пользователей: {len(users)}')


count_users()