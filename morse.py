from random import sample

# https://en.wikipedia.org/wiki/Morse_code

# Morse code is not what is called 'prefix code' so that
# no encoding of some character could be a prefix of the
# encoding of some other character. Decoding sequences of
# dots and dashes is therefore ambiguous (for example, "..."
# could be either "s" or "eee") unless the operator inserts
# a short pause as an artificial separator between letters.

# The dictionary of Morse codes and the corresponding letters.

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
# of value: key is stored in the reverse dictionary.

codes_r = {codes[k]: k for k in codes}


# Given a string of characters, encode it in Morse code
# placing the given separator between the encodings of the
# individual letters. Unknown characters are simply skipped
# in this encoding.

def encode_morse(text, sep=''):
    return sep.join((codes_r.get(c, '') for c in text.lower()))


# A recursive generator that yields all possible ways to
# decode the given Morse code message back to letters. This
# generator is written recursively to find all the possible
# first characters, followed by the recursive decodings of
# the rest of the message.

def decode_morse(message):
    if message == '':
        yield ''
    else:
        for prefix in codes:
            if message.startswith(prefix):
                head = codes[prefix]
                for tail in decode_morse(message[len(prefix):]):
                    yield head + tail


# To paraphrase that Heath Ledger Joker meme, nobody has a
# problem when a generator uses some other lazy sequence
# such as range as part of its computation, but make your
# generator recursively use another instance of that same
# generator, and everyone loses their minds...

# Since in general there can be an exponential number of
# possible decodings back to characters, it is essential
# for decode_morse to be lazy so that it produces these
# decodings one at the time instead of potentially filling
# up the entire process memory. For example, just consider
# the number of different ways to decode a sequence of n
# consecutive dots back to letter sequences:

# In [0]: [len(list(decode_morse('.'*n))) for n in range(1, 13)]
# Out[0]: [1, 2, 4, 8, 15, 29, 56, 108, 208, 401, 773, 1490]


if __name__ == '__main__':
    with open('words_sorted.txt', encoding='utf-8') as f:
        wordlist = [word.strip() for word in f if len(word) < 8]
    print(f'Read a list of {len(wordlist)} words.')

    # Convert to set for a quick lookup of individual words.
    words = set(wordlist)

    for text in sample(wordlist, 20):
        enc = encode_morse(text)
        print(f'The word {text!r} encodes in Morse to {enc!r}.')
        print(f'The Morse code message {enc!r} decodes to words:')
        # We are interested only in decodings that are actual words.
        dec = [word for word in decode_morse(enc) if word in words]
        for word in dec:
            print(f"{word!r} split as {encode_morse(word, ' ')}")
        print('')

# Motivated readers could find the largest group of words that
# all encode to the same series of Morse dots and dashes.

# Were Morse code designed today, it would surely be constructed
# as a "Huffman code" to produce an optimal prefix code for the
# character frequencies of English. This guarantees the unique
# decodability of each sequence of dots and dashes back to the
# original English text. Alas, we cannot really fault Samuel Morse
# (1791-1872) for not being aware of all the nifty advances of
# combinatorial algorithms during the twentieth century...

# https://en.wikipedia.org/wiki/Huffman_coding
