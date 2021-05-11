class SimpleSentence:
    def __init__(self, subject=None, predicate=None, direct_object=None,
                 indirect_object=None, copula=None, complement=None):
        self.subject = subject
        self.predicate = predicate
        self.copula = copula
        self.direct_object = direct_object
        self.indirect_object = indirect_object
        self.complement = complement
        self.pos = {
            'complement': self.complement,
            'subject': self.subject,
            'direct_object': self.direct_object,
            'indirect_object': self.indirect_object
        }

    def console(self):
        print("SimpleSentence / Clause:")
        if self.predicate:
            print("Subject: {}; Predicate: {}; Direct Object: {}".format(
                self.subject, self.predicate, self.direct_object))
            print("Indirect Object: {}, Complement".format(
                self.indirect_object, self.complement))
        else:
            print("Subject: {}; Copula: {}; Complement: {}".format(
                self.subject, self.copula, self.complement))

    def extract_preposition(self, prep_dict, part_of_sentence='complement'):
        ''' returns (preposition, complement) from a noun phrase '''
        segment = self.pos[part_of_sentence].split()
        i = len(segment)
        while i > 0:
            search = ' '.join(segment[0:i])
            if search in prep_dict:
                return search, ' '.join(segment[i:])
            i -= 1
        return None, ' '.join(segment)


class CompoundSentence:
    def __init__(self, first_clause, coordinating_conjunction, second_clause):
        self.first_clause = first_clause
        self.second_clause = second_clause
        self.coordinating_conjunction = coordinating_conjunction

    def console(self):
        print("CompoundSentence:")
        self.first_clause.console()
        print(self.coordinating_conjunction)
        self.second_clause.console()


class ComplexSentence:
    def __init__(self, independent_clause, subordinating_conjunction,
                 subordinate_clause):
        self.independent_clause = independent_clause
        self.subordinate_clause = subordinate_clause
        self.subordinating_conjunction = subordinating_conjunction

    def console(self):
        print("ComplexSentence:")
        self.independent_clause.console()
        print(self.subordinating_conjunction)
        self.subordinate_clause.console()


class CompoundComplexSentence:
    def _init__(self):
        raise NotImplementedError
