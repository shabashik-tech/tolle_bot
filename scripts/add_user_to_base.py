import pickle

from scripts.logger import log


def create_user_id_file(message):
    USER_ID = set()
    with open('scripts/user_id.pickle', 'wb') as file:
        id = message.from_user.id
        pickle.dump(USER_ID, file)


def add_new_user(message):
    # create_user_id_file(message)
    with open('scripts/user_id.pickle', 'rb') as f:
        USER_ID = pickle.load(f)
        print(f'Загрузка данных из файла - {USER_ID}')
        if message.from_user.id not in USER_ID:
            USER_ID.add(message.from_user.id)
            print(f'Пользователь {message.from_user.id} добавлен в сет - {USER_ID}')
            with open('scripts/user_id.pickle', 'ab') as f:
                pickle.dump(USER_ID, f)
                print(f'Загрузка данных в файл - {USER_ID}')
                log.info(f'Пользователь {message.from_user.id} - {message.from_user.first_name}, добавлен в базу.')
                print(f'Пользователь {USER_ID} - {message.from_user.first_name} находится в базе')
                log.info(f'Пользователь {message.from_user.id} - {message.from_user.first_name}, находится в базе.')