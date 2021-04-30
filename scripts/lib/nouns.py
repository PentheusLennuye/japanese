
silent_h = ['honour', 'honourable', 'herb']


def is_plural(word):
    if word[-1] != 's':
        return False
    elif word[-2] == 's':
        return False
    else:
        return True


def get_article(word, indefinite=True, pointer=None):
    if indefinite:
        return get_indefinite_article(word)
    return get_definite_article(word, pointer)


def get_indefinite_article(word):
    if is_plural(word):
        return ''
    if word in silent_h:
        return 'an'
    first_letter = word[0].lower()
    if first_letter in ('a', 'e', 'i', 'o', 'u'):
        return 'an'
    else:
        return 'a'


def get_definite_article(word, pointer=None):
    pointers = {'this': 'these', 'that': 'those'}
    if pointer is None:
        return 'the'
    if not is_plural(word):
        return pointer
    return pointers[pointer]
