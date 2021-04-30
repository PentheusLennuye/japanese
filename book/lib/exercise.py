class Exercise:
    def __init__(self, title, instructions, questions, answers):
        self.title = title
        self.instructions = instructions
        self.questions = questions
        self.answers = answers
        self._set_facts()

    def _set_facts(self):
        self.num_questions = len(self.questions)
