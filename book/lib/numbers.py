#!/usr/bin/env python3

jnumerals = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
jkana = {
            '一': 'いち',
            '二': 'に',
            '三': 'さん',
            '四': 'よん',
            '五': 'ご',
            '六': 'ろく',
            '七': 'なな',
            '八': 'はち',
            '九': 'きゅう',
            '十': 'じゅう'
        }
junits = {
        'hour': {'四': 'よじ', '九': 'くじ'},
        'minutes': {'一': 'いっぷん', '三': 'さんぷん', '四': 'よんぷん',
                    '六': 'ろっぷん', '八': 'はっぷん', '九': 'きゅふん',
                    '十': 'じゅっぷん'},
        'people': {'一': 'ひとり', '二': 'ふたり'},
        'flat objects': {'四': 'よんまい'}
        }
jcounters = {
        'hour': {'kanji': '時', 'kana': 'じ'},
        'minutes': {'kanji': '分', 'kana': 'ふん'},
        'people': {'kanji': 'じん', 'kana': 'にん'},
        'flat objects': {'kanji': '枚', 'kana': 'まい'}
        }


class JNumber:
    def __init__(self, number, units=None):
        self.number = int(number)
        self.units = units
        self.kanji = ''
        self.furigana = ''
        self.counter = {}

        self._set_text(self.number)
        if self.kanji[-1] == '四':
            self.furigana = self.furigana[:-2] + 'し'
        elif self.kanji[-1] == '七':
            self.furigana = self.furigana[:-2] + 'しち'
        self._set_counter()

    def get_number(self):
        return [self.kanji, self.furigana]

    def get_units(self):
        if not self.units or self.units not in junits:
            return [self.kanji, self.furigana]
        lastchar = self.kanji[-1]
        if lastchar in junits[self.units]:
            w_furigana = self.furigana[:-3] + junits[self.units][lastchar]
        else:
            w_furigana = self.furigana + self.counter['kana']
        w_kanji = self.kanji + self.counter['kanji']
        return [w_kanji, w_furigana]

    def _set_text(self, w_number):
        if w_number >= 100000000:  # Hundred million
            hundred_millions = int(w_number / 100000000)
            self._set_text(hundred_millions)
            w_number -= hundred_millions * 100000000
            self.kanji += '億'
            self.furigana += 'おく'
        if w_number >= 10000:
            ten_thousands = int(w_number / 10000)
            self._set_text(ten_thousands)
            w_number -= ten_thousands * 10000
            self.kanji += '万'
            self.furigana += 'まん'
        if w_number >= 1000:
            thousands = int(w_number / 1000)
            self._set_text(thousands)
            w_number -= thousands * 1000
            self._set_thousands(thousands)
        if w_number >= 100:
            hundreds = int(w_number / 100)
            self._set_text(hundreds)
            w_number -= hundreds * 100
            self._set_hundreds(hundreds)
        if w_number >= 10:
            tens = int(w_number / 10)
            self._set_text(tens)
            w_number -= tens * 10
            self._set_tens(tens)
        if w_number != 0:
            try:
                self.kanji += jnumerals[w_number]
                self.furigana += jkana[jnumerals[w_number]]
            except IndexError:
                print("w_number is " + str(w_number))
                raise IndexError

    def _set_thousands(self, thousands):
        if thousands == 1:
            self.kanji = self.kanji[:-1]  # No ichisen
            self.furigana = self.furigana[:-2]
        if thousands == 8:
            self.furigana = self.furigana[:-1]  # No hyakusen
        self.kanji += '千'
        if thousands == 3:
            self.furigana += 'ぜん'
        elif thousands == 8:
            self.furigana += 'っせん'
        else:
            self.furigana += 'せん'

    def _set_hundreds(self, hundreds):
        if hundreds == 1:
            self.kanji = self.kanji[:-1]  # No ichihyaku
            self.furigana = self.furigana[:-2]
        elif hundreds in [6, 8]:
            self.furigana = self.furigana[:-1]  # No rokuhyaku or hachihyaku
        self.kanji += '百'
        if hundreds == 3:
            self.furigana += 'びゃく'
        elif hundreds in [6, 8]:
            self.furigana += 'っぴゃく'
        else:
            self.furigana += 'ひゃく'

    def _set_tens(self, tens):
        if tens == 1:
            self.kanji = self.kanji[:-1]  # No ichijuu
            self.furigana = self.furigana[:-2]
        self.kanji += '十'
        self.furigana += 'じゅう'

    def _set_counter(self):
        if self.units in jcounters:
            self.counter = jcounters[self.units]


if __name__ == '__main__':
    y = JNumber(9, 'hour')
    print(y.get_number())
    print(y.get_units())
