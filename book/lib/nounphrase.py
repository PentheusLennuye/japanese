#!/usr/bin/env python3

from .basics import (get_kanji, get_furigana, load_from_json,
                     keyed_dictionary)


articles = ['a', 'an', 'the']
conjunctions = {
    'and': ['と', ''],   # missing subleties like たり, や
    'or':  ['か', ''],   # missing subleties
    'with': ['て', ''],
    'but': ['でも', ''],
    'because': ['から', '']  # missing subleties
}


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
                          emphasis=False, action=True):
        '''
        Builds an array as follows:
        [ [kanji, furigana], [kanji, furigana], ....]
        Emphasis is only used for subject, and action will modify location.
        '''
        self.noun_phrase = []
        self.purpose = purpose
        self.predicate = predicate
        self.emphasis = emphasis
        self._set_particle(action)
        self._split_nouns(self._lose_the_article(noun))

    def get_noun_phrase(self):
        ''' returns [kanji, furigana],[k, f]...],[particle, '']'''
        answer = self.noun_phrase
        answer.append(self.particle)
        return answer

    def _set_splitter(self):
        if self.key == 'kanji':
            self.splitter = 'の'

    def _lose_the_article(self, noun):
        tokens = noun.split()
        if tokens[0].lower() in articles:
            return ' '.join(tokens[1:])
        return noun

    def _split_nouns(self, noun_phrase):
        if noun_phrase in self.noun_dict:  # The phrase IS a noun
            self._add_noun(noun_phrase)
            return
        noun_list = noun_phrase.split(self.splitter)
        for n in noun_list:
            if n in conjunctions:
                self.noun_phrase.append(conjunctions[n])
                continue
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
        if possessive not in possessives:
            return False
        self.noun_phrase += [possessives[possessive], ['の', '']]
        return True

    def _add_determiner(self, determiner):
        if self.key == 'kanji':
            determiners = {
                'この': ['この', ''],
                'その': ['その', ''],
                'あの': ['あの', '']
            }
        else:
            determiners = {
                'this': ['この', ''],
                'that': ['その', ''],
                'that there': ['あの', '']
            }
        if determiner not in determiners:
            return False
        self.noun_phrase += [determiners[determiner], ['の', '']]
        return True

    def _set_particle(self, action):
        purpose = self.purpose
        emphasis = self.emphasis
        particles = {
                'subject': ['は', ''],
                'indirect object': ['に', ''],
                'location': ['に', ''],
                'complement': [],
        }
        if purpose == 'subject' and emphasis:
            self.particle = ['が', '']
        elif purpose == 'location' and action:
            self.particle = ['で', '']
        elif purpose == 'direct object':
            if 'particle' in self.predicate:
                self.particle = [self.predicate['particle'], '']
            else:
                self.particle = ['', '']
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
