#!/usr/bin/env python3.9

import wx

EN = 2
JP = 0

class STBox(wx.BoxSizer):
    '''
    A vertical Box with main text and optional gloss.
    It receives a panel, and a list of 2-ples (main, gloss) or a list of
    strings.
    '''
    def __init__(self, panel, pair):
        super().__init__(wx.VERTICAL)
        self.pair = pair
        self.panel = panel
        self.gfont = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self.gfont.SetPointSize(8)
        self.mfont = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self.mfont.SetPointSize(14)
        self._set()

    def _set(self):
        if isinstance(self.pair, str):
            label = self.pair
        elif isinstance(self.pair, list):  # List means there is a gloss
            label = self.pair[0]
            gloss = wx.StaticText(self.panel, label=self.pair[1])
            gloss.SetForegroundColour((0, 0, 0))
            gloss.SetFont(self.gfont)
            self.Add(gloss, 0, wx.ALL|wx.ALIGN_LEFT, 0)
        else:
            raise ValueError('pair must be list of lists or strings')

        maintext = wx.StaticText(self.panel, label=label)
        maintext.SetForegroundColour((0, 0, 0))
        maintext.SetFont(self.mfont)

        self.Add(maintext, 0, wx.ALL|wx.ALIGN_CENTER, 0)


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


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='日本語の練習', size=(700, 400))
        
        self.playfield = Playfield(self)

        self.playfield.setQuestion(
            'The library is behind the university.'.split(),
            EN
        )

        self.playfield.setAnswer(
            [['図書館', 'としょかん'], ['は', ''], ['大学', 'だいがく'],
            ['の',''], ['後ろ','うし'], ['です','']],
            JP
        )
        self.playfield.Layout()
        self.Show()


def start_exercise():
    app = wx.App()
    MainFrame()
    app.MainLoop()


if __name__ == '__main__':
    start_exercise()
