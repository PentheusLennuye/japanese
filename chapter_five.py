#!/usr/bin/env python3

import json
import random

from lib.adjectives import get_long_adjective

ADJ_FILE = 'adjectives.json'
IRR_FILE = 'irregular.json'


def start():
    adjectives = load_adjectives(ADJ_FILE)
    irregulars = load_irregulars(IRR_FILE)
    while True:
        test_long_adjective(adjectives, irregulars)
        if is_quit():
            break


def load_adjectives(filepath):
    with open(filepath) as fp:
        db = json.load(fp)['adjectives']
    return db


def load_irregulars(filepath):
    with open(filepath) as fp:
        db = json.load(fp)['adjectives']
    return db


def test_long_adjective(adjectives, irregulars):
    index = random.randint(0, len(adjectives)-1)
    negation = random.randint(0, 1)
    tense = ('nonpast', 'past')[random.randint(0, 1)]
    pose_long_adjective_question(adjectives, index, tense, negation)
    answer, furigana = get_long_adjective(irregulars, adjectives[index],
                                          tense, negation)
    print(answer)
    if furigana:
        print("({})".format(furigana))


def pose_long_adjective_question(adjectives, index, tense, negation):
    english = adjectives[index]['english']
    question = "What is '{}' in {} tense{}? ".format(
            english,
            tense,
            ('', ', negative')[negation]
            )
    input(question)


def is_quit():
    response = None
    while response not in ('Y', 'y', 'N', 'n', ''):
        response = input('Continue [Y/n]? ').strip()
        if response == '':
            response = 'y'
    return response in ('N', 'n')


if __name__ == '__main__':
    start()
