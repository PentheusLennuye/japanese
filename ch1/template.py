#!/usr/bin/env python3
# File: TEMPLATE.py
#

import json
import os
import random
import yaml

CURDIR = os.path.dirname(os.path.realpath(__file__))
NOUNS = os.path.join(CURDIR, '../dictionary', 'nouns.json')
RELATIONS = os.path.join(CURDIR, '../ai', 'relations.yaml')
MAXQ = 10


def start():
    majors, occupations, people = get_lists()
    print(majors)
    print(occupations)
    print(people)


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

    random.shuffle(majors)
    random.shuffle(occupations)
    random.shuffle(people)

    return(majors, occupations, people)


def convert_to_english_hash(nouns):
    nounhash = {}
    for n in nouns:
        nounhash[n['english']] = n
    return nounhash


if __name__ == '__main__':
    start()
