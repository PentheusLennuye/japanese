#!/usr/bin/env python3.9

from random import shuffle, randint
import wx

from conf.conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from lib.exercise import Exercise
from lib.nounphrase import NounPhrase
from lib.time import Time
from lib.particles import get_adverb, get_predicate
from lib.verbs import Conjugator
from lib.ui.mainframe import MainFrame


title = "Chapter Three Exercise 4"
instructions = "Answer how often you do an activity."
actions = [
    ['', '', '', 'スポーツ', 'する', ''],
    ['', '', '', '雑誌', '読む', ''],
    ['', '', '', '図書館', '行く', ''],
    ['', '', '', '映画', '見る', ''],
    ['', '', '', 'コーヒー', '飲む', ''],
    ['', '', '', '日本の音楽', '聞く', ''],
    ['', '', '', '朝ご飯', '食べる', '']
]
SUBJ = 0
TIME = 1
LOC = 2
OBJ = 3
PRED = 4
PADV = 5

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
doushi = keyed_dictionary(verb_dict, 'kanji')
noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
meishi = keyed_dictionary(noun_dict, 'kanji')
adv_dict = load_from_json("{}/adverbs.json".format(DICTIONARY_DIR), 'adverbs')
adverbs = keyed_dictionary(adv_dict, 'english')


def start_exercise():
    c = Conjugator()
    n = NounPhrase(meishi, 'kanji')
    questions = []
    answers = []
    shuffle(actions)
    for a in actions:
        i = randint(0, len(adv_dict)-1)
        a[PADV] = adv_dict[i]['english']
        q_sentence = []
        a_sentence = []
        if a[SUBJ] != '':
            q_sentence += [a[SUBJ], '/']
            n.build_noun_phrase(a[SUBJ])
            a_sentence += n.get_noun_phrase()
        if a[TIME] != '':
            q_sentence += [a[TIME], '/']
            a_sentence += Time(a[TIME]).get_time()
        if a[LOC] != '':
            q_sentence += [a[LOC], '/']
            n.build_noun_phrase(a[LOC], 'location')
            a_sentence += n.get_noun_phrase()
        if a[OBJ] != '':
            q_sentence += [a[OBJ], '/']
            n.build_noun_phrase(a[OBJ], 'direct object', doushi[a[PRED]])
            a_sentence += n.get_noun_phrase()
        if a[PADV] != '':
            q_sentence += [a[PADV], '/']
            a_sentence.append(get_adverb(adverbs[a[PADV]]))
        if a[PRED] != '':
            q_sentence.append(a[PRED])
            a_sentence.append(get_predicate(c, doushi[a[PRED]]))

        questions.append(q_sentence)
        answers.append(a_sentence)
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


if __name__ == '__main__':
    start_exercise()
