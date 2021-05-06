#!/usr/bin/env python3.9

# There isn't.
# Determine or list whether things exist at a place or not.

import wx

from conf.conf import DICTIONARY_DIR, AI_DIR
from lib.ai import is_iru
from lib.basics import load_from_json, keyed_dictionary
from lib.exercise import Exercise
from lib.nounphrase import NounPhrase
from lib.particles import get_predicate
from lib.verbs import Conjugator
from lib.ui.mainframe import MainFrame


POLITE = True
title = "Chapter Four Exercise 1b"
instructions = "Respond fully and correctly to each question."

questions = [
    'あなたの町に日本のレストランがありますか。',
    'あなたの家に猫がいますか。',
    'あなたの学校に何がありますか。',
    'あなたの学校に日本人の学生がいますか。',
    'デパートに何がありますか。',
    'この教室に誰がいますか。',
    '動物園に何がいますか。',
    'あなたの国に何がありますか。',
    'あなたの家に何がありますか。'
]

e_answers = [
    ['no', 'my neighbourhood', 'Japan restaurant', 'to exist'],
    ['no', 'my house', 'cat', 'to exist'],
    ['', 'my school', 'classroom', 'to exist'],
    ['no', 'my school', 'Japanese person', 'to exist'],
    ['', 'department store', 'clothes', 'to exist'],
    ['', 'this school', 'teacher', 'to exist'],
    ['', 'zoo', 'dog', 'to exist'],
    ['', 'my country', 'lake', 'to exist'],
    ['', 'my house', 'food', 'to exist']
]

yesno = {
    'no': ['いいえ', ''],
    'yes': ['ええ', '']
}

YESNO = 0
LOC = 1
SUBJ = 2

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
doushi = keyed_dictionary(verb_dict, 'kanji')

noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
nouns = keyed_dictionary(noun_dict, 'english')

ai = load_from_json("{}/relations.json".format(AI_DIR), 'relation')


def start_exercise():
    # Basically, if it isn't "iru," it's "aru."
    c = Conjugator()
    n = NounPhrase(nouns)
    positive = True
    answers = []
    i = 0
    while i < len(questions):
        a_sentence = []
        if e_answers[i][YESNO] != '':
            a_sentence.append(yesno[e_answers[i][YESNO]])
        if e_answers[i][LOC] != '':
            n.build_noun_phrase(
                e_answers[i][LOC], 'location', None, None, False  # no action
            )
            a_sentence += n.get_noun_phrase()
        if e_answers[i][SUBJ] != '':
            n.build_noun_phrase(
                e_answers[i][SUBJ], 'subject', None, True  # Emphasis on iru
            )
            a_sentence += n.get_noun_phrase()
        if e_answers[i][YESNO] == 'no':
            positive = False
        else:
            positive = True
        if is_iru(ai, e_answers[i][SUBJ]):
            iru = get_predicate(c, doushi['いる'], positive)
            a_sentence.append(iru)
        else:
            aru = get_predicate(c, doushi['ある'], positive)
            a_sentence.append(aru)
        answers.append(a_sentence)
        i += 1
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


if __name__ == '__main__':
    start_exercise()
