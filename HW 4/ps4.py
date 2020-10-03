# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist


def random_word(wordlist):
    return random.choice(wordlist)

def random_string(wordlist, n):
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    alphabet = string.ascii_lowercase + ' '
    result_lower = {}
    result_upper = {}
    for x in range(27):
        result_lower[alphabet[x]] = alphabet[x + shift]
        result_upper[alphabet[x].upper()] = alphabet[x + shift].upper()
        if x + shift == 26:
            shift = shift-27
    result_upper.update(result_lower)
    return result_upper     # returns uppercase letter for space because update() replaces lowercase letter with it


def build_encoder(shift):
    return build_coder(shift)


def build_decoder(shift):
    coder = build_coder(shift)
    decoder = {}
    for x in coder:
        decoder[coder[x]] = x
    return decoder


def apply_coder(text, coder):
    result = ''
    punctuation = string.punctuation
    for x in text:
        if x in punctuation:
            result += x
        else:
            try:
                result += coder[x]
            except KeyError:
                result += ' '
    return result


def apply_shift(text, shift):
    return apply_coder(text, build_encoder(shift))


#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    max_valid_words = 0
    best_shift = 0
    for x in range(27):
        shifted_text = apply_coder(text, build_decoder(x))
        shifted_text = shifted_text.split()
        counter = 0
        for y in shifted_text:
            # print('y', y)
            if is_word(wordlist, y):
                counter += 1
        if counter > max_valid_words:
            max_valid_words = counter
            best_shift = x
        # print('counter', counter)
    return best_shift


#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    for x in shifts:
        text_pre = text[:x[0]]
        text_after = text[x[0]:]
        text = text_pre + apply_coder(text_after, build_encoder(x[1]))
    return text
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    best_shifts = []
    for x in range(27):
        shifted_text = apply_coder(text, build_decoder(x))
        split_shifted_text = shifted_text.split()
        counter = 0
        for y in split_shifted_text:
            if is_word(wordlist, y):
                counter += 1
        if counter > 0:
            best_shifts += [shifted_text]
    for x in best_shifts:
        # space = x.find(' ')
        result = find_best_shifts_rec(wordlist, x, 0)
        if result is not None:
            return result


def find_best_shifts_rec(wordlist, text, start):
    # print('text', text)
    best = find_best_shift(wordlist, text[start:])
    # print('best', best)
    decoded = apply_coder(text[start:], build_decoder(best))
    s = text[:start] + decoded[:]
    # print('before start', text[:start])
    # print('decoded', decoded)
    if ' ' in s[start:]:
        st = s[start:].find(' ')+1+len(s[:start])
        print(s)
        print('s', s[start:])
        print('start', s[start:])
        print('best', best)
        return [(start, best)] + find_best_shifts_rec(wordlist, s, st)  # [text[start:].find(' '),
    else:
        for x in s:
            if is_word(wordlist, x) is False:
                print('dog')
                return [None]
        return [(start, best)]


# statement = "JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?"
# shifts = find_best_shifts(wordlist, statement)
# print(apply_shifts(statement, shifts))


def decrypt_fable():
    story = get_fable_string()
    best_shift = find_best_shift(wordlist, story)
    return apply_shift(story, best_shift)
print(decrypt_fable())

    
#What is the moral of the story?
#
#
#
#
#
