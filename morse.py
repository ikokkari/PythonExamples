from random import Random
from bisect import bisect_left

# https://en.wikipedia.org/wiki/Morse_code

# Morse code is not what is called 'prefix code' so that
# no encoding of some character could be a prefix of the
# encoding of some other character. Decoding sequences of
# dots and dashes is therefore ambiguous (for example, "..."
# could be either "s" or "eee") unless the operator inserts
# a short pause as an artificial separator between letters.

# Dictionary of Morse codes and their corresponding letters.

codes = {
    '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
    '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
    '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
    '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
    '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
    '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
    '-.--': 'y', '--..': 'z'
    }

# Construct a reverse dictionary from an existing dictionary
# with this handy dictionary comprehension. If multiple keys
# of the original map to the same value, only the last pair
# of value and key is stored in the reverse dictionary. Here
# this doesn't matter, since no two keys in codes map to the
# same value.

codes_r = {codes[k]: k for k in codes}


# Given a string of characters, encode it in Morse code
# placing the given separator between the encodings of the
# individual letters. Unknown characters are simply skipped
# in this encoding.

def encode_morse(text, sep=''):
    return sep.join(codes_r.get(c, '') for c in text.lower())


# To filter out decoded words that are actual words, two utility
# functions using the bisection method from the standard library.

def is_legal_word_prefix(prefix, words):
    # Find the first word in wordlist that is lexicographically
    # at least as large as the given prefix.
    idx = bisect_left(words, prefix)
    # Check that that word starts with the given prefix.
    return idx < len(words) and words[idx].startswith(prefix)


def is_legal_word(word, words):
    idx = bisect_left(words, word)
    return idx < len(words) and words[idx] == word


# A recursive generator that yields all possible ways to
# decode the given Morse code message back to letters so that
# only actual words are generated.

def decode_morse(message, words, word_so_far=""):
    if message == "":
        if is_legal_word(word_so_far, words):
            yield word_so_far
    else:
        # Complete the current word from the remaining message.
        for prefix in codes:
            if message.startswith(prefix):
                new_word = word_so_far + codes[prefix]
                if is_legal_word_prefix(new_word, words):
                    yield from decode_morse(message[len(prefix):], words, new_word)


# To paraphrase that Heath Ledger Joker meme, nobody has a
# problem when a generator uses some other lazy sequence
# such as range as part of its computation, but make your
# generator recursively use another instance of that same
# type of generator, and everyone loses their minds...

# Since in general there can be an exponential number of ways
# to decode Morse code back to characters, it is essential
# for decode_morse to be lazy so that it decodes these
# messages one at the time, instead of potentially filling
# up the entire process memory. For example, just consider
# the number of different ways to decode a sequence of n
# consecutive dots back to characters:

def __demo():
    with open('words_sorted.txt', encoding='utf-8') as f:
        words = [word.strip() for word in f if len(word) < 12]
    print(f'Read a list of {len(words)} words.')

    rng = Random(424242)

    for text in rng.sample(words, 20):
        message = encode_morse(text)
        print(f'The word {text!r} encodes in Morse to {message!r}')
        print(f'The Morse code message {message!r} decodes to words:')
        for word in decode_morse(message, words, ""):
            print(f"{word!r} split as {encode_morse(word, ' ')}")
        print('')


if __name__ == '__main__':
    __demo()

# Motivated readers could find the largest group of words that
# all encode to the same series of Morse dots and dashes.

# Were Morse code designed today, it would surely be constructed
# as a "Huffman code" to produce the optimal prefix code for the
# individual character frequencies of English. This guarantees
# unique decodability of each sequence of dots and dashes back to
# the original English text. Alas, we cannot fault Samuel Morse
# (1791-1872) for not being aware of all the nifty advances of
# combinatorial algorithms made during the twentieth century...

# https://en.wikipedia.org/wiki/Huffman_coding

# Note that Huffman code is optimal only if every character must
# be encoded separately. More advanced compression methods can and
# will automatically exploit the conditional probabilities between
# consecutive letters. For example, after seeing "qui", letters p,
# t and z suddenly become more likely compared to their baseline
# probabilities in English when every letter must be encoded on its
# own, separated from its surrounding context...
