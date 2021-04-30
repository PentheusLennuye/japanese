#!/usr/bin/env python3

from .basics import (get_kanji, get_furigana, load_from_json,
                     keyed_dictionary)


class NounPhrase:
    def __init__(self, noun_dict, key='english'):
        self.noun_dict = noun_dict
        self.key = key
        self.predicate = None   # Determines direct object particle
        self.emphasis = None
        self.purpose = None
        self.particle = None
        self.splitter = None

        self._set_splitter()

    def build_noun_phrase(self, noun, purpose='subject', predicate=None,
                          emphasis=False):
        '''
        Builds an array as follows:
        [ [kanji, furigana], [kanji, furigana], ....]
        '''
        self.noun_phrase = []
        self.purpose = purpose
        self.predicate = predicate
        self.emphasis = emphasis
        self._set_particle()
        self._split_nouns(noun)

    def get_noun_phrase(self):
        ''' returns [kanji, furigana],[k, f]...],[particle, '']'''
        answer = self.noun_phrase
        answer.append(self.particle)
        return answer

    def _set_splitter(self):
        if self.key == 'kanji':
            self.splitter = 'の'

    def _split_nouns(self, noun):
        if noun in self.noun_dict:
            self._add_noun(noun)
            return
        noun_list = noun.split(self.splitter)
        for n in noun_list:
            try:
                self._add_noun(n, False)
            except KeyError:  # Maybe it's a possessive pronoun
                self._add_possessive(n)
        self.noun_phrase = self.noun_phrase[:-1]  # Cut off the last の

    def _add_noun(self, noun, single=True):
        noun_object = self.noun_dict[noun]
        furigana = get_furigana(self.noun_dict[noun])
        if not furigana:
            furigana = ''
        self.noun_phrase.append([get_kanji(noun_object), furigana])
        if not single:
            self.noun_phrase.append(['の', ''])

    def _add_possessive(self, possessive):
        if self.key == 'kanji':
            possessives = {
                '私': ['私', 'わたし'],
                'あなた': ['あなた', ''],
                '彼': ['彼', 'かれ'],
                '彼女': ['彼女', 'かのじょ'],
                'からら': ['彼ら', 'かれら']
            }
        else:
            possessives = {
                'my': ['私', 'わたし'],
                'your': ['あなた', ''],
                'his': ['彼', 'かれ'],
                'her': ['彼女', 'かのじょ'],
                'their': ['彼ら', 'かれら']
            }
        self.noun_phrase += [possessives[possessive], ['の', '']]

    def _set_particle(self):
        purpose = self.purpose
        emphasis = self.emphasis
        particles = {
                'subject': ['は', ''],
                'indirect object': ['に', ''],
                'location': ['で', '']
        }
        if purpose == 'subject' and emphasis:
            self.particle = ['が', '']
        elif purpose == 'direct object':
            self.particle = [self.predicate['particle'], '']
        else:
            self.particle = particles[purpose]


if __name__ == '__main__':
    DICTIONARY_DIR = '../../dictionary'
    KEY = 'english'
    noun_dict = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
    nouns = keyed_dictionary(noun_dict, KEY)
    n = NounPhrase(nouns, KEY)
    n.build_noun_phrase('school', 'location')
    print(n.get_noun_phrase())
    n.build_noun_phrase('my house')
    print(n.get_noun_phrase())
