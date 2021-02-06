# -*- coding: utf-8 -*-
"""
Бот позволяющий:
- вывести случайную цитату из книги Тишина говорит;
- вывести случайное изображение из "9 практик";
- скачать предоставленные на выбор аудиофайлы записей из книги "Практика";
"""
import pickle

from scripts.add_user_to_base import add_new_user
from scripts.logger import configure_logging

import telebot
from scripts.parser_book import random_citate, random_image, list_audio, power_of_now, white_noise
from settings import TOKEN
from telebot import types


bot = telebot.TeleBot(token=TOKEN)
USER_ID = set()


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Тишина говорит - цитаты 📜')
    keyboard.row('ПРАКТИКА - изображения 🎴', 'ПРАКТИКА - аудио 🎵')
    keyboard.row('Аудиокниги 📚')
    keyboard.row('Белый шум 🌫️')
    return keyboard


def book_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('1. Сила момента сейчас')
    keyboard.row('2. Новая земля')
    keyboard.row('⬅️ Назад')
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
    add_new_user(message)


@bot.message_handler(commands=['info'])
def send_info(message):
    markup_inline = types.InlineKeyboardMarkup()  # добавляем клавиатуру
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # добавляем кнопку
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')  # добавляем кнопку
    markup_inline.add(item_yes, item_no)  # добавляем кнопки в клавиатуру

    bot.send_message(
        message.chat.id,
        'Хотите узнать информацию о себе?',
        reply_markup=markup_inline,
    )
    add_new_user(message)


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
    if message.data == 'return_menu':
        bot.send_message(
            chat_id,
            'Вы в главном меню',
            reply_markup=main_keyboard,
        )

    # callback для скачивания аудио из книги Power of Now
    if 'power' in message.data:
        track = message.data.split('_')[3]
        files = power_of_now()
        for file in files:
            if track == file:
                audio = open(file, 'rb')
                bot.send_audio(chat_id,
                               audio,
                               reply_markup=main_keyboard,
                               )

    # callback для скачивания булого шума
    if 'white' in message.data: # todo Что то не скачивает. Нужно проверить
        track = message.data.split('_')[1]
        files = white_noise()
        for file in files:
            if track == file:
                audio = open(file, 'rb')
                bot.send_audio(chat_id,
                               audio,
                               reply_markup=main_keyboard,
                               )

    # callback для инлайна /info
    if message.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_reply.row('Мой ID', 'Мой ник')
        markup_reply.row('⬅️ Назад')
        bot.send_message(
            message.message.chat.id,
            'Нажмите одну из кнопок',
            reply_markup=markup_reply,
        )
    elif message.data == 'no':
        pass


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
    elif message.text == 'Аудиокниги 📚':
        bot.send_message(
            message.chat.id,
            'Выберите интересующую книгу: ',
            reply_markup=book_keyboard()
        )
    elif message.text == '1. Сила момента сейчас':
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
    elif message.text == 'Мой ID':
        bot.send_message(
            message.chat.id,
            f'Ваш ID: {message.from_user.id}',
        )
    elif message.text == 'Мой ник':
        bot.send_message(
            message.chat.id,
            f'Ваш username: {message.from_user.first_name}',
        )
    elif message.text == '⬅️ Назад':
        bot.send_message(
            message.chat.id,
            '⬅️ Назад',
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


def power_of_now_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    files = power_of_now()
    for file in files:
        keyboard.add(types.InlineKeyboardButton(
            text=f'🎵 {file[24:]}',
            callback_data=f'power_of_now_{file}'),
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
    configure_logging()
    bot.polling()
