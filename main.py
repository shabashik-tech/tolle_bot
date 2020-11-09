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
                pickle.dump(message.from_user.id, f)
                log.info(f'add new user - {message.from_user.first_name}')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = f'Приветствую тебя {message.from_user.first_name}! ' \
             f'Этот бот предназначен для медитации над сутрами книги Экхарта Толле, "Тишина говорит".\n\n' \
             f'Поддержать автора бота - \nЯндекс-кошелек: 41001865866277,\nСБЕР: 2202 2003 3780 3959'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    add_new_user(message)


@bot.message_handler(content_types=['text'])
def get_citate(message):
    if message.text == 'Тишина говорит...':
        first_word = random_citate()
        bot.send_message(message.chat.id, first_word, reply_markup=keyboard)


def count_users():
    with open('user_id.pickle', 'rb') as f:
        users = pickle.load(f)
        print(f'Всего пользователей: {len(users)}')


count_users()
configure_logging()
bot.polling()