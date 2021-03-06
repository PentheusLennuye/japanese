#!/usr/bin/env python3

import json
import shutil


def load_from_json(path, word_type):
    try:
        with open(path) as fp:
            db = json.load(fp)[word_type]
    except FileNotFoundError:
        print("No dictionary found at {}. I will create a new one. "
              "CTRL-C to cancel")
        db = []
    return db


def save_to_json(path, db):
    try:
        shutil.copy(path, '{}.bak'.format(path))
    except FileNotFoundError:
        pass
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(db, fp, ensure_ascii=False)


def get_basics(cur_chapter):
    english = ''
    while english == '':
        english = input("English word (or STOP to quit): ").strip()
    if english == 'STOP':
        return False, False, False, False, False
    kana = input("Kana: ").strip()
    kanji = input("Kanji: ").strip()
    if kanji == '':
        kanji = None
    chapter = input("Chapter [{}]: ".format(cur_chapter).strip())
    if chapter == '':
        chapter = cur_chapter
    else:
        cur_chapter = chapter
    return english, kana, kanji, chapter, cur_chapter


def build_entry(english, kana, kanji, chapter, particle, vtype):
    entry = {'english': english,
             'kana': kana,
             'chapter': chapter,
             }
    if kanji:
        entry['kanji'] = kanji
    return entry


def confirm(entry):
    confirm = build_confirm(entry)
    response = None
    while response not in ('', 'y', 'Y', 'n', 'N'):
        response = input(confirm).strip()
    if response not in ('', 'y', 'Y'):
        return False
    return True


def build_confirm(entry):
    confirm = entry['english'] + ': '
    if 'particle' in entry:
        confirm += entry['particle'] + ' '
    if 'kanji' in entry:
        confirm += "{} ({})".format(entry['kanji'], entry['kana'])
    else:
        confirm += entry['kana']
    if 'type' in entry:
        confirm += ", {}-type".format(entry['type'])
    if 'positivity' in entry:
        confirm += ", {}".format(
            ['negative', 'positive'][entry['positivity']]
        )
    confirm += ", ch. " + entry['chapter']
    confirm += "[Y/n] "
    return confirm


def keyed_dictionary(db, searchkey):
    new_db = {}
    for entry in db:
        key = searchkey
        if key == 'kanji' and key not in entry:
            key = 'kana'
        new_db[entry[key]] = {}
        keys = list(entry.keys())
        for k in keys:
            new_db[entry[key]][k] = entry[k]
    return new_db


def get_furigana(entry):
    if 'kanji' not in entry:
        return None
    if entry['english'] == 'to come':
        return '???'
    kana = entry['kana']
    kanji = entry['kanji']
    i = 0
    while i < len(kanji) and i < len(kana):
        if kana[-(1 + i)] == kanji[-(1 + i)]:
            i += 1
        else:
            break
    if i > 0:
        return kana[0:-i]
    return kana


def get_kanji(entry, verb=False):
    if 'kanji' in entry:
        if not verb:
            return entry['kanji']

    else:
        return get_kana(entry)


def get_kana(entry):
    return entry['kana']


def searchtree(searchitem, path, node, nodename):
    ''' Returns a reversed list of node names to the found item '''
    if isinstance(node, dict):
        nodenames = list(node.keys())
        for nodename in nodenames:
            if searchtree(searchitem, path, node[nodename], nodename):
                path.append(nodename)
                return True
    elif isinstance(node, list):
        if searchitem in node:
            return True
        return False
    return False
