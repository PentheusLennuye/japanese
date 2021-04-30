#!/usr/bin/env python3
# File: nounphrase.py
#
# Practises minutes

import random


MAXQ = 10

juu = [
    '',
    'じゅう',
    'にじゅう',
    'さんじゅう',
    'よんじゅう',
    'ごじゅう'
]

funpun = [
    'っぷん',
    'いっぷん',
    'にふん',
    'さんぷん',
    'よんぷん',
    'ごふん',
    'ろっぷん',
    'ななふん',
    'はっぷん',
    'きゅうふん',
]
ampm = ('a.m.', 'p.m.')
gozengogo = ('午前', '午後')
ji = [
    '',
    'いちじ',
    'にじ',
    'さんじ',
    'よじ',
    'ごじ',
    'ろくじ',
    'しちじ',
    'はちじ',
    'くじ',
    'じゅうじ',
    'じゅういちじ',
    'じゅうにじ'
]


def start():
    quiz()


def quiz():
    halt = MAXQ
    print("{} questions on time.\n".format(halt))
    i = 0
    while i < halt:
        noon = random.randint(0, 1)
        en_noon = ampm[noon]
        jp_noon = gozengogo[noon]
        hour = random.randint(1, 12)
        tens = random.randint(0, 5)
        ones = random.randint(0, 9)
        q = "{}:{}{} {} in Japanese? ".format(hour, tens, ones, en_noon)
        input(q)
        mae = ''
        if tens > 3 or (tens == 3 and ones > 0):
            mae = '前'
            ones = 10 - ones
            tens = 5 - tens
            hour += 1
            if hour >= 13:
                hour = 1
            minutes = juu[tens] + funpun[ones]
        elif tens == 3 and ones == 0:
            minutes = 'はん'
        elif ones == 0:
            minutes = juu[tens][:-1] + 'っぷん'
        else:
            minutes = juu[tens] + funpun[ones]
        answer = "{} {}{}{}".format(
            jp_noon, ji[hour], minutes, mae
        )
        print(answer)
        i += 1


if __name__ == '__main__':
    start()
