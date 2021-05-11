#!/usr/bin/env python3.9

# There isn't.
# Determine or list whether things exist at a place or not.

# import wx

from conf.conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from lib.sentencetokenizer import SentenceTokenizer
from lib.en_to_jp_translator import build_japanese_spacial_noun_phrase, get_copula
# from lib.exercise import Exercise
from lib.nounphrase import NounPhrase
from lib.verbs import Conjugator
# from lib.ui.mainframe import MainFrame


POLITE = True
translate = [
    'The library is behind the university.',
    'The library is beside the supermarket.',
    'The post office is in front of the hospital.',
    'The cafe is inside the hotel.',
    'The bus stop is before the university.',
    'The park is behind the hotel.',
    'The supermarket is beside the library.',
    'The hospital is beside the university.',
    # 'The hospital is between the hotel and the university.'
    # The last needs a conjunction parser
]

title = 'Chapter Four Exercise 2A'
instructions = 'Translate the following into Japanese'


def start_exercise():
    dictionary = load_from_json(
        "{}/dictionary.json".format(DICTIONARY_DIR), 'dictionary'
    )
    prepositions = load_from_json(
        "{}/sources/prepositions.json".format(DICTIONARY_DIR), 'prepositions'
    )
    prep_dictionary = keyed_dictionary(prepositions, 'english')
    st = SentenceTokenizer(dictionary)
    snp = NounPhrase(dictionary, 'subject')
    cnp = NounPhrase(dictionary, 'complement')

    questions = []
    answers = []
    for t in translate:
        questions.append(t.split())
        sentence_parts = st.breakdown(t)
        snp.build_noun_phrase(sentence_parts.subject)
        subject = snp.get_noun_phrase()
        if sentence_parts.copula in ['is', 'am', 'are']:
            predicate = Conjugator(dictionary['to be']).conjugate()
        prep, compl = sentence_parts.extract_preposition(
            prep_dictionary, 'complement'
        )

       complement = build_japanese_spacial_noun_phrase(prep, compl, cnp)
       # print(complement)
    #    answers.append(subject + jcomplement + predicate)
   # app = wx.App()
   # MainFrame(Exercise(title, instructions, questions, answers))
   # app.MainLoop()


if __name__ == '__main__':
    start_exercise()
