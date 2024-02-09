import telebot
from telebot import types

bot = telebot.TeleBot('6656400001:AAHPefzdqUZkWcCFm18Q7ZpudoBoUEpCfBU')

main_keyboard = types.ReplyKeyboardMarkup()
main_keyboard.row('Тренировка', 'Добавить слово', "Удалить слово", "FAQ")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в чат-бот по изучению IT словаря', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_message(message):
    text = message.text.lower()
    if text == 'тренировка':
        bot.send_message(message.from_user.id,'в разработке')
    elif text == 'добавить слово':
        bot.send_message(message.from_user.id, 'в разработке')
    elif text == 'удалить слово':
        bot.send_message(message.from_user.id, 'в разработке')
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял')

bot.polling(none_stop=True)

