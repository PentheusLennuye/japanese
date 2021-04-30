#!/usr/bin/env python3

# Practice stringing together direct objects and conjugated verbs

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

actions = ['to read:雑誌', 'to hear:音楽', 'to do:テニス',
           'to eat:ハンバーガー', 'to drink:コーヒー', 'to see:テレビ',
           'to study:日本語']
shuffle(actions)

verbs = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
ev = keyed_dictionary(verbs, 'english')
nouns = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
meishi = keyed_dictionary(nouns, 'kanji')

c = Conjugator()
print("Exercise 2: Basic word order and present indicative polite conjugation")
for a in actions:
    verb, noun = a.split(':')
    furigana = get_furigana(meishi[noun])
    question = ("Create a proper sentence with "
                "'{}' and '{}.'".format(verb, noun))
    fmt = '{:>' + str(len(question)-1) + '}'
    print()
    if furigana:
        print(fmt.format(furigana))
    input(question + " Hit RETURN. ".format(verb, noun))

    answer = noun + ev[verb]['particle'] + c.conjugate(ev[verb])
    furigana = get_furigana(ev[verb])
    spacing = int(len(question)/2 - len(answer)/2)
    astring = "\n" + ' '*spacing + answer
    if furigana:
        astring += ' (' + furigana + ')'
    print(astring)
    sleep(1)
