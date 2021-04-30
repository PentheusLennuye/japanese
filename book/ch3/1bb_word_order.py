#!/usr/bin/env python3.9

from random import shuffle
import wx

from conf import DICTIONARY_DIR
from lib.exercise import Exercise
from ui.mainframe import MainFrame
from grammar.verbs import Conjugator
from lib.basics import (load_from_json, keyed_dictionary)
from lib.particles import get_location, get_predicate, get_direct_object


title = "Chapter Three Exercise 1B (b)"
instructions = ("Create a valid sentence in present indicative form "
                "with the given terms.")
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
    questions = []
    answers = []
    shuffle(actions)
    for a in actions:
        e_loc, e_pred, e_dir_obj = a.split(':')
        j_loc, j_loc_part = get_location(nouns[e_loc])
        j_dir_obj, j_dir_obj_part = get_direct_object(
                meishi[e_dir_obj], verbs[e_pred]
        )
        j_pred = get_predicate(c, verbs[e_pred])

        questions.append([e_pred, ',', e_dir_obj, ',', e_loc])
        answers.append([j_loc, j_loc_part, j_dir_obj, j_dir_obj_part, j_pred])
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


if __name__ == '__main__':
    start()
