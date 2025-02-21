import json
import random
from random import randint
import telebot
from telebot import types
from pair_words import PairWords
#from test import init_test_set_pair_words

bot = telebot.TeleBot('6656400001:AAHPefzdqUZkWcCFm18Q7ZpudoBoUEpCfBU')
#клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard.row('Тренировка', 'Подборки') #'Добавить слово', "Удалить слово"
main_keyboard.row('Создать подборку', "FAQ")
#main_keyboard.row('Словарь', "FAQ")
sets_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
sets_keyboard.row('Добавить в подборку', 'Изменить слово', 'Изменить название')
sets_keyboard.row('Удалить подборку', 'Удалить слова', 'Назад')
back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
back_keyboard.row('Назад')
delete_sets_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
delete_sets_keyboard.row('Да', 'Нет')
database = {}#конечный словарь с id пользователей
reverse_dict = {}

def load_from_json(data): #обработка json и вывод словаря
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Load JSON as a list of dictionaries
    return [PairWords.from_dict(item) for item in data]
    #нужно добавить подключение к revers_data_json
    with open(reverse_data, 'r', encoding='utf-8') as file:#добавила 20,02,25 но не факт что правильно
        data = json.load(file)  # Load JSON as a list of dictionaries
        return [PairWords.from_dict(item) for item in data]
def open_database(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data_try = json.load(file)
    for key_id in data_try:
        key_id = int(key_id)
        database[key_id] = []
        for item in data_try[str(key_id)]:
            database[key_id].append(PairWords.from_dict(item))
    return database
    #return [PairWords.from_dict(item) for item in data_try]

set_pair_words = load_from_json('data.json') #init_test_set_pair_words()переделываем под database, чтобы учитывать id пользователя

#dictionary = {'reboot':['перезагружать'], 'source':['источник'], 'compile':['компилировать']}#временный нужно будет полностью перейти на список подборок

open_database('try_data_json.json')
open_database('reverse_data_json.json')# добавила 20,02,25 но не факт что правильно
print(database)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if user_id not in database.keys():
        database[user_id] = load_from_json('data.json')
    bot.send_message(message.from_user.id, 'Добро пожаловать в чат-бот по изучению IT словаря', reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def send_message(message):#обработка кнопок главного меню тренировка, подборки, создать подборку
    try:
        text = message.text.lower()
        if text == 'тренировка':
            if len(database[message.from_user.id]) > 0:#был set_pair_words
                bot.send_message(message.from_user.id, set_selection(message.from_user.id))
                bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
                bot.register_next_step_handler(message, select_set_for_training)
            else:
                bot.send_message(message.from_user.id, 'Список подборок пока пуст, создайте свою первую подборку')
            #print(database)
        elif text == 'подборки':
            #print(database)
            if len(database[message.from_user.id]) > 0:#был set_pair_words
                bot.send_message(message.from_user.id, set_selection(message.from_user.id))
                bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
                bot.register_next_step_handler(message, select_set)
            else:
                bot.send_message(message.from_user.id, 'Список подборок пока пуст, создайте свою первую подборку')
            #print(database)
    #def make_new_set():#создать новую подборку

        elif text == 'создать подборку':
            bot.send_message(message.from_user.id, 'Введите название подборки', reply_markup=back_keyboard)
            bot.register_next_step_handler(message, create_new_set)
        elif text == 'faq':
            bot.send_message(message.from_user.id, 'Если есть вопросы или пожелания можете связаться с администратором @BatSkipper' , reply_markup=main_keyboard)
        elif text == 'database':
            print(database)
    except Exception as e:
        print('Ошибка: ', e)##

def set_selection(user_id):#вывод списка подборок(в скобках было пусто)
    count = 1
    set_selections = 'Список подборок:\n'
    #print(database[user_id])
    for selection in database[user_id]:  # вывод списка подборок (было set_pair_words)
        set_selections += f'{count}. {selection.get_name()}\n'
        # print(f'{count}. {selection.get_name()}')
        count += 1
    return set_selections
def select_set(message):# вывод подборки по выбранному номеру
    number_set = message.text.lower()
    if number_set.isdigit() and 1 <= int(number_set) <= len(database[message.from_user.id]):
        number_set = int(number_set) - 1
        #print(database[message.from_user.id][number_set])#нужно вывести нормальрно подборку и показать новые кнопки для дальнейших действий
        choose_set = f'{database[message.from_user.id][number_set].get_name()}\n'
        count = 1
        for key in database[message.from_user.id][number_set].get_words():#set_pair_words
            choose_set += f'{count}. {key} - {", ".join(database[message.from_user.id][number_set].get_words()[key])}\n'
            count += 1
            if len(choose_set) > 3500:
                bot.send_message(message.from_user.id, choose_set)
                choose_set = ''
        #print(type(choose_set))
        bot.send_message(message.from_user.id, choose_set)
        if len(database[message.from_user.id][number_set].get_words()) > 0: #set_pair_words[number_set]
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=sets_keyboard)
            bot.register_next_step_handler(message, select_action, number_set)
        else:
            #print(choose_set)
            bot.send_message(message.from_user.id, 'Подборка пока еще пуста, выберите действие', reply_markup=sets_keyboard)
            bot.register_next_step_handler(message, select_action, number_set)
        #print(database)
    elif number_set == 'назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, 'Введено не коректное значение', reply_markup=main_keyboard)

def select_action(message, number_set):#обработка работы кнопок добавить в подборку, изменить слово, изменить назваие, удалить подборку, удалить слова, назад
    #raise Exception('Проверка работы try exept')
    text = message.text.lower()
    if text == 'добавить в подборку':
        bot.send_message(message.from_user.id, 'Введите новые слова в формате: "link - ссылка; ссылочка"', reply_markup=back_keyboard)
        bot.register_next_step_handler(message, add_pair_words, number_set)
    elif text == 'изменить слово':
        if len(database[message.from_user.id][number_set].get_words()) == 0:
            bot.send_message(message.from_user.id, 'Подборка пока пустая, выберите, пожалуйста, другое действие', reply_markup=sets_keyboard)
            bot.register_next_step_handler(message, select_action, number_set)
        else:
            bot.send_message(message.from_user.id, 'Введите слово, которое хотите изменить или слово и его перевод, если хотите изменить его значение')
            bot.send_message(message.from_user.id, 'Например: hi - hello или link - ссылка')
            bot.register_next_step_handler(message, change_pair_words, number_set)#переход на следующую функцию которая будет заменять
    elif text == 'изменить название':#изменение название
        bot.send_message(message.from_user.id, 'Введите новое название подборки', reply_markup=back_keyboard)
        bot.register_next_step_handler(message, change_name_set, number_set)
    elif text == 'удалить подборку':
        bot.send_message(message.from_user.id, 'Вы действительно хотите удалить подборку?', reply_markup=delete_sets_keyboard)
        bot.register_next_step_handler(message, delete_set, number_set)
    elif text == 'удалить слова':
        if len(database[message.from_user.id][number_set].get_words()) == 0:
            bot.send_message(message.from_user.id, 'Подборка пока пустая, выберите, пожалуйста, другое действие', reply_markup=sets_keyboard)
            bot.register_next_step_handler(message, select_action, number_set)
        else:
            bot.send_message(message.from_user.id, 'Введите слово, которое хотите удалить, например: link')
            bot.register_next_step_handler(message, del_word, number_set)

    elif text == 'назад':
        bot.send_message(message.from_user.id, set_selection(message.from_user.id))
        bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
        bot.register_next_step_handler(message, select_set)
    else:
        bot.send_message(message.from_user.id, 'Неверный выбор. Попробуйте снова')
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)

def add_pair_words(message, number_set):#функция получения сообщения для добавить в подборки
    words = message.text.lower().replace(' ', ' ')#при добавлении в подбоорку replace работает

    if words == 'назад':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
        return #остановить работу функции
        #bot.send_message(message.from_user.id, set_selection(message.from_user.id)) не туда
        #bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard) не туда
        #bot.register_next_step_handler(message, select_set) не туда
    #дописать разбивку по строкам для массовой загрузки в словарь!!!!
    words_split_line = words.splitlines()
    answer = 'YES'
    not_correct = []
    for line in words_split_line:
        words_split = line.split(' - ')
        words_split_transcript = words_split[1].split('; ')
        if len(words_split) == 2:
            print(database[message.from_user.id][number_set])
            database[message.from_user.id][number_set].add(words_split[0], words_split_transcript)
            save_data(message.from_user.id)
            for key, values in [(words_split[0], words_split_transcript)]:#создаем обратный словарь для проверок одинаковых англ слов
                for value in values:
                    if value not in reverse_dict[message.from_user.id][number_set].words:
                        reverse_dict[message.from_user.id][number_set].words[value] = [key]
                    else:
                        reverse_dict[message.from_user.id][number_set].words[value].append(key)
                    # если нет значения, то он создает его
            print(reverse_dict[message.from_user.id][number_set].words)
        else:
            answer = 'NO'
            not_correct.append(line)
    if answer == 'YES':
        bot.send_message(message.from_user.id, 'Слова добавлены')
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    elif answer == 'NO':
        bot.send_message(message.from_user.id, 'Слова добавлены, за исключением: ')
        bot.send_message(message.from_user.id, '\n'.join(not_correct), reply_markup=main_keyboard)
def change_pair_words(message, number_set):#функция изменить слово
    words = message.text.lower().replace(' ', ' ')
    words_split = words.split(' - ')
    if words == 'назад':
        bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
        bot.register_next_step_handler(message, set_selection(message.from_user.id))
        return #остановить работу функции
    ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    en = 'abcdefghijklmnopqrstuvwxyz' #alphabet = [chr(i) for i in range(97, 123)]
    result = False
    print(words_split)
    print(number_set)
    for i in words_split[-1]:
        if i in en:
            result = database[message.from_user.id][number_set].change(words_split[0], words_split[1], 1)
            save_data(message.from_user.id)
            print('result', result)
            break
        elif i in ru:
            result = database[message.from_user.id][number_set].change(words_split[0], words_split[1], 2)#!!!!!IndexError: list index out of range
            save_data(message.from_user.id)
            break
        else:
            bot.send_message(message.from_user.id, 'Значение не корректно')
            break

    if result:
        save_data(message.from_user.id)
        bot.send_message(message.from_user.id, 'Значение изменено', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    else:
        bot.send_message(message.from_user.id, 'Произошла ошибка', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)


def change_name_set(message, number_set):# смена имени подборки
    name = message.text.replace(' ', ' ')

    if name == 'Назад':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    else:
        database[message.from_user.id][number_set].change_name_set(name)
        bot.send_message(message.from_user.id, 'Название подборки успешно изменено', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    #elif text == 'добавить слово':
    #    bot.send_message(message.from_user.id, 'Введите слово и его перевод в формате: "link ссылка"')
    #    bot.register_next_step_handler(message, get_pair_words)
    #elif text == 'удалить слово':
    #    bot.send_message(message.from_user.id, 'Введите слово, которое хотите удалить')
    #    bot.register_next_step_handler(message, drop_world) # вызов другой функции на ввод данных
    # elif text == "словарь":
    #     bot.send_message(message.from_user.id, 'Полный словарь ниже')
    #     show_dictionary(message)
    # else:
    #     bot.send_message(message.from_user.id, 'Я вас не понял')


# def get_pair_words(message):# добавление в словарь
#     pair = message.text.split()
#     if len(pair) == 2 and ((pair[0] != 'Добавить' and pair[1] != 'слово') or (pair[0] != 'Удалить' and pair[1] != 'слово')):
#         dictionary[pair[0]] = pair[1:]
#         bot.send_message(message.from_user.id, 'Слово добавлено')
#     else:
#         bot.send_message(message.from_user.id, 'Формат ввода должен быть как в примере:"link ссылка"')

#def show_dictionary(message):#вывести словарь
    # all_dict_for_print = ''
    # print(dictionary)
    # for key, value in dictionary.items():
    #     all_dict_for_print += key + ' ' + ', '.join(value) + '\n'
    # print(all_dict_for_print)
    # bot.send_message(message.from_user.id, all_dict_for_print)
    # bot.send_message(message.from_user.id,'Всего слов в словаре: ' + str(len(dictionary)))

# def drop_world(message):#удаление слова
#     word_drop = message.text.lower()
#     if word_drop in dictionary.keys() or word_drop in dictionary.values():
#         dictionary.pop(word_drop)
#         bot.send_message(message.from_user.id, text='Слово удалено из вашего славоря')
#     elif not(word_drop in dictionary.keys() or word_drop in dictionary.values()):
#         bot.send_message(message.from_user.id, text='Такого слова не найдено')
#         pass

def exercise(message, copy_dict, right_answer): #тренировка
    check_answer = message.text.lower()
    print('right_answer', type(right_answer), 'check_answer', type(check_answer))
    print('right_answer', right_answer, 'check_answer', check_answer)
    if check_answer == 'назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
        return
    elif type(right_answer) == str:
        if check_answer == right_answer:
            bot.send_message(message.from_user.id, 'Правильный ответ!')
        else:
            bot.send_message(message.from_user.id, 'В этот раз не повезло. Неправильный ответ!')
            bot.send_message(message.from_user.id, right_answer)
    elif type(right_answer) == list:
        if check_answer in right_answer:
            bot.send_message(message.from_user.id, 'Правильный ответ')
        else:
            bot.send_message(message.from_user.id, 'В этот раз не повезло. Неправильный ответ!')
            bot.send_message(message.from_user.id, right_answer)
    else:
        bot.send_message(message.from_user.id, 'В этот раз не повезло. Неправильный ответ!')
        bot.send_message(message.from_user.id, right_answer)
    print(copy_dict, 'copy dict exercise')
    if len(copy_dict) == 0:
        bot.send_message(message.from_user.id, 'Тренирвока окончена', reply_markup=main_keyboard)
    else:
        rand_tuple = list(copy_dict.items())[randint(0, len(copy_dict) - 1)]
        copy_dict.pop(rand_tuple[0])
        rand = list(rand_tuple)
        random.shuffle(rand)
        print(rand)
        if isinstance(rand[0], list):
            rand[0] = ', '.join(rand[0])
        bot.send_message(message.from_user.id, 'Введите перевод - ' + rand[0])
        bot.register_next_step_handler(message, exercise, copy_dict, rand[1])


def delete_set(message, number_set):#удалить подборку,в которой находится пользователь
    text = message.text.lower()
    if text == 'да':
        database[message.from_user.id].pop(number_set)#set_pair_words
        bot.send_message(message.from_user.id, 'Подборка успешно удалена', reply_markup=main_keyboard)
        bot.send_message(message.from_user.id, set_selection(message.from_user.id))
        bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
        save_data(message.from_user.id)
        bot.register_next_step_handler(message, select_set)
    else:
        bot.send_message(message.from_user.id, 'Подборка не удалена', reply_markup=sets_keyboard)
        bot.send_message(message.from_user.id, 'Вы остались в той же подборке, выберите действие')
        bot.register_next_step_handler(message, select_action, number_set)


def create_new_set(message):#создание новой подборки
    text = message.text.replace(' ', ' ')
    if text.lower() == 'назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
        bot.register_next_step_handler(message, select_action)
    elif len(text) > 0 and text != 'Назад':
        new_pair_words = PairWords(text)
        database[message.from_user.id].append(new_pair_words)
        bot.send_message(message.from_user.id, 'Добавлено успешно', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, len(database[message.from_user.id]) - 1)#номер подборки индекс(длина-1) , был set_pair_words
        save_data(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Название не корректно, вы вернулить в главное меню', reply_markup=main_keyboard)
    print(database)

def del_word(message, number_set):#удаление слов из подборки
    word = message.text.lower()
    result = database[message.from_user.id][number_set].delete(word)#set_pair_words был
    if word == 'назад':
        bot.send_message(message.from_user.id,'Вы вернулись в главное меню', reply_markup=main_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    elif result:
        save_data(message.from_user.id)
        bot.send_message(message.from_user.id, 'Слово удалено', reply_markup=sets_keyboard)
        bot.register_next_step_handler(message, select_action, number_set)
    else:
        bot.send_message(message.from_user.id, 'Слово не найдено')
        bot.register_next_step_handler(message, select_action, number_set)

def select_set_for_training(message):#выбор подборки для тренировки
    number_set = message.text.lower()
    if number_set.isdigit() and 1 <= int(number_set) <= len(database[message.from_user.id]):#был set_pair_words
        number_set = int(number_set) - 1
        dictionary = database[message.from_user.id][number_set].get_words()#set_pair_words был
        copy_dict = dictionary.copy()
        if len(copy_dict) == 0:
            bot.send_message(message.from_user.id, 'Подборка пока пустая')
            bot.send_message(message.from_user.id, set_selection(message.from_user.id))
            bot.send_message(message.from_user.id, 'Введите номер подборки', reply_markup=back_keyboard)
            bot.register_next_step_handler(message, select_set_for_training)
        else:
            bot.send_message(message.from_user.id, 'Сейчас мы начнем тренировать слова, выбранной подборки',
                             reply_markup=back_keyboard)
            print(copy_dict, 'copy dict select set for')
            rand_tuple = list(dictionary.items())[randint(0, len(dictionary) - 1)]
            copy_dict.pop(rand_tuple[0])
            rand = list(rand_tuple)
            print(rand, rand[0])
            random.shuffle(rand)
            print(rand)
            if isinstance(rand[0], list):
                rand[0] = ', '.join(rand[0])
            bot.send_message(message.from_user.id, 'Введите перевод - ' + rand[0])
            bot.register_next_step_handler(message, exercise, copy_dict, rand[1])

    elif number_set == 'назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=main_keyboard)
    else:
        bot.send_message(message.from_user.id, 'Введено не коректное значение', reply_markup=main_keyboard)

def save_data(user_id):#
    print(database)
    database_for_savedata = {}
    for key in database:
        database_for_savedata[key] = [element.to_dict() for element in database[user_id]]
    print(database_for_savedata)
    file_dictionary = open('try_data_json.json', 'w', encoding='utf-8')# создание файла в котором будет храниться подборка
    file_dictionary.write(json.dumps(database_for_savedata, ensure_ascii=False, indent=4))#было in set_pair_words
    file_dictionary.close()



bot.polling(none_stop=True)
#secret amvera 74PnHfyy5E