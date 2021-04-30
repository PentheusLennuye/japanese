#!/usr/bin/env python3

# Practice stringing together direct objects and conjugated verbs

from conf import DICTIONARY_DIR
from lib.basics import (load_from_json, keyed_dictionary, get_furigana,
                        get_kanji)

# from lib.suu import convert_from_arabic
from grammar.verbs import Conjugator
from random import shuffle
from time import sleep

print("""
Conjugation and sentence order
------------------------------
""")

actions = ['library:to read:雑誌', 'home:to hear:音楽', 'school:to do:テニス',
           "McDonald's:to eat:ハンバーガー", 'cafe:to drink:コーヒー',
           'home:to see:テレビ', 'college:to study:日本語']

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
verbs = keyed_dictionary(verb_dict, 'english')

noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
meishi = keyed_dictionary(noun_dict, 'kanji')
nouns = keyed_dictionary(noun_dict, 'english')


def start():
    c = Conjugator()
    shuffle(actions)
    print("Exercise 2: Basic word order and present indicative "
          "polite conjugation")
    for a in actions:
        place, predicate, dir_object = a.split(':')
        pose_question(place, predicate, dir_object)
        answer_question(c, place, predicate, dir_object)
        sleep(1)


def pose_question(place, predicate, dir_object):
    furigana = get_furigana(meishi[dir_object])
    question = ("Create a proper sentence with '{}', "
                "'{}' and '{}.'".format(place, predicate, dir_object))
    fmt = '{:>' + str(len(question)-1) + '}'
    print()
    if furigana:
        print(fmt.format(furigana))
    input(question + " Hit RETURN. ")


def answer_question(c, place, predicate, dir_object):
    furigana = get_furigana(nouns[place])
    if furigana:
        print("\n" + furigana)

    answer = get_kanji(nouns[place]) + 'で'
    answer += dir_object + verbs[predicate]['particle']
    answer += c.conjugate(verbs[predicate])
    print(answer)
    furigana = get_furigana(verbs[predicate])
    if furigana:
        print(' '*20 + furigana)


if __name__ == '__main__':
    start()
