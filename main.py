# -*- coding: utf-8 -*-
"""
Бот позволяющий:
- вывести случайную цитату из книги Тишина говорит;
- вывести случайное изображение из "9 практик";
- скачать предоставленные на выбор аудиофайлы записей из книги "Практика";
"""
import time

import telebot
from telebot import types

from scripts.work_with_user_id import add_user, read_user_set
from scripts.logger import configure_logging
from scripts.parser_book import random_citate, random_image, list_audio, white_noise
from settings import TOKEN

bot = telebot.TeleBot(token=TOKEN)
USER_ID = set()


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Тишина говорит - цитаты 📜')
    keyboard.row('ПРАКТИКА - изображения 🎴', 'ПРАКТИКА - аудио 🎵')
    keyboard.row('Белый шум 🌫️')
    return keyboard


main_keyboard = main_keyboard()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = f'~\n' \
             f'Приветствую тебя, {message.from_user.first_name}! \n' \
             f'Внутренняя тишина - твоя сущностная природа. Что есть тишина? Внутреннее пространство или ' \
             f'осознание, благодаря которому воспринимаются читаемые сейчас строки.\n' \
             f'Ты и есть это осознание, принявшее форму личности.\n\n' \
             f'Послушай о чем говорит тишина. Для продолжения нажми кнопку "Тишина говорит..."\n' \
             f'~\n'
    bot.send_message(
        message.chat.id,
        answer,
        reply_markup=main_keyboard,
    )
    add_user(message)


@bot.callback_query_handler(func=lambda message: True)
def callback_inlines(message):

    # callback для скачивания аудио
    chat_id = message.message.chat.id
    if 'audio' in message.data:
        track = message.data.split("_")[1]
        files = list_audio()
        for file in files:
            if track == file:
                audio = open(file, 'rb')
                bot.send_audio(chat_id,
                               audio,
                               reply_markup=main_keyboard,
                               )
    # callback для скачивания булого шума
    if 'white' in message.data:
        files = white_noise()
        for file in files:
            if file:
                audio = open(file, 'rb')
                bot.send_audio(chat_id,
                               audio,
                               reply_markup=main_keyboard,
                               )
    if message.data == 'return_menu':
        bot.send_message(
            chat_id,
            'Вы в главном меню',
            reply_markup=main_keyboard,
        )


# анализатор текста :)
@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Тишина говорит - цитаты 📜':
        first_word = random_citate()
        bot.send_message(
            message.chat.id,
            first_word,
            reply_markup=main_keyboard,
        )
    elif message.text == 'ПРАКТИКА - изображения 🎴':
        file = random_image()
        image = open(file, 'rb')
        bot.send_photo(
            message.chat.id,
            image,
            reply_markup=main_keyboard,
        )
    elif message.text == 'ПРАКТИКА - аудио 🎵':
        chat_id = message.chat.id
        text = 'Выберите интересующий файл'
        bot.send_message(
            chat_id, text,
            parse_mode='HTML',
            reply_markup=audio_keyboard(chat_id),
        )
    elif message.text == 'Белый шум 🌫️':
        chat_id = message.chat.id
        text = 'Выберите интересующий файл'
        bot.send_message(
            chat_id, text,
            parse_mode='HTML',
            reply_markup=white_keyboard(chat_id),
        )
    elif message.text == '⬅️ Назад':
        bot.send_message(
            message.chat.id,
            '⬅️ Назад',
            reply_markup=main_keyboard,
        )

    elif message.text == 'Статистика':
        answer = read_user_set()
        bot.send_message(
            message.chat.id,
            text=answer,
            reply_markup=main_keyboard,
        )


# функция для инлайн клавиатуры которая появляется при выборе Аудио: "elif message.text == 'Практика (аудио)...':"
def audio_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    files = list_audio()
    for file in files:
        keyboard.add(types.InlineKeyboardButton(
            text=f'🎵 {file[6:]}',
            callback_data=f'audio_{file}'),
        )
    keyboard.add(types.InlineKeyboardButton(
        text='⬅ Вернуться в меню',
        callback_data='return_menu'),
    )
    return keyboard


def white_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    files = white_noise()
    for file in files:
        keyboard.add(types.InlineKeyboardButton(
            text=f'🎵 {file[18:]}',
            callback_data=f'white_{file}'),
        )
    keyboard.add(types.InlineKeyboardButton(
        text='⬅ Вернуться в меню',
        callback_data='return_menu'),
    )
    return keyboard


if __name__ == '__main__':
    while True:
        try:
            configure_logging()
            bot.polling(none_stop=True)
        except Exception as ex:
            time.sleep(3)
            print(ex)