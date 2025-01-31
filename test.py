import json
#def load_from_json(data): #обработка json и вывод словаря
with open('test_data.json', 'r+', encoding='utf-8') as file:
    data = file.read().replace(u"\xa0", " ")# Load JSON as a list of dictionaries
    print(data)
    file.write(data)
char = ' '
print(f"Символ: {repr(char)}, Код: {ord(char)}")

