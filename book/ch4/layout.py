#!/usr/bin/env python3.9

import wx

from lib.playfield import Playfield

EN = 2
JP = 0


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
