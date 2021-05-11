#!/usr/bin/env python3

# kore wa nan desu ka(これはなんですか): drills on identifying nouns

from conf import DICTIONARY_DIR
from lib.basics import load_from_json, keyed_dictionary
from random import randint, shuffle

print("""
KORE and SORE practice. これとそれの練習
---------------------------------------
You will see the additional terms:
1. 改行(かいぎょう). It means "line break" (i.e., RETURN)
2. 答え(こたえ). It means "answer."
3. 押して(おして). It is the command to "push."
""")

things = ('pen bicycle hat pencil umbrella dictionary bag t-shirt wallet '
          'dictionary notebook shoe watch newspaper library bank cafe '
          'blackboard lights door curtain window chair pencil desk eraser '
          'book').split()
things.append('post office')
jpointers = ('これ:それ', 'それ:これ', 'あれ:あれ')
epointers = ('this:that', 'that:this', 'that over there:that over there')
shuffle(things)

nouns = load_from_json("{}/nouns.json".format(DICTIONARY_DIR), 'nouns')
enouns = keyed_dictionary(nouns, 'english')
for thing in things:
    index = randint(0, 2)
    shitsumon, kotae = jpointers[index].split(':')
    question, answer = epointers[index].split(':')
    entry = enouns[thing]
    if 'kanji' in entry:
        mono = entry['kanji']
        furigana = "({})".format(entry['kana'])
    else:
        mono = entry['kana']
        furigana = None
    input("\nAsk the question: What is {}? Hit RETURN. ".format(question))
    print("{}はなんですか。".format(shitsumon))
    input("\nお答えください。改行を押して。({}) ".format(thing))
    print("{}は{}です。".format(kotae, mono))
    if furigana:
        print(furigana)
