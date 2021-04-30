#!/usr/bin/env python3.9

from random import shuffle, randint

import wx

from conf.conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from lib.exercise import Exercise
from lib.nounphrase import NounPhrase
from lib.particles import get_invitation
from lib.time import Time
from lib.verbs import Conjugator
from lib.ui.mainframe import MainFrame

title = "Chapter Three Exercise 3B"
instructions = "Make an invitation with the given terms."
actions = ['library::to study', 'my house::to talk', ':music:to listen',
           ':movie:to see', "McDonald's:hamburger:to eat",
           ':green tea:to drink', ':ice cream:to eat']

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
verbs = keyed_dictionary(verb_dict, 'english')
noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
nouns = keyed_dictionary(noun_dict, 'english')
dows = 'Sunday Monday Tuesday Wednesday Thursday Friday Saturday'.split()


def start_exercise():
    c = Conjugator()
    n = NounPhrase(nouns)
    questions = []
    answers = []
    shuffle(actions)
    for a in actions:
        i = randint(0, len(dows)-1)
        j_sentence = []
        j_sentence += Time(dows[i], nouns).get_time()
        e_sentence = [dows[i], '/']
        e_loc, e_dir_obj, e_pred = a.split(':')
        if e_loc != '':
            e_sentence += [e_loc, '/']
            n.build_noun_phrase(e_loc, 'location')
            j_sentence += n.get_noun_phrase()
        if e_dir_obj != '':
            e_sentence += [e_dir_obj, '/']
            n.build_noun_phrase(e_dir_obj, 'direct object', verbs[e_pred])
            j_sentence += n.get_noun_phrase()
        if e_pred != '':
            e_sentence.append(e_pred)
            j_sentence.append(get_invitation(c, verbs[e_pred]))

        questions.append(e_sentence)
        answers.append(j_sentence)
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


if __name__ == '__main__':
    start_exercise()
