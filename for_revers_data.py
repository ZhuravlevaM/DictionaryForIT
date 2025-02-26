import json
from pair_words import PairWords

database = {}
def load_from_json(data): #обработка json и вывод словаря
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Load JSON as a list of dictionaries
    return [PairWords.from_dict(item) for item in data]

set_pair_words = load_from_json('data.json')

d = {'hi': ['привет', 'здравствуйте'], 'hello': ['привет', 'здравствуйте']}


# Создаем обратный словарь
reverse_d = set_pair_words.copy()
#print(reverse_d)

for i in range(len(set_pair_words)):
   set_words = set_pair_words[i].words
   reverse_d[i].words = {} #очистить данные в копии перед добавлением
   for key, values in list(set_words.items()):
        for value in values:
            if value not in reverse_d[i].words:
                reverse_d[i].words[value] = [key]
            else:
                reverse_d[i].words[value].append(key)
                #если нет значения, то он создает его
print(reverse_d)
def save_data():#
    database_for_savedata = [element.to_dict() for element in reverse_d]
    print(database_for_savedata)
    file_dictionary = open('reverse_data.json', 'w', encoding='utf-8')# создание файла в котором будет храниться подборка
    file_dictionary.write(json.dumps(database_for_savedata, ensure_ascii=False, indent=4))#было in set_pair_words
    file_dictionary.close()

save_data()

#print(reverse_d[319826849][6].words)
