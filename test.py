import json
from pair_words import PairWords

database = {}
def open_database(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data_try = json.load(file)
    for key_id in data_try:
        key_id = int(key_id)
        database[key_id] = []
        for item in data_try[str(key_id)]:
            database[key_id].append(PairWords.from_dict(item))
    return database

open_database('data.json')

d = {'hi': ['привет', 'здравствуйте'], 'hello': ['привет', 'здравствуйте']}


# Создаем обратный словарь
reverse_d = database.copy()
#print(reverse_d)
for user_id in database:
    for i in range(len(database[user_id])):
        set_words = database[user_id][i].words
        #print(reverse_d[user_id][i].words)
        reverse_d[user_id][i].words = {} #очистить данные в копии перед добавлением
        for key, values in list(set_words.items()):
            for value in values:
                if value not in reverse_d[user_id][i].words:
                    reverse_d[user_id][i].words[value] = [key]
                else:
                    reverse_d[user_id][i].words[value].append(key)
                #если нет значения, то он создает его

def save_data(user_id):#
    print(database)
    database_for_savedata = {}
    for key in database:
        database_for_savedata[key] = [element.to_dict() for element in database[user_id]]
    print(database_for_savedata)
    file_dictionary = open('reverse_data.json', 'w', encoding='utf-8')# создание файла в котором будет храниться подборка
    file_dictionary.write(json.dumps(database_for_savedata, ensure_ascii=False, indent=4))#было in set_pair_words
    file_dictionary.close()

save_data(319826849)

print(reverse_d[319826849][6].words)
