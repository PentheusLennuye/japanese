#!/usr/bin/env python3

import re
from lib.numbers import JNumber
from lib.noun import NounPhrase

re_timestamp = re.compile(r'(\d{1,2}):?(\d\d)?([ap]m)?')
G_HOUR = 1
G_MINUTES = 2
G_MERIDIAN = 3


class InvalidTimeError(Exception):
    pass


class Time:
    def __init__(self, timestamp, noun_dict=None):
        self.timestamp = timestamp
        self.noun_dict = noun_dict
        self.noun = None
        self.particle = ['', '']
        self.meridian = ['', '']
        if timestamp[0] in '123456789':
            match = re_timestamp.match(timestamp)
            if match:
                self._set_clock_time(match)
            else:
                raise InvalidTimeError
        else:
            self._set_noun_time()

    def get_time(self):
        return self.noun, self.particle

    def _set_noun_time(self):
        self.noun = NounPhrase(
            self.noun_dict, self.timestamp
        ).get_noun()[0]  # returns ['日曜日', 'にちようび']
        if self.noun[0][0] in '日月火水木金土一二三四五六七八九十':
            self.particle = ['に', '']

    def _set_clock_time(self, match):
        self.particle = ['に', '']
        self._set_hour(match)
        self._set_minutes(match)
        self._set_meridian(match)

        hour = JNumber(self.hour, 'hour')
        minutes = JNumber(self.minutes, 'minutes')
        khours, fhours = hour.get_units()
        kminutes, fminutes = minutes.get_units()
        self.noun = [self.meridian[0] + khours + kminutes,
                     self.meridian[1] + fhours + fminutes]

    def _set_hour(self, match):
        if not match.group(1):
            raise InvalidTimeError
        self.hour = int(match.group(1))
        if self.hour < 0 or self.hour > 23:
            raise InvalidTimeError

    def _set_minutes(self, match):
        if match.group(2):
            self.minutes = int(match.group(2))
        else:
            self.minutes = 0
        if self.minutes < 0 or self.minutes > 59:
            raise InvalidTimeError

    def _set_meridian(self, match):
        meridians = {
            'pm': ['午後', 'ごご'],
            'am': ['午前', 'ごぜん']
        }
        if not match.group(3):
            return
        meridian = match.group(3)
        if meridian not in ['am', 'pm']:
            raise InvalidTimeError
        self.meridian = meridians[meridian]


if __name__ == '__main__':
    timestamp = '8:10pm'
    print(Time(timestamp).get_time())
