import telebot
from settings import TOKEN
from parser_book import random_citate
import pickle
import logging

bot = telebot.TeleBot(token=TOKEN)
log = logging.getLogger('bot')


def configure_logging():
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M'))
    file_handler.setLevel(logging.INFO)
    log.addHandler(file_handler)


keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Тишина говорит...')


def add_new_user(message):
    with open('user_id.pickle', 'rb') as f:
        users = pickle.load(f)
        if message.from_user.id not in users:
            with open('user_id.pickle', 'wb') as f:
                # сделать ДОПИСЬ в файл, а не переписывание заново
                pickle.dump(message.from_user.id, f)
                log.info(f'Add new user - {message.from_user.first_name}')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = f'~\n' \
             f'Приветствую тебя, {message.from_user.first_name}! \n' \
             f'Внутренняя тишина - твоя сущностная природа. Что есть тишина? Внутреннее пространство или ' \
             f'осознание, благодаря которому воспринимаются читаемые сейчас строки.\n' \
             f'Ты и есть это осознание, принявшее форму личности.\n\n' \
             f'Послушай о чем говорит тишина. Для продолжения нажми кнопку "Тишина говорит..."\n' \
             f'~\n' \
             f'Поддержать автора бота - \nЯндекс-кошелек: 41001865866277,\nСБЕР: 2202 2003 3780 3959'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    add_new_user(message)


@bot.message_handler(content_types=['text'])
def get_citate(message):
    if message.text == 'Тишина говорит...':
        first_word = random_citate()
        bot.send_message(message.chat.id, first_word, reply_markup=keyboard)


# def count_users():
#     with open('user_id.pickle', 'rb') as f:
#         users = pickle.load(f)
#         print(f'Всего пользователей: {len(users)}')


# count_users()
configure_logging()
bot.polling()