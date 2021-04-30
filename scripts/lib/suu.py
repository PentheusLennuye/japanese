#!/usr/bin/env python3

ones = ('', 'ichi', 'ni', 'san', 'yon', 'go', 'roku', 'nana', 'hachi',
        'kyū')
tens = ('', 'jyū', 'nijyū', 'sanjyū', 'yonjyū', 'gojyū', 'rokujyū', 'nanajyū',
        'hachijyū', 'kyūjyū')
hundreds = ('', 'hyaku', 'nihyaku', 'sanbyaku', 'yonhyaku', 'gohyaku',
            'roppyaku', 'nanahyaku', 'happyaku', 'kyūhyaku')
thousands = ('', 'sen', 'nisen', 'sanzen', 'yonsen', 'gosen', 'rokusen',
             'nanasen', 'hassen', 'kyūsen')
tenthousands = ('', 'ichiman', 'niman', 'sanman', 'yonman', 'goman', 'rokuman',
                'nanaman', 'hachiman', 'kyūman', 'jyūman')


def convert_from_arabic(arabic):
    n1 = int(arabic % 10)
    n10 = int((arabic - n1) % 100)
    n100 = int((arabic - (n1 + n10)) % 1000)
    n1000 = int((arabic - (n1 + n10 + n100)) % 10000)
    n10000 = int(arabic - (n1 + n10 + n100 + n1000))
    answer = ''
    for n in [tenthousands[int(n10000/10000)],
              thousands[int(n1000/1000)],
              hundreds[int(n100/100)],
              tens[int(n10/10)],
              ones[n1]]:
        if n:
            answer += ' ' + n
    return answer.strip()


if __name__ == '__main__':
    print(convert_from_arabic(10247))
