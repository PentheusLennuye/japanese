from lib.basics import get_kanji, get_furigana


class NounPhrase:
    '''
    Builds an array as follows:
    [ [kanji, furigana], ....]
    '''
    def __init__(self, noun_dict, noun, key='english',
                 purpose='subject', predicate=None, emphasis=False):
        self.noun_dict = noun_dict
        self.predicate = predicate   # Determines direct object particle
        self.emphasis = emphasis
        self.purpose = purpose
        self.key = key
        self.noun_phrase = []
        self.particle = None
        self.splitter = None

        self._set_splitter()
        self._split_nouns(noun)
        self._set_particle()

    def get_noun(self):
        return self.noun_phrase

    def get_noun_phrase(self):
        ''' returns ([[kanji, furigana]...], particle)'''
        return self.noun_phrase, self.particle

    def _set_splitter(self):
        if self.key == 'japanese':
            self.splitter = 'の'

    def _split_nouns(self, noun):
        if noun in self.noun_dict:
            self.noun_phrase.append(noun)
        noun_list = noun.split(self.splitter)
        for n in noun_list:
            try:
                self._add_noun(n)
            except KeyError:  # Maybe it's a possessive pronoun
                self._add_possessive(n)
        self.noun_phrase = self.noun_phrase[:-1]  # Cut off the last の

    def _add_noun(self, noun):
        noun_object = self.noun_dict[noun]
        furigana = get_furigana(self.noun_dict[noun])
        if not furigana:
            furigana = ''
        self.noun_phrase += [get_kanji(noun_object), furigana]
        self.noun_phrase += ['の', '']

    def _add_possessive(self, possessive):
        if self.key == 'japanese':
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
