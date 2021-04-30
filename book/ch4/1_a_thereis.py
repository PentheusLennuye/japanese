#!/usr/bin/env python3.9

# There is.
# An exercise on determining whether or not something is animate or not.

from random import shuffle

import wx

from conf.conf import DICTIONARY_DIR, AI_DIR
from lib.basics import load_from_json, keyed_dictionary, searchtree
from lib.exercise import Exercise
from lib.nounphrase import NounPhrase
from lib.particles import get_predicate
from lib.verbs import Conjugator
from lib.ui.mainframe import MainFrame


title = "Chapter Four Exercise 1"
instructions = "State that there is (there exists) each item"

items = ('hospital cafe bank library supermarket restaurant '
         'park bicycle child woman man dog cat bus').split()
items += ['post office', 'department store', 'bus stop']

verb_dict = load_from_json("{}/verbs.json".format(DICTIONARY_DIR), 'verbs')
doushi = keyed_dictionary(verb_dict, 'kanji')

noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
nouns = keyed_dictionary(noun_dict, 'english')

ai = load_from_json("{}/relations.json".format(AI_DIR), 'relation')


def start_exercise():
    # Basically, if it isn't "iru," it's "aru."
    c = Conjugator()
    iru = get_predicate(c, doushi['いる'])
    aru = get_predicate(c, doushi['ある'])
    n = NounPhrase(nouns)
    questions = []
    answers = []

    shuffle(items)
    for i in items:
        q_sentence = [i, ]
        a_sentence = []
        n.build_noun_phrase(i, 'subject', None, True)  # Emphasis for aru/iru
        a_sentence += n.get_noun_phrase()
        if is_iru(i):
            a_sentence.append(iru)
        else:
            a_sentence.append(aru)
        questions.append(q_sentence)
        answers.append(a_sentence)
    app = wx.App()
    MainFrame(Exercise(title, instructions, questions, answers))
    app.MainLoop()


def is_iru(noun):
    ''' Determine the AI path for the noun. If it matches on of the relations
        return True
    '''
    successful_paths = ['living thing:person', 'living thing:animal']
    my_path = []
    searchtree(noun, my_path, ai, None)
    my_path.reverse()
    my_path = ':'.join(my_path)
    return my_path in successful_paths


if __name__ == '__main__':
    start_exercise()
