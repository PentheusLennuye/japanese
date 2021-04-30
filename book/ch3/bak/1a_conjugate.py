#!/usr/bin/env python3

# Practice conjugation and basic sentence order

from conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary, get_furigana
# from lib.suu import convert_from_arabic
from grammar.verbs import Conjugator
from random import shuffle
from time import sleep

print("""
Conjugation and sentence order
------------------------------
""")

# Exercise 1. Conjugation

actions = ('飲む 聞く 見る 話す 行く 来る 帰る 寝る 読む '
           '起きる 勉強する する').split()
shuffle(actions)

verbs = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
doushi = keyed_dictionary(verbs, 'kanji')

c = Conjugator()
print("Exercise 1: Conjugate")
for a in actions:
    furigana = get_furigana(doushi[a])
    print()
    if furigana:
        print("          " + furigana)
    question = "Conjugate {} into -ます and -ません. Hit RETURN. ".format(a)
    input(question)
    answer = c.conjugate(doushi[a])
    answer += ' ' + c.conjugate(doushi[a], "indicative", False)
    spacing = int(len(question)/2 - len(answer)/2)
    print("\n" + ' '*spacing + answer)
    sleep(1)
