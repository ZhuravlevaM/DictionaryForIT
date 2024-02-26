import random
from random import randint
dictionary = {'reboot':'перезагружать', 'source':'источник', 'compile':'компилировать'}
rand = list(list(dictionary.items())[randint(0, len(dictionary)-1)])
random.shuffle(rand)
print(rand[0])
translate = input()
if translate == rand[1]:
    print('Good')
else:
    print('Try again')

#if (ran_word == rand[0] and translate == rand[1]) or (ran_word == rand[1] and translate == rand[0]):
#    print('Good')
#elif ran_word == rand[1] and translate == rand[0]:
#    print('Good')
#else:
#    print('Try again')

