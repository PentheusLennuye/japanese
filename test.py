#!/usr/bin/env python3.9

import wx
from ui.mainframe import MainFrame


class Exercise:
    def __init__(self, title, instructions, questions, answers):
        self.title = title
        self.instructions = instructions
        self.questions = questions
        self.answers = answers
        self._set_facts()

    def _set_facts(self):
        self.num_questions = len(self.questions)


if __name__ == '__main__':
    title = "Chapter Three Exercise 1B (b)"
    instructions = ("Create a valid sentence in present indicative form "
                    "with the given terms.")
    questions = [
        ['study', ', ', 'Japanese (language)', ', ', 'library'],
        ['listen', ', ', 'music', ', ', 'home']
    ]
    answers = [
        [['図書館', 'としょかん'], ['で', ''], ['日本語', 'にほんご'],
         ['を', ''], ['勉強します', 'べんきょうします']],
        [['内', 'うち'], ['で', ''], ['音楽', 'おんがく'],
         ['を', ''], ['聞きます', 'ききます']]
    ]
    e = Exercise(title, instructions, questions, answers)

    app = wx.App()
    frame = MainFrame(e)
    app.MainLoop()
