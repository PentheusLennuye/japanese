import wx

JP = 0
EN = 1


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


class JToken(wx.BoxSizer):
    def __init__(self, panel, token, furigana):
        super().__init__(wx.VERTICAL)
        self.token = token
        self.furigana = furigana
        self._set_static_text(panel)

        self.Add(self.get_static_text('f'), 0, wx.LEFT, 0)
        self.Add(self.get_static_text(), 0, wx.CENTER, 0)

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


class QABox(wx.BoxSizer):
    def __init__(self, panel, wordlist, language=JP):
        super().__init__(wx.HORIZONTAL)
        self.language = language
        self.wordlist = wordlist
        self.panel = panel
        self._set_tokens()

    def _set_tokens(self):
        if self.language == JP:
            for word in self.wordlist:
                self.Add(JToken(self.panel, word[0], word[1]), 0, wx.CENTER, 0)
        if self.language == EN:
            for word in self.wordlist:
                self.Add(EToken(self.panel, word), 0, wx.CENTER, 0)
