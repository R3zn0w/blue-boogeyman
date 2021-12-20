# -*- coding: utf-8 -*-

import codecs
import json
with codecs.open("slowa_picked.txt", "r", "utf-8") as f:
    temp = f.read().splitlines()
    f.close()


# create new dictionary with 5>= letter words
# with codecs.open("slowa_picked.txt", "w", "utf-8") as f:
#     for word in temp:
#         if word.__len__() >= 5:
#             f.write(f'{word}\n')
#     f.close()


# create dictionary that maps numeral representation into all possible words (e.g. "11111111": ["aaronowa", "aaronowe", ... ])
tab1 = ["a", "c", "e", "m", "n", "o", "r", "s", "u", "w", "z", "x", "v"]
tab2 = ["ą", "ę", "g", "j", "p", "y", "q"]
tab3 = ["b", "ć", "d", "h", "k", "l", "ł", "ń", "ó", "ś", "t", "ź", "ż", "i"]
tab4 = ["f"]
gloss = {"null": ["noll"]}
for line in temp:
    numbered = ""
    for char in line:
        if char in tab1:
            numbered = numbered + "1"
        elif char in tab2:
            numbered = numbered + "2"
        elif char in tab3:
            numbered = numbered + "3"
        elif char in tab4:
            numbered = numbered + "4"
    if numbered in gloss:
        gloss[numbered].append(line)
    else:
        gloss.update({numbered: [line]})

with open('dict.json', 'w') as fp:
    json.dump(gloss, fp)
    fp.close()
