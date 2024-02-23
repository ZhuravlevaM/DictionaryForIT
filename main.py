import random
from random import randint
import telebot
from telebot import types

bot = telebot.TeleBot('6656400001:AAHPefzdqUZkWcCFm18Q7ZpudoBoUEpCfBU')

main_keyboard = types.ReplyKeyboardMarkup()
main_keyboard.row('Тренировка', 'Добавить слово', "Удалить слово")
main_keyboard.row('Словарь', "FAQ")
dictionary = {'reboot':'перезагружать', 'source':'источник', 'compile':'компилировать'}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в чат-бот по изучению IT словаря', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_message(message):
    text = message.text.lower()
    if text == 'тренировка':
        bot.send_message(message.from_user.id,'сейчас мы начнем тренировать слова, имеющиеся в вашем словаре')

        copy_dict = dictionary.copy()
        rand_tuple = list(dictionary.items())[randint(0, len(dictionary) - 1)]
        copy_dict.pop(rand_tuple[0])
        rand = list(rand_tuple)
        random.shuffle(rand)
        bot.send_message(message.from_user.id, 'Введите перевод ' + rand[0])
        bot.register_next_step_handler(message, exercise, copy_dict, rand[1])
    elif text == 'добавить слово':
        bot.send_message(message.from_user.id, 'введите слово и его перевод в формате: "link ссылка"')
        bot.register_next_step_handler(message, get_pair_words)
    elif text == 'удалить слово':
        bot.send_message(message.from_user.id, 'Введите слово, которое хотите удалить')
        bot.register_next_step_handler(message, drop_world) # вызов другой функции на ввод данных
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
    for key, value in dictionary.items():
        all_dict_for_print += key + ' ' + value + '\n'
    print(all_dict_for_print)
    bot.send_message(message.from_user.id, all_dict_for_print)
    bot.send_message(message.from_user.id,'Всего слов в словаре: ' + str(len(dictionary)))

def drop_world(message):
    word_drop = message.text.lower()
    if word_drop in dictionary.keys() or word_drop in dictionary.values():
        dictionary.pop(word_drop)
        bot.send_message(message.from_user.id, text='Слово удалено из вашего славоря')
    else:
        bot.send_message(message.from_user.id, text='Такого слова не найдено')


def exercise(message, copy_dict, right_answer): #тренировка
    check_answer = message.text.lower()
    if check_answer == right_answer:
        bot.send_message(message.from_user.id, 'Правильный ответ!')
    else:
        bot.send_message(message.from_user.id, 'В этот раз не повезло. Неправильный ответ!')

    if len(copy_dict) == 0:
        bot.send_message(message.from_user.id, 'Тренирвока окончена')
    else:
        rand_tuple = list(dictionary.items())[randint(0, len(dictionary) - 1)]
        copy_dict.pop(rand_tuple[0])
        rand = list(rand_tuple)
        random.shuffle(rand)
        bot.send_message(message.from_user.id, 'Введите перевод ' + rand[0])
        bot.register_next_step_handler(message, exercise, copy_dict, rand[1])

bot.polling(none_stop=True)