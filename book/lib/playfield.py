
import wx

from .stbox import STBox

EN = 2
JP = 0


class Playfield:
    def __init__(self, panel):
        self.panel = wx.Panel(panel)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.box)
        self.panel.SetBackgroundColour((255, 255, 255))
        self.question_box = wx.BoxSizer(wx.HORIZONTAL)
        self.answer_box = wx.BoxSizer(wx.HORIZONTAL)

    def setQuestion(self, fields, lang=JP):
        '''
        Sets up the horizontal question box with a label for each field.
        Lang is an integer representing the language, and
        sets the border between StaticText widgets.
        '''
        for field in fields:
            self.question_box.Add(STBox(self.panel, field),
                                  0,
                                  wx.ALL|wx.ALIGN_CENTER,
                                  lang)

    def setAnswer(self, fields, lang=JP):
        '''
        Sets up the horizontal question box with a label for each field.
        Lang is an integer representing the language, and
        sets the border between StaticText widgets.
        '''
        for field in fields:
            self.answer_box.Add(STBox(self.panel, field),
                                0,
                                wx.ALL|wx.ALIGN_CENTER,
                                lang)

    def Layout(self):
        self.box.Add(self.question_box, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        self.box.Add(self.answer_box, 0, wx.ALL|wx.ALIGN_CENTER, 10)
