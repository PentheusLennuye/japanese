#!/usr/bin/env python3

import json
import os

from .basics import get_furigana


class TenseNotAvailableError(Exception):
    pass


class Conjugator:
    def __init__(self, verb=None):
        self.tense = None
        self.polite = None
        self.positive = None
        self.stem = None
        self.root = None
        self.group = None
        self.set_verb(verb)

    def set_verb(self, verb):
        if verb is None:
            return
        if 'kanji' in verb:
            self.verb = verb['kanji']
        else:
            self.verb = verb['kana']
        self._set_exceptions()
        self._set_endings()
        self._set_group(verb)
        self._set_roots_and_stems()

    def _set_exceptions(self):
        mydir = os.path.dirname(__file__)
        with open("{}/irregulars.json".format(mydir)) as fp:
            self.exceptions = json.load(fp)['irregulars']['verbs']

    def _set_endings(self):
        mydir = os.path.dirname(__file__)
        with open("{}/endings.json".format(mydir)) as fp:
            self.endings = json.load(fp)['endings']

    def conjugate(self, tense='indicative', positive=True, polite=True):
        x = 1 if polite else 0  # To map to the JSON for positive and polite
        y = 0 if positive else 1
        furigana = get_furigana(self.verb)
        if furigana is None:
            furigana = ''

        if self.verb in self.exceptions:
            return [self.exceptions[self.verb][tense][x][y], furigana]

        if self.group == 'irregular':
            return [self.root + self.exceptions['する'][tense][x][y],
                    furigana]
        return [self.root + self.endings[self.group][self.stem][tense][x][y],
                furigana]

    def _set_group(self, verb):
        groups = {
            'る': 'ichidan',
            'する': 'irregular'
            }
        if verb['type'] in groups:
            self.group = groups[verb['type']]
        else:
            self.group = 'godan'

    def _set_roots_and_stems(self):
        if self.group == 'irregular':
            self.root = self.verb[:-2]
            self.stem = self.verb[-2:]
        else:
            self.root = self.verb[:-1]
            self.stem = self.verb[-1]


if __name__ == '__main__':
    c = Conjugator()
    myverb = {'english': 'to swim',
              'type': 'う',
              'kanji': '泳ぐ',
              'kana': 'およぐ',
              'particle': 'intransitive'}
    print("Test: printing some conjugations")
    print(c.conjugate(myverb))
    print(c.conjugate(myverb, "past presumptive"))
    print(c.conjugate(myverb, "past presumptive", False))
    print(c.conjugate(myverb, "past presumptive", False, False))
