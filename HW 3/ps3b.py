from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    # print(f'hand {hand}')
    permutations = []
    for x in range(1, HAND_SIZE+1):
        permutations += get_perms(hand, x)
    # print('perm', permutations)
    score = 0
    answer = ''
    for guess in permutations:
        if guess in word_list:
            if get_word_score(guess, HAND_SIZE) > score:
                answer = guess
                # print(answer)
                score = get_word_score(guess, HAND_SIZE)
    if score == 0:
        answer = None
        return answer
    return answer
# hand = {'a': 2, 'p': 1, 'm': 1, 'z': 1, 'j': 1}
# print(type(comp_choose_word(hand, load_words())))


#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...    
    score = 0
    print('Hand: ', end='')
    display_hand(hand)
    u_hand = hand.copy()
    # print('u_hand', u_hand)
    response = comp_choose_word(u_hand, word_list)
    print(response)
    while hand != {} and response is not None:
        # print(f'response: {type(response)}')
        u_hand = update_hand(u_hand, response)
        score += get_word_score(response, len(hand))
        print(f'Word Score: {get_word_score(response, len(hand))} \n'
              f'Hand:', end=' ')
        display_hand(u_hand)
        response = comp_choose_word(u_hand, word_list)
    print(f'Hand Score: {score}')
    return score

#{'i': 2, 's': 1, 'y': 1, 'z': 2, 'p': 1}
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    score = 0
    decision = 'start'
    hand = {}
    sub_decision = ''
    while decision == 'n' or decision == 'r' or decision == 'start':
        while decision != 'e' and decision != 'n' and decision != 'r':
            decision = input(
                f'Input \'n\' for a new hand, \'r\' to play the last hand again, and \'e\' to exit the game')
        if decision == 'e':
            print(f'Final Score: {score}')
            return
        elif decision == 'n':
            hand = deal_hand(HAND_SIZE)
            while sub_decision != 'u' and sub_decision != 'c':
                sub_decision = input('Input \'u\' to play the hand yourself or'
                                     ' input \'c\' for the computer to play the hand')
            if sub_decision == 'u':
                score += play_hand(hand, word_list)
            elif sub_decision == 'c':
                score += comp_play_hand(hand, word_list)
        elif decision == 'r':
            while sub_decision != 'u' and sub_decision != 'c':
                sub_decision = input('Input \'u\' to play the hand yourself or'
                                     ' input \'c\' for the computer to play the hand')
            if sub_decision == 'u':
                score += play_hand(hand, word_list)
            elif sub_decision == 'c':
                score += comp_play_hand(hand, word_list)
        decision = 'start'
        sub_decision = ''


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
