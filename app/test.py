#!/usr/bin/env python3.9

import wx


class NoKanjiNoFuriganaError(Exception):
    pass


class StaticBlock(wx.StaticText):
    def __init__(self, panel, label):
        super().__init__(panel, label=label)
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)


class ExerciseTitle(StaticBlock):
    def __init__(self, panel, label):
        super().__init__(panel, label=label)
        self.font.SetFractionalPointSize(24)
        self.SetFont(self.font)


class ExerciseInstructions(StaticBlock):
    def __init__(self, panel, label):
        super().__init__(panel, label=label)
        self.font.SetFractionalPointSize(12)
        self.SetFont(self.font)


class EToken(StaticBlock):
    def __init__(self, panel, label):
        super().__init__(panel, label=label)
        self.font.SetFractionalPointSize(16)
        self.SetFont(self.font)
        self.Wrap(0)


class JToken():
    def __init__(self, panel, token, furigana):
        self.token = token
        self.furigana = furigana
        self._set_static_text(panel)

    def get_furigana(self):
        return self.furigana

    def get_token(self):
        return self.token

    def get_static_text(self, selection='t'):
        if selection == 't':
            return self.st_token
        elif selection == 'f':
            return self.st_furigana
        else:
            raise NoKanjiNoFuriganaError

    def _set_static_text(self, panel):
        self.st_furigana = wx.StaticText(panel, label=self.furigana)
        f_font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        f_font.SetFractionalPointSize(9)
        self.st_furigana.SetFont(f_font)
        t_font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        t_font.SetFractionalPointSize(24)
        self.st_token = wx.StaticText(panel, label=self.token)
        self.st_token.SetFont(t_font)


class JWord(JToken):
    def __init__(self, panel, token, furigana):
        super().__init__(panel, token, furigana)


class JMarker(JToken):
    def __init__(self, panel, furigana):
        super().__init__(panel, furigana, '')


class JWordBox(wx.BoxSizer):

    def __init__(self, word, marker):
        super().__init__(wx.HORIZONTAL)
        self.word = word
        self.marker = marker
        self._init()

    def _init(self):
        word_box = wx.BoxSizer(wx.VERTICAL)
        word_box.Add(self.word.get_static_text('f'), 0, wx.CENTER, 0)
        word_box.Add(self.word.get_static_text(), 0, wx.CENTER, 0)
        self.Add(word_box, 0, wx.ALL, 0)

        marker_box = wx.BoxSizer(wx.VERTICAL)
        marker_box.Add(self.marker.get_static_text('f'), 0, wx.CENTER, 0)
        marker_box.Add(self.marker.get_static_text(), 0, wx.CENTER, 0)
        self.Add(marker_box, 0, wx.ALL, 0)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='日本語の練習', size=(500, 500))
        self.InitUI()

    def InitUI(self):
        main_panel = wx.Panel(self)
        self.main_box = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(self.main_box)

        header_panel = wx.Panel(main_panel)
        self.header_box = wx.BoxSizer(wx.VERTICAL)
        header_panel.SetSizer(self.header_box)

        playfield_panel = wx.Panel(main_panel)
        playfield_panel.SetBackgroundColour((255, 255, 255))
        self.playfield_box = wx.BoxSizer(wx.VERTICAL)
        playfield_panel.SetSizer(self.playfield_box)

        # Title
        title = "Chapter Three Exercise 1B (b)"

        # Instructions
        instructions = ("Create a valid sentence in present indicative form "
                        "with the given terms.")

        # Question Box ----------------------------
        question_box = wx.BoxSizer(wx.HORIZONTAL)
        for word in ['study', ', ', 'Japanese (language)', ', ', 'library']:
            question_box.Add(EToken(playfield_panel, word), 0, wx.CENTER, 0)

        # Answer Box ------------------------------
        place = JWord(playfield_panel, '図書館', 'としょかん')
        dir_object = JWord(playfield_panel, '日本語', 'にほんご')
        predicate = JWord(playfield_panel, '勉強します', 'べんきょうします')

        answer_box = wx.BoxSizer(wx.HORIZONTAL)
        for subphrase in [(place, 'で'), (dir_object, 'を'), (predicate, '')]:
            answer_box.Add(
                JWordBox(subphrase[0], JMarker(playfield_panel, subphrase[1])),
                0, wx.ALL, 0
            )

        self._add_to_header_box(ExerciseTitle(header_panel, title))
        self._add_to_header_box(ExerciseInstructions(header_panel,
                                                     instructions))
        self._add_to_playfield_box(question_box)
        self._add_to_playfield_box(answer_box)

        self.main_box.Add(header_panel, 1, wx.EXPAND | wx.ALL, 10)
        self.main_box.Add(playfield_panel, 3, wx.EXPAND | wx.ALL, 10)
        self.Show()

    def _add_to_header_box(self, item, border=10):
        self.header_box.Add(item, 1, wx.ALL | wx.CENTER, border)

    def _add_to_playfield_box(self, item, border=10):
        self.playfield_box.Add(item, 1, wx.ALL | wx.CENTER,  border)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
