def build_japanese_spacial_noun_phrase(simplesentence, noun_parser):
    ''' Convert English spacial preposition modifying a complement into a
        Japanese spacial noun phrase. Forget about adverbs and adjectives
        for now.'''
    preposition, complement = simplesentence.split_on_preposition('complement')
    noun_parser.build_noun_phrase(complement)
    result = [noun_parser.get_noun_phrase()[0]]  # No particle
    result.append(['の', ''])

    # This takes some explaining. An English preposition is a Japanese
    # noun.
    noun_parser.build_noun_phrase(' '.join(preposition))  # JP Noun
    result.append(noun_parser.get_noun_phrase()[0])
    return result


def get_copula(english):
    if english in ['is', 'am', 'are']:
        return 
