#!/usr/bin/env python3
# suu.py
#
# Quiz for Japanese numbers up to 90,000. This is *not* the hitotsu system,
# obviously.

import random
import sys

DEFAULT_ITERATIONS = 10
TOPNUM = 100000

ones = ('', 'ichi', 'ni', 'san', 'shi', 'go', 'roku', 'shichi', 'hachi',
        'kyū')
tens = ('', 'jyū', 'nijyū', 'sanjyū', 'yonjyū', 'gojyū', 'rokujyū', 'nanajyū',
        'hachijyū', 'kyūjyū')
hundreds = ('', 'hyaku', 'nihyaku', 'sanbyaku', 'yonhyaku', 'gohyaku',
            'roppyaku', 'nanahyaku', 'happyaku', 'kyūhyaku')
thousands = ('', 'sen', 'nisen', 'sanzen', 'yonsen', 'gosen', 'rokusen',
             'nanasen', 'hassen', 'kyūsen')
tenthousands = ('', 'ichiman', 'niman', 'sanman', 'yonman', 'goman', 'rokuman',
                'nanaman', 'hachiman', 'kyūman', 'jyūman')


def start():
    if len(sys.argv) <= 1:
        max_iterations = DEFAULT_ITERATIONS
    else:
        try:
            max_iterations = int(sys.argv[1])
        except ValueError:
            print("Argument must be an integer.")
            usage()
            sys.exit(1)
    i = 0
    print("{} questions.".format(max_iterations))
    while i < max_iterations:
        i += 1
        pose()


def usage():
    print("Usage: {} [number_of_questions]".format(sys.argv[0]))


def pose():
    arabic = random.randint(1, TOPNUM)  # Zero is 'zero' or 'rei.' Yawn.
    nihongo = get_nihongo(arabic)
    direction = random.randint(0, 1)
    if direction:
        input(' '.join(nihongo))
        print(arabic)
    else:
        input(arabic)
        print(' '.join(nihongo))
    print()


def get_nihongo(arabic):
    n1 = int(arabic % 10)
    n10 = int((arabic - n1) % 100)
    n100 = int((arabic - (n1 + n10)) % 1000)
    n1000 = int((arabic - (n1 + n10 + n100)) % 10000)
    n10000 = int(arabic - (n1 + n10 + n100 + n1000))
    nihongo = [tenthousands[int(n10000/10000)],
               thousands[int(n1000/1000)],
               hundreds[int(n100/100)],
               tens[int(n10/10)],
               ones[n1]]
    return(nihongo)


if __name__ == '__main__':
    start()
