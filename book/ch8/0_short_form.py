#!/usr/bin/env python3
#
# Drills verbs, adjectives and nouns in short form
# past tense, negative and positive.

import json
import random

from lib.verbs import Conjugator as VC
from lib.adjectives import Conjugator as AC


MAXQ = 10
groups = {
        'る': 'ichidan',
        'する': 'irregular'
        }


def main():
    verb_quiz(MAXQ)
    print("====\n")
    adjective_quiz(MAXQ)


def verb_quiz(total):
    print("Verb short form drill")
    verbs = load('verbs')
    score = 0
    wrong = []

    i = 0
    while i < total:
        negation = random.randint(0, 1)
        negate_string = ', negative' if negation else ''
        if verbs[i]['type'] in groups:
            group = groups[verbs[i]['type']]
        else:
            group = 'godan'
        if 'kanji' in verbs[i]:
            kanji_verb_quiz(verbs[i], group, negation, negate_string)
        else:
            kana_verb_quiz(verbs[i], group, negation, negate_string)
        score, wrong = correct(verbs[i], score, wrong)
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


def kanji_verb_quiz(verb, group, negation, negate_string):
    kanjic = VC(verb['kanji'], group,
                politeness=False, negation=negation)
    kanac = VC(verb['kana'], group,
               politeness=False, negation=negation)
    furigana = ' (' + verb['kana'] + ')'
    query = verb['kanji'] + furigana + negate_string + '? '
    input(query)
    print(kanjic.present() + ' (' + kanac.present() + ')')


def kana_verb_quiz(verb, group, negation, negate_string):
    kanac = VC(verb['kana'], group,
               politeness=False, negation=negation)
    query = verb['kana'] + negate_string + '? '
    input(query)
    print(kanac.present())


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


def adjective_quiz(total):
    print("Adjective short form drill")
    adjectives = load('adjectives')
    irregulars = load('irregulars')
    score = 0
    wrong = []

    i = 0
    while i < total:
        negation = random.randint(0, 1)
        negate_string = ', negative' if negation else ''
        if 'kanji' in adjectives[i]:
            kanji_adjective_quiz(adjectives[i], irregulars,
                                 negation, negate_string)
        else:
            kana_adjective_quiz(adjectives[i], irregulars,
                                negation, negate_string)
        score, wrong = correct(adjectives[i], score, wrong)
        i += 1
        print()
    print("Score: {}/{}".format(score, total))
    if len(wrong) > 0:
        print("Incorrect:")
        for w in wrong:
            print("\t{}".format(w['kana']))


def kanji_adjective_quiz(adj, irr, negation, negate_string):
    kanjic = AC(irr, adj, 'nonpast', negation, False)
    kanac = AC(irr, adj, 'nonpast', negation, False, False)
    furigana = ' (' + adj['kana'] + ')'
    query = adj['kanji'] + furigana + negate_string + '? '
    input(query)
    print(kanjic.get_adjective() + ' (' + kanac.get_adjective() + ')')


def kana_adjective_quiz(adj, irr, negation, negate_string):
    kanac = AC(irr, adj, 'nonpast', negation, False, False)
    query = adj['kana'] + negate_string + '? '
    input(query)
    print(kanac.get_adjective())


if __name__ == '__main__':
    main()
