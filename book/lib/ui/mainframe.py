#!/usr/bin/env python3.9

import wx
from .georgeui import EN, QABox, ExerciseTitle, ExerciseInstructions


class MainFrame(wx.Frame):
    def __init__(self, exercise):
        super().__init__(parent=None, title='日本語の練習', size=(700, 400))
        self.exercise = exercise
        self.InitUI()

    def InitUI(self):
        self.index = 0
        self._set_layout()
        self._define_buttons()
        self.set_header()
        self.set_qa()
        self.set_control_box()
        self.Show()

    def _set_layout(self):
        self.main_panel = wx.Panel(self)
        self.main_box = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.main_box)

        self.header_panel = wx.Panel(self.main_panel)
        self.header_box = wx.BoxSizer(wx.VERTICAL)
        self.header_panel.SetSizer(self.header_box)

        self.playfield_panel = wx.Panel(self.main_panel)
        self.playfield_panel.SetBackgroundColour((255, 255, 255))
        self.playfield_box = wx.BoxSizer(wx.VERTICAL)
        self.playfield_panel.SetSizer(self.playfield_box)

        self.control_panel = wx.Panel(self.main_panel)
        self.control_box = wx.BoxSizer(wx.VERTICAL)
        self.control_panel.SetSizer(self.control_box)

        self.main_box.Add(self.header_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.main_box.Add(self.playfield_panel, 3, wx.EXPAND | wx.ALL, 5)
        self.main_box.Add(self.control_panel, 1, wx.EXPAND | wx.ALL, 5)

    def _define_buttons(self):
        self.button = wx.Button(self.control_panel, label='答え')
        self.button.Bind(wx.EVT_BUTTON, self.reveal_answer)
        self.quit_button = wx.Button(self.control_panel, label='終わる')
        self.quit_button.SetForegroundColour((240, 80, 80))
        self.quit_button.Bind(wx.EVT_BUTTON, self.end_program)

    def goto_next_question(self, event):
        self.index += 1
        if self.index < self.exercise.num_questions:
            self.set_qa()
            self.playfield_box.Layout()
            self.answer_box.ShowItems(show=False)
            self.button.SetLabel('答え')
            self.button.Bind(wx.EVT_BUTTON, self.reveal_answer)
        else:
            self.button.Hide()

    def reveal_answer(self, event):
        self.answer_box.ShowItems(show=True)
        self.playfield_box.Layout()
        self.button.SetLabel(label='次の質問')
        self.button.Bind(wx.EVT_BUTTON, self.goto_next_question)
        if self.index >= self.exercise.num_questions - 1:
            self.button.Hide()

    def end_program(self, event):
        self.Destroy()

    def set_header(self):
        self._add_to_header_box(
            ExerciseTitle(self.header_panel, self.exercise.title)
        )
        self._add_to_header_box(
            ExerciseInstructions(self.header_panel, self.exercise.instructions)
        )

    def _add_to_header_box(self, item, border=10):
        self.header_box.Add(item, 1, wx.ALL | wx.CENTER, border)

    def set_qa(self):
        self.playfield_box.Clear(True)
        self.question_box = QABox(
            self.playfield_panel,
            self.exercise.questions[self.index],
            EN
        )
        self.answer_box = QABox(
            self.playfield_panel,
            self.exercise.answers[self.index],
        )
        self._add_to_playfield_box(self.question_box)
        self._add_to_playfield_box(self.answer_box)

    def _add_to_playfield_box(self, item, border=2):
        self.playfield_box.Add(item, 1, wx.CENTER,  border)

    def set_control_box(self):
        self.control_box.Add(self.button, 0, wx.CENTER, 5)
        self.control_box.Add(self.quit_button, 0, wx.CENTER, 5)
        self.answer_box.ShowItems(show=False)
        self.Layout()
