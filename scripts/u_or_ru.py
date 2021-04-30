#!/usr/bin/env python3

import json
import random

from conf import DICTIONARY_DIR
from lib.basics import save_to_json

FILE = "{}/verbs.json".format(DICTIONARY_DIR)
RETEST = 'u_or_ru.retest.json'
TYPES = ('', 'う', 'る')


def start():
    testable_verbs = get_testable_verbs()
    num_testable_verbs = len(testable_verbs)
    print("{} verbs to test.".format(num_testable_verbs))
    score, wrong = quiz(testable_verbs)
    if len(wrong) > 0:
        summarize_wrong(wrong)
        save_to_json(RETEST, {"verbs": wrong})
    print("{} out of {} ".format(score, num_testable_verbs))


def get_testable_verbs():
    verbs = load_json(FILE, 'verbs')
    testable_verbs = []
    for verb in verbs:
        if verb['type'] == 'る':
            testable_verbs.append(verb)
        elif verb['type'] == 'う' and verb['kana'].endswith('る'):
            testable_verbs.append(verb)
    random.shuffle(testable_verbs)
    return testable_verbs


def load_json(filepath, root):
    with open(filepath) as fp:
        db = json.load(fp)[root]
    return db


def quiz(testable_verbs):
    score = 0
    wrong = []
    i = 0
    for t in testable_verbs:
        i += 1
        if 'kanji' in t:
            prompt = "{}. {} ({})".format(i, t['kanji'], t['kana'])
        else:
            prompt = (t['kana'])

        answer = None
        while answer not in ('1', '2'):
            answer = input("{}: 1 for う, 2 for る: ".format(prompt)).strip()
        if TYPES[int(answer)] == t['type']:
            score += 1
            print("Yes.")
        else:
            print("WRONG. YOU PUTZ! "
                  "{} is a fricking {}-verb!!".format(prompt, t['type']))
            wrong.append(t)
    return score, wrong


def summarize_wrong(wrong):
    print("Incorrect\n-------")
    for w in wrong:
        if 'kanji' in w:
            print("{} ({}):".format(w['kanji'], w['kana']), w['type'])
        else:
            print(w['kana'] + ':', w['type'])
    print("Remember: i or e before ru => る-verb, mostly")


if __name__ == '__main__':
    start()
