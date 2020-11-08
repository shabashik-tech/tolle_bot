import telebot
from settings import TOKEN
from tolle_main import random_citate

bot = telebot.TeleBot(token=TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Тишина говорит...')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, random_citate, reply_markup=keyboard)


bot.polling()