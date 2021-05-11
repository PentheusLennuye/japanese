

def build_japanese_spacial_noun_phrase(
    epreposition, eprepositional_complement, noun_parser
):
    ''' Convert English spacial preposition modifying a complement into a
        Japanese spacial noun phrase. Forget about adverbs and adjectives
        for now.'''

    noun_parser.build_noun_phrase(epreposition)
    jpreposition = noun_parser.get_noun_phrase()
    jpreposition = jpreposition[0]  # Strip any particle

    noun_parser.build_noun_phrase(eprepositional_complement)
    jprepositional_complement = noun_parser.get_noun_phrase()[0]
    return jprepositional_complement + ['の', ''] + jpreposition


def get_copula(english):
    if english in ['is', 'am', 'are']:
        return ['です', '']
