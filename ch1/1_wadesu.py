#!/usr/bin/env python3
# File: wadesu.py
#
# Practises X は Y です。

import json
import os
import random
import yaml

CURDIR = os.path.dirname(os.path.realpath(__file__))
NOUNS = os.path.join(CURDIR, '../dictionary', 'nouns.json')
RELATIONS = os.path.join(CURDIR, '../ai', 'relations.yaml')
MAXQ = 10


def start():
    names, majors, occupations, people = get_lists()
    quiz('majors', '何', names, majors)
    quiz('occupations', '何', names, occupations)
    quiz('people', '誰', names, people)


def get_lists():
    with open(RELATIONS) as fp:
        relations = yaml.load(fp, Loader=yaml.FullLoader)['relations']
    with open(NOUNS) as fp:
        nouns = json.load(fp)['nouns']
    nouns = convert_to_english_hash(nouns)
    majors = []
    for m in relations['abstract']['discipline']:
        majors.append(nouns[m])
    occupations = []
    for o in relations['abstract']['occupation']:
        occupations.append(nouns[o])
    people = []
    for p in relations['living thing']['person']:
        people.append(nouns[p])
    names = []
    for n in relations['name']['person']:
        names.append(n)

    random.shuffle(names)
    random.shuffle(majors)
    random.shuffle(occupations)
    random.shuffle(people)

    return(names, majors, occupations, people)


def convert_to_english_hash(nouns):
    nounhash = {}
    for n in nouns:
        nounhash[n['english']] = n
    return nounhash


def quiz(title, qu, names, attr):
    maxpeople = len(names) - 1
    halt = min(MAXQ, len(attr)) - 1
    print("{} questions on {}.\n".format(halt + 1, title))
    i = 0
    j = 0
    while i < halt:
        if j > maxpeople:
            j = 0
        en = attr[i]['english']
        q = "{}. Q: {}さんの専攻は{}ですか。({})".format(i+1, names[j], qu, en)
        if 'kanji' in attr[i]:
            a = "   A: {}さんの専攻は{}です。".format(names[j], attr[i]['kana'])
            a += " ({})".format(attr[i]['kanji'])
        else:
            a = "{}さんの専攻は{}です。".format(names[j], attr[i]['kana'])
        input(q)
        print(a)
        print()
        i += 1
        j += 1


if __name__ == '__main__':
    start()
