#!/usr/bin/env python3

# suuji (数字): drills on the cost of certain objects

from conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from lib.suu import convert_from_arabic
from random import shuffle, normalvariate

print("""
SUUJI practice. 数字練習
------------------------
You will see the additional terms:
1. 改行(かいぎょう). It means "line break" (i.e., RETURN)
2. 答え(こたえ). It means "answer."
3. 押して(おして). It is the command to "push."
""")

objects = ['pencil:50', 'umbrella:1000', 'newspaper:110', 'book:1500',
           'shoe:3500', 'watch:10000', 'bag:20000', 'dictionary:8000',
           'trousers:9000', 'bicycle:25000', 'notebook:450', 'hat:2800',
           't-shirt:9000']
shuffle(objects)

nouns = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
enouns = keyed_dictionary(nouns, 'english')
for o in objects:
    english, price = o.split(':')
    price = int(normalvariate(float(price), 3))
    entry = enouns[english]
    if 'kanji' in entry:
        jobject = entry['kanji']
        furigana = "({})".format(entry['kana'])
    else:
        jobject = entry['kana']
        furigana = None
    input("\nAsk the question: How much is the {}. "
          "Hit RETURN.".format(english))
    print("{}はいくらですか。({}円)".format(jobject, price))
    if furigana:
        print(furigana)
    input("お答えください。改行を押して。".format(jobject))
    print("{}は{}円です。".format(jobject, convert_from_arabic(price)))
