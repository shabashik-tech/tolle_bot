import telebot
from settings import TOKEN
from tolle_main import random_citate
import pickle

bot = telebot.TeleBot(token=TOKEN)

USERS_ID = set()

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Тишина говорит...')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    USERS_ID.add(message.from_user.id)
    with open('user_id.pickle', 'wb') as f:
        pickle.dump(USERS_ID, f)
    with open('user_id.pickle', 'rb') as f:
        if message.from_user.id in pickle.load(f):
            bot.send_message(message.chat.id, f'Приветствую тебя {message.from_user.first_name}! '
                                              'Этот бот предназначен для медитации '
                                              'над сутрами книги Экхарта Толле, "Тишина говорит".\n\n'
                                              'Поддержать автора бота - \n'
                                              'Яндекс-кошелек: 41001865866277,\n'
                                              'СБЕР: 2202 2003 3780 3959', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_citate(message):
    if message.text == 'Тишина говорит...':
        first_word = random_citate()
        bot.send_message(message.chat.id, first_word, reply_markup=keyboard)


bot.polling()