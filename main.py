import telebot
from telebot import types

bot = telebot.TeleBot('6656400001:AAHPefzdqUZkWcCFm18Q7ZpudoBoUEpCfBU')

main_keyboard = types.ReplyKeyboardMarkup()
main_keyboard.row('Тренировка', 'Добавить слово', "Удалить слово")
main_keyboard.row('Словарь', "FAQ")
dictionary = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в чат-бот по изучению IT словаря', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_message(message):
    text = message.text.lower()
    if text == 'тренировка':
        bot.send_message(message.from_user.id,'сейчас мы начнем тренировать слова, имеющиеся в вашем словаре')
    elif text == 'добавить слово':
        bot.send_message(message.from_user.id, 'введите слово и его перевод в формате: "link ссылка"')
        bot.register_next_step_handler(message, get_pair_words)
    elif text == 'удалить слово':
        bot.send_message(message.from_user.id, 'слово удалено из вашего славоря')
    elif text == "словарь":
        bot.send_message(message.from_user.id, 'полный словарь ниже')
        show_dictionary(message)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял')


def get_pair_words(message):
    pair = message.text.split()
    if len(pair) == 2:
        dictionary[pair[0]] = pair[1]
        bot.send_message(message.from_user.id, 'Слово добавлено')
    else:
        bot.send_message(message.from_user.id, 'Формат ввода должен быть как в примере:"link ссылка"')

def show_dictionary(message):
    all_dict_for_print = ''
    for key, value in dictionary:
        all_dict_for_print += key + ' ' + value + '\n'
    bot.send_message(message.from_user.id, all_dict_for_print)
    bot.send_message(message.from_user.id,'Всего слов в словаре: ' + str(len(all_dict_for_print)))

bot.polling(none_stop=True)