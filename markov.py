"""Generate Markov text from text files."""

import sys
from random import choice

N = 5


def open_and_read_file():
    """Take file path as string; return text as string.
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    # create file object
    file = open(sys.argv[1])
    # read file
    text = file.read()
    # close file - you only have a certain number of active file discriptors
    file.close()

    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.
    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    For example:
        >>> chains = make_chains('hi there mary hi there juanita')
    Each bigram (except the last) will be a key in chains:
        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]
    Each item in chains is a list of all possible following words:
        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    # take text string and split on spaces
    words = text_string.split()
    # loop through words using enumerate so we can reference the next word
    for i, word in enumerate(words):
        # try this block for error
        try:
            key_list = []
            # loop through n which is three in this case
            for j in range(N):
                try:
                    # create key lists by adding j(0, 1 or 2) to i
                    # so we get three strings in our tuple in this case
                    key_list.append(words[i + j])
                # throw index error and stop bc we are at the end
                except IndexError:
                    break
            # only add tuples that are the length of N
            if len(key_list) == N:
                keys = tuple(key_list)
            else:
                # break to avoid duplicating the last tuple N times
                break

            # if the tuple of the word and the next word is already a key
            if keys in chains.keys():
                # add the value to the list of words
                chains[keys].append(words[i + N])
            else:
                # set value to the next word in text
                chains[keys] = [words[i + N]]
        # except if there is index error
        except IndexError:
            break
    return chains


def make_text(chains):
    """Return text from chains."""
    words = []

    working_key = choice(list(chains.keys()))
    # if the first letter is lowercase keep generating more options
    while working_key[0].islower():
        # create  var that chooses random key
        working_key = choice(list(chains.keys()))

    # looping through indexs of N
    for i in range(N):
        # adding each index of our tuple in range N to words list
        # aka add all of our tuple to words list
        words.append(working_key[i])
    # start while true loop because we dont many working keys there will be
    while True:
        try:
            # next var picks a word from value list
            next = choice(chains[working_key])
            # add word to words list
            words.append(next)
            working_list = []
            # start at 1 bc we want all of the words in working key except the first one
            for index in range(1, N):
                # add each str in the working key except for the first string
                # we want new working key to stay the length of N
                working_list.append(working_key[index])
            # adds our new random word from working key at the end
            working_list.append(next)
            # change to tuple
            working_key = tuple(working_list)
        # stop loop when there is a key error because we have reached the end of our text
        except KeyError:
            break

    # return words with spaces in between each
    return " ".join(words)


# if we are running directly and not being imported
# if we wrote another py file and imported parkov.py
# we dont want to run the tests below because we already have run these tests
# and it could output things dont want to output in our new file
if __name__ == "__main__":
    input_path = "green-eggs.txt"

    # Open the file and turn it into one long string
    input_text = open_and_read_file()

    # Get a Markov chain
    chains = make_chains(input_text)

    # Produce random text
    random_text = make_text(chains)

    print(random_text)
