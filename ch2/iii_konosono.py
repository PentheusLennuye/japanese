#!/usr/bin/env python3

# kono hon wa ikura desu ka(これはなんですか): price drills

from conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from lib.suu import convert_from_arabic
from lib.nouns import get_definite_article
from random import randint, shuffle, normalvariate

print("""
KORE and SORE practice. これとそれの練習
---------------------------------------
You will see the additional terms:
1. 改行(かいぎょう). It means "line break" (i.e., RETURN)
2. 答え(こたえ). It means "answer."
3. 押して(おして). It is the command to "push."
""")

things = ('pencil:60 pen:290 computer:68000 wallet:4300 dictionary:3500 '
          'bicycle:17000 clock:12600 umbrella:900 bag:4200 book:2100 pen:315 '
          'cap:1800 t-shirt:2800 trousers:7350 shoe:2700').split()
shuffle(things)

nouns = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
enouns = keyed_dictionary(nouns, 'english')
for pair in things:
    thing, price = pair.split(':')
    price = int(normalvariate(float(price), 3))
    entry = enouns[thing]
    if 'kanji' in entry:
        mono = entry['kanji']
        furigana = "({})".format(entry['kana'])
    else:
        mono = entry['kana']
        furigana = None
    that = get_definite_article(thing, 'that')
    ethis = get_definite_article(thing, 'this')
    specific_thing = [that + ' ' + thing, ethis + ' ' + thing,
                      that + ' ' + thing + ' over there']
    tokutenomono = ['その' + mono, 'この' + mono, 'あの' + mono]
    index = randint(0, 2)
    input("\nAsk the question: How much is {}? "
          "Hit RETURN. ".format(specific_thing[index]))
    print("{}はいくらですか。".format(tokutenomono[index]))
    if furigana:
        print(furigana)
    input("\nお答えください。改行を押して。({}円) ".format(price))
    print("{}は{}円です。".format(tokutenomono[index], convert_from_arabic(price)))
