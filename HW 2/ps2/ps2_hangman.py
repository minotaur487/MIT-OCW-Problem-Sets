# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print( "  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
word = choose_word(wordlist)
guesses = 26
word_length = len(word)
letters = string.ascii_lowercase
cumulative = [" "]*word_length
show = []
for x in range(word_length):
    show += ['_']
    show += [' ']
print("Welcome to the game, Hangman!")
print("I am thinking of a word that is", word_length, "letters long.")

def p_guess(guess, word, show, num, cu):
    if guess in word:
        i, z = 0, 0
        for x in list(word):
            if guess == x:
                show[i] = guess
                cu[z] = guess
            i += 2
            z += 1
        show = ''.join(show)
        print("Good Guess:", show)
        return show, num, cu
    else:
        show = ''.join(show)
        print("Oops! That letter is not in my word:", show)
        return show, num-1, cu


def available_letters(g, l):
    l = list(l)
    if g in l:
        l.remove(g)
        return ''.join(l)
    else:
        print("You already guessed this!")
        return ''.join(l)


while guesses != 0 and word != ''.join(cumulative):
    print()
    print("You have", guesses, "guesses left.")
    print("Available letters:", letters)
    while True:
        g = input("Please guess a letter: ").lower()
        if len(g) == 1 and g != " ":
            break
    show, guesses, cumulative = p_guess(g, word, show, guesses, cumulative)
    show = list(show)
    letters = available_letters(g, letters)
print()
if guesses == 0 and word != ''.join(cumulative):
    print("Guess you lost")
else:
    print("Congratulations, you won!")
