# Default kana.!/usr/bin/env python3


adjective_map = {
    'い': {
        'long': {
            'nonpast': ['です', 'くないです'],
            'past': ['かったです', 'くなかったです']
        },
        'short': {
            'nonpast': ['', 'くない'],
            'past': ['かった', 'くなかった']
        }
    },
    'な': {
        'long': {
            'nonpast': ['です', 'じゃないです'],
            'past': ['でした', 'じゃなかったです']
        },
        'short': {
            'nonpast': ['だ', 'じゃない'],
            'past': ['だった', 'じゃなかった']
        }
    }
}


class Conjugator():
    def __init__(self, irregulars, adjective, tense='nonpast',
                 negation=False, politeness=True, kanji=1):
        self.irregulars = irregulars
        self.adjective = adjective
        self.tense = tense
        self.form = 'long' if politeness else 'short'
        self.negation = negation
        self.kanji = kanji
        self.english = adjective['english']
        self._set_japanese()

    def conjugate(self):
        f = self.form
        t = self.tense
        n = self.negation
        at = self.adjective['type']

        # Check for irregular first
        # The irregular list is [kanji, kana].
        w = 1
        if self.english in self.irregulars:
            if self.kanji and self.irregular[self.english][f][t][n][0] != '':
                w = 0
            return self.irregulars[self.english][f][t][n][w]

        # Otherwise
        root = self._modify_for_tense()
        return root + adjective_map[at][f][t][n]

    def _set_japanese(self):
        if self.kanji and 'kanji' in self.adjective:
            self.japanese = self.adjective['kanji']
        else:
            self.japanese = self.adjective['kana']

    def _modify_for_tense(self):
        # い-adjectives
        if self.adjective['type'] == 'い':
            if self.tense == 'past' or self.negation:
                return self.japanese[:-1]

        return self.japanese
