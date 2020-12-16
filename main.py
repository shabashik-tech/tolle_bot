# -*- coding: utf-8 -*-

import telebot
from settings import TOKEN
from parser_book import random_citate
import pickle
from logger import log, configure_logging


bot = telebot.TeleBot(token=TOKEN)
USER_ID = set()

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Тишина говорит...')


def add_new_user(message):
    with open('user_id.pickle', 'rb') as f:
        USER_ID = pickle.load(f)
        print(f'Загрузка данных из файла - {USER_ID}')
        if message.from_user.id not in USER_ID:
            USER_ID.add(message.from_user.id)
            print(f'Пользователь {message.from_user.id} добавлен в сет - {USER_ID}')
            with open('user_id.pickle', 'ab') as f:
                pickle.dump(USER_ID, f)
                print(f'Загрузка данных в файл - {USER_ID}')
                log.info(f'Пользователь {message.from_user.id} - {message.from_user.first_name}, добавлен в базу.')
                print(f'Пользователь {USER_ID} находится в базе')
                log.info(f'Пользователь {message.from_user.id} - {message.from_user.first_name}, находится в базе.')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = f'~\n' \
             f'Приветствую тебя, {message.from_user.first_name}! \n' \
             f'Внутренняя тишина - твоя сущностная природа. Что есть тишина? Внутреннее пространство или ' \
             f'осознание, благодаря которому воспринимаются читаемые сейчас строки.\n' \
             f'Ты и есть это осознание, принявшее форму личности.\n\n' \
             f'Послушай о чем говорит тишина. Для продолжения нажми кнопку "Тишина говорит..."\n' \
             f'~\n' \
             # f'Поддержать автора бота - \nЯндекс-кошелек: 41001865866277,\nСБЕР: 2202 2003 3780 3959'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    add_new_user(message)


@bot.message_handler(content_types=['text'])
def get_citate(message):
    if message.text == 'Тишина говорит...':
        first_word = random_citate()
        bot.send_message(message.chat.id, first_word, reply_markup=keyboard)

configure_logging()
bot.polling()