#!/usr/bin/env python3
#
# Drills verbs, adjectives and nouns in short form
# past tense, negative and positive.

import json
import random

from lib.verbs import Conjugator as VC
from lib.adjectives import Conjugator as AC


MAXQ = 10


def main():
    quiz(MAXQ, 'verbs', 'past')
    print("====\n")
    quiz(MAXQ, 'adjectives', 'past')
    print("====\n")


def quiz(total, word_type, tense):
    title = word_type[:-1].capitalize()
    print("{} short form {} tense drill".format(title, tense))
    score = 0
    wrong = []

    words = load(word_type)
    if word_type == 'adjectives':
        irregulars = load('irregulars')
    else:
        irregulars = {}

    i = 0
    while i < total:
        negation = random.randint(0, 1)
        negate_string = ', negative' if negation else ''
        quiz_string = ' {}{}'.format(tense, negate_string)
        if 'kanji' in words[i]:
            kanji_quiz(word_type, irregulars, words[i],
                       tense, negation, quiz_string)
        else:
            kana_quiz(word_type, irregulars, words[i],
                      tense, negation, quiz_string)
        score, wrong = correct(words[i], score, wrong)
        i += 1
        print()
    print("Score: {}/{}".format(score, total))
    if len(wrong) > 0:
        print("Incorrect:")
        for w in wrong:
            print("\t{}".format(w['kana']))


def load(word_type):
    with open('dictionary/{}.json'.format(word_type)) as fp:
        words = json.load(fp)[word_type]
    random.shuffle(words)
    return words


# The first false is politeness
def kanji_quiz(word_type, irregulars, word, tense, negation, quiz_string):
    if word_type == 'verbs':
        kanjic = VC(word, tense, negation, False)
        kanac = VC(word, tense, negation, False, False)
    elif word_type == 'adjectives':
        kanjic = AC(irregulars, word, tense, negation, False)
        kanac = AC(irregulars, word, tense, negation, False, False)
    furigana = ' (' + word['kana'] + ')'
    query = word['kanji'] + furigana + quiz_string + '? '
    input(query)
    print(kanjic.conjugate() + ' (' + kanac.conjugate() + ')')


def kana_quiz(word_type, irregulars, word, tense, negation, quiz_string):
    if word_type == 'verbs':
        kanac = VC(word, tense, negation, False, False)
    elif word_type == 'adjectives':
        kanac = AC(irregulars, word, tense, negation, False, False)
    query = word['kana'] + quiz_string + '? '
    input(query)
    print(kanac.conjugate())


def correct(verb, score, wrong):
    correct = None
    while correct not in ('Y', 'y', 'N', 'n'):
        correct = input('Were you correct [Y/n]? ').strip()
        if correct in ('', 'y', 'Y'):
            correct = 'y'
        elif correct in ('n', 'N'):
            correct = 'n'
    if correct == 'y':
        score += 1
    else:
        wrong.append(verb)
    return score, wrong


if __name__ == '__main__':
    main()
