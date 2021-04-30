import json
import os


class Conjugator:
    def __init__(self, verb, tense='present', negation=False,
                 politeness=True, kanji=1):
        self.verb = None
        self.tense = tense
        self.kanji = kanji
        self.politeness = politeness
        self.negation = negation
        self.stem = None
        self.root = None
        self.group = None
        self._set_verb(verb)
        self._set_stems()
        self._set_group(verb)
        self._set_endings()
        self._set_exceptions()

    def conjugate(self):
        if self.tense == 'past':
            return self.past()
        elif self.tense == 'present':
            return self.present()

    def _set_verb(self, verb):
        if self.kanji and 'kanji' in verb:
            self.verb = verb['kanji']
        else:
            self.verb = verb['kana']

    def _set_stems(self):
        if self.verb in ('来る'):
            self.stem = self.verb[1]
            self.root = self.verb[0]
        elif self.group == 'irregular':
            self.stem = self.verb[-2:]
            self.root = self.verb[:-2]
        else:
            self.root = self.verb[:-1]
            self.stem = self.verb[-1]


    def _set_group(self, verb):
        groups = {
            'る': 'ichidan',
            'する': 'irregular'
            }
        if verb['type'] in groups:
            self.group = groups[verb['type']]
        else:
            self.group = 'godan'

    def _set_endings(self):
        mydir = os.path.dirname(__file__)
        with open("{}/endings.json".format(mydir)) as fp:
            self.endings = json.load(fp)['endings']

    def _set_exceptions(self):
        mydir = os.path.dirname(__file__)
        with open("{}/exceptions.json".format(mydir)) as fp:
            self.exceptions = json.load(fp)['exceptions']

    def past(self):
        if self.politeness:
            ending = 'ました' if not self.negation else 'ませんでした'
            return self._masu_ending(ending)
        return self.past_short()

    def _masu_ending(self, ending):
        if self.verb in self.exceptions:
            return self.root + self.exceptions[self.verb]['masu'] + ending
        return self.root + \
            self.endings[self.group][self.stem]['masu'] + ending

    def past_short(self):
        if not self.negation:
            if self.verb in self.exceptions:
                te = self.exceptions[self.verb]['te']
            else:
                te = self.root + self.endings[self.group][self.stem]['te']
            if te.endswith('て'):
                return te[:-1] + 'た'
            else:
                return te[:-1] + 'だ'
        if self.verb in self.exceptions:
            nai = self.exceptions[self.verb]['nai']
        else:
            nai = self.root + self.endings[self.group][self.stem]['nai']
        return nai + 'なかった'

    def present(self):
        if self.politeness:
            ending = 'ます' if not self.negation else 'ません'
            return self._masu_ending(ending)
        else:
            return self.present_short()

    def present_short(self):
        if not self.negation:
            return self.verb
        if self.verb in self.exceptions:
            return self.exceptions[self.verb]['nai']
        return self.root + self.endings[self.group][self.stem]['nai'] + 'ない'

    def future(self):
        return self.present()

    def progressive(self):
        ending = 'います' if not self.negation else 'いません'
        if self.verb in self.exceptions:
            return self.exceptions[self.verb]['te'] + ending
        else:
            return self.root + self.endings[self.group][self.stem]['te'] + \
                ending
