class PairWords:
    def __init__(self, name, words=None):
        if words is None:
            words = dict()
        self.name = name
        self.words = words

    def get_name(self):
        return self.name

    def get_words(self):
        return self.words

    def add(self, part1, part2):
        if part1 in self.words:
            self.words[part1].extend(part2)
        else:
            self.words[part1] = part2

    def delete(self, key):
        if key in self.words:
            self.words.pop(key) #удалить по ключу
            return True
        else:
            for i in self.words:
                value = self.words[i]
                if key in value:
                    self.words.pop(i)
                    return True
            return False

    def change(self, key, change_word, mode):
        if mode == 1:# 1=английский язык, ключ в словаре
            if key in self.words: # иностранное слово
                time_value = self.words[key] #переменная, которая временно будет хранить значение по ключу
                self.words.pop(key)
                self.words[change_word] = time_value
                print('if in change mode 1')
                return True

            #нужно дописать возможность удаления по значению, кнопки по какому варианту будет происходить удаление
        elif mode == 2:
            if key in self.words:
                self.words[key] = [change_word]
                return True
        else:
             return False

    def print(self):
        print(self.words)

    def __str__(self):
        return f'{self.name} {self.words}'

    def to_dict(self):
        return {
           "name":  self.name,
            "words": self.words
        }

    def change_name_set(self, new_name):
        self.name = new_name

    @staticmethod
    def from_dict(data):
        """Create a PairWords object from a dictionary."""
        return PairWords(name=data["name"], words=data["words"])
