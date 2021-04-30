#!/usr/bin/env python3
# File: nounphrase.py
#
# Practises X の Y

import json
import os
import random
import yaml

CURDIR = os.path.dirname(os.path.realpath(__file__))
NOUNS = os.path.join(CURDIR, '../dictionary', 'nouns.json')
RELATIONS = os.path.join(CURDIR, '../ai', 'relations.yaml')
MAXQ = 10

SKIP_HEADER = ['time', 'event', 'activity', 'media', 'transport',
               'instrument', 'language']

def start():
    nouns, relations = open_files()
    metanouns = get_metanouns(nouns, relations)
    names = get_names(relations)
    quiz("の", names, metanouns)


def open_files():
    with open(RELATIONS) as fp:
        relations = yaml.load(fp, Loader=yaml.FullLoader)['relations']
    with open(NOUNS) as fp:
        nouns = json.load(fp)['nouns']
    nouns = convert_to_english_hash(nouns)
    return nouns, relations


def convert_to_english_hash(nouns):
    nounhash = {}
    for n in nouns:
        nounhash[n['english']] = n
    return nounhash


def get_metanouns(nouns, relations):
    metanouns = []
    for header in ('living thing', 'abstract', 'object'):
        sublist = relations[header].keys()
        for s in sublist:
            if s in SKIP_HEADER:
                continue
            if s == 'discipline':
                s = 'subject'
            elif s == 'occupation':
                s = 'job'
            if s not in ['unclassified']:
                metanouns.append(nouns[s])
    random.shuffle(metanouns)
    return metanouns


def get_names(relations):
    names = []
    for i in relations['name']['person']:
        names.append(i)
    return names


def quiz(title, names, nouns):
    maxpeople = len(names) - 1
    halt = min(MAXQ, len(nouns)) - 1
    print("{} questions on {}.\n".format(halt + 1, title))
    i = 0
    j = 0
    while i < halt:
        if j > maxpeople:
            j = 0
        en = nouns[i]['english']
        q = "{}'s {} in Japanese? ".format(names[j], en)
        if 'kanji' in nouns[i]:
            a = "   A: {}さんの{}".format(names[j], nouns[i]['kana'])
            a += " ({})".format(nouns[i]['kanji'])
        else:
            a = "{}さんの{}".format(names[j], nouns[i]['kana'])
        input(q)
        print(a)
        print()
        i += 1
        j += 1


if __name__ == '__main__':
    start()
