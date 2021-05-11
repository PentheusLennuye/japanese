import wx

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
