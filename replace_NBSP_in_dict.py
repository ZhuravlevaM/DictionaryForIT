import json
from pair_words import PairWords
def load_from_json(): #обработка json и вывод словаря
    with open('data.json', 'r', encoding='utf-8') as file:
        data = file.read().replace(' ', " ")# Load JSON as a list of dictionaries замена символа на пробел
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(data)
char = ' '
print(f"Символ: {repr(char)}, Код: {ord(char)}")

load_from_json()