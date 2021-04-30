#!/usr/bin/env python3.9

from random import shuffle
import wx

from conf import DICTIONARY_DIR
from lib.exercise import Exercise
from ui.mainframe import MainFrame
from grammar.verbs import Conjugator
from lib.basics import (load_from_json, keyed_dictionary)
from lib.particles import (get_invitation, get_direct_object, get_location,
                           build_modified_noun)


title = "Chapter Three Exercise 3A"
instructions = "Make an invitation with the given terms."
actions = [':movie:to see', ':my house:to come', ':tennis:to do',
           ':supper:to eat', 'library::to study', 'cafe::to talk',
           'home:green tea:to drink', ':music:to listen']

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
verbs = keyed_dictionary(verb_dict, 'english')
noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
nouns = keyed_dictionary(noun_dict, 'english')


def start():
    c = Conjugator()
    questions = []
    answers = []
    shuffle(actions)
    for a in actions:
        j_sentence = []
        e_sentence = []
        e_loc, e_dir_obj, e_pred = a.split(':')
        if e_loc != '':
            e_sentence += [e_loc, ',']
            j_sentence += get_location(nouns[e_loc])
        if e_dir_obj != '':
            e_sentence += [e_dir_obj, ',']
            try:
                j_sentence += get_direct_object(
                    nouns[e_dir_obj], verbs[e_pred]
                )
            except KeyError:
                j_sentence += build_modified_noun(
                    nouns, verbs, e_dir_obj, e_pred
                )
        if e_pred != '':
            e_sentence.append(e_pred)
            j_sentence.append(get_invitation(c, verbs[e_pred]))

        questions.append(e_sentence)
        answers.append(j_sentence)
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


if __name__ == '__main__':
    start()
