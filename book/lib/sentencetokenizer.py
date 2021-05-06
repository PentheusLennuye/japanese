from .sentence import CompoundSentence, ComplexSentence, SimpleSentence

DEBUG = False


class InvalidSentenceError(Exception):
    pass


class IllegalAdverbError(Exception):
    pass


class SentenceTokenizer:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.articles = ['a', 'an', 'the']
        self.copulae = ['is', 'am', 'are']  # for now
        self.conjunctions = 'and or because since'.split()
        self.coordinating_conjunctions = ['and', 'or']
        self.subordinating_conjunctions = ['because', 'since']

    def breakdown(self, sentence):
        '''
        The post office is in front of the hospital and it is ugly.
        becomes:
        CompoundSentence
            first_clause:
                SimpleSentence
                    subject: the post office
                    copular: is
                    complement: in front of the hospital
            second_clause:
                SimpleSentence
                    subject: it
                    copular: is
                    complement: ugly
            coordinating_conjunction: and
        '''
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        independent_clause, remainder = self.pop_clause(sentence)
        if remainder == '':
            return independent_clause
        conjunction, remainder = self.pop_conjunction(remainder)
        if conjunction in self.coordinating_conjunctions:
            second_clause, remainder = self.pop_clause(remainder)
            return CompoundSentence(independent_clause, conjunction,
                                    second_clause)
        elif conjunction in self.subordinating_conjunctions:
            subordinate_clause, remainder = self.pop_clause(remainder)
            return ComplexSentence(independent_clause, conjunction,
                                   subordinate_clause)
        else:
            raise InvalidSentenceError(sentence)

    def pop_clause(self, sentence):
        subject, remainder = self.pop_subject(sentence)
        predicate, remainder = self.pop_predicate(remainder)
        if predicate:
            # direct_object, remainder = self.pop_direct_object(remainder)
            # indirect_object, remainder = self.pop_indirect_object(remainder)
            # complement, remainder = self.pop_complement(remainder)
            direct_object = None
            indirect_object = None
            complement = None
            copula = None
        else:
            copula, remainder = self.pop_copula(remainder)
            complement, remainder = self.pop_complement(remainder)
            direct_object = None
            indirect_object = None
        return SimpleSentence(subject, predicate, direct_object,
                              indirect_object, copula, complement), remainder

    def pop_subject(self, subsentence):
        ''' Basically, everything up to a predicate, or an abverb chain leading
            to a predicate or copula is the subject '''
        tokens = subsentence.split()
        limit = len(tokens)
        i = 0
        while i < limit:
            if tokens[i] in self.copulae:
                return ' '.join(tokens[:i]), ' '.join(tokens[i:])
            if tokens[i] in self.dictionary:
                pos = self.dictionary[tokens[i]]['pos']
                if pos == 'verb':
                    return ' '.join(tokens[:i-1]), ' '.join(tokens[i:])
                if pos in self.copulae:
                    return ' '.join(tokens[:i-1]), ' '.join(tokens[i:])
                if pos == 'adverb':
                    if self.target_of_adverb(tokens[i+1:]) == 'verb':
                        return ' '.join(tokens[:i-1]), ' '.join(tokens[i:])
            i += 1
        raise InvalidSentenceError(subsentence)

    def target_of_adverb(self, tokens):
        '''Recursively go through a series of adverbs until a non-adverb is
           found.'''
        if tokens[0] in self.copulae:
            return 'copular'
        pos = self.dictionary[tokens[0]]['pos']
        if pos not in ['adjective', 'adverb', 'verb']:
            raise IllegalAdverbError(' '.join(tokens))
        if pos != 'adverb':
            return pos
        if len(tokens) <= 1:
            raise InvalidSentenceError
        return self.target_of_adverb(tokens[1:])

    def pop_predicate(self, subsentence):
        tokens = subsentence.split()
        limit = len(tokens)
        i = 0
        while i < limit:
            if tokens[i] in self.copulae:
                return None, subsentence
            if tokens[i] in self.dictionary:
                pos = self.dictionary[tokens[i]]['pos']
                if pos not in ['verb', 'adverb']:
                    return ' '.join(tokens[:i]), ' '.join(tokens[i:])
                if pos == 'adverb':
                    if self.target_of_adverb(tokens[i+1:]) != 'verb':
                        return ' '.join(tokens[:i]), ' '.join(tokens[i:])
            i += 1
        return ' '.join(tokens), ''  # Intransitive (i.e. no object)

    def pop_copula(self, subsentence):
        tokens = subsentence.split()
        limit = len(tokens)
        i = 0
        while i < limit:
            if tokens[i] in self.dictionary:
                pos = self.dictionary[tokens[i]]['pos']
                if pos == 'adverb':
                    if self.target_of_adverb(tokens[i+1:]) != 'copular':
                        return ' '.join(tokens[:i]), ' '.join(tokens[i:])
                if pos == 'verb':
                    raise InvalidSentenceError
            if tokens[i] not in self.copulae:
                return ' '.join(tokens[:i]), ' '.join(tokens[i:])
            i += 1
        # Intransitive (e.g. "Is George there?" "He is!")
        return ' '.join(tokens), ''

    def pop_direct_object(self, subsentence):
        raise NotImplementedError

    def pop_indirect_object(self, subsentence):
        raise NotImplementedError

    def pop_complement(self, subclause):
        '''Anything remaining in a clause up to a conjunction
           is a complement'''
        tokens = subclause.split()
        limit = len(tokens)
        i = 0
        while i < limit:
            if tokens[i] in self.conjunctions:
                return ' '.join(tokens[:i]), ' '.join(tokens[i:])
            i += 1
        return ' '.join(tokens), ''  # Just a simple sentence, no conjunction

    def pop_conjunction(self, subclause):
        tokens = subclause.split()
        if tokens[0] in self.conjunctions:
            return tokens[0], ' '.join(tokens[1:])
        return None, subclause
