# The dictionary of Morse codes and the corresponding letters.

codes = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z"
    }

# Morse code is not what is known as "prefix code" so that
# no encoding of some character would be a prefix of the
# encoding of some other character. This makes the decoding
# ambiguous unless the Morse operator takes a noticeable
# short pause between the individual letters.

# Construct a reverse dictionary from an existing dictionary 
# with this handy dictionary comprehension.

codes_r = { codes[v]: v for v in codes }

# Given a string of characters, encode it in Morse code
# placing the given separator between the encodings of the
# individual letters. Unknown characters are simply skipped
# in this encoding.
def encode_morse(text, sep=""):
    return sep.join((codes_r.get(c, "") for c in text.lower()))

# A generator function that yields all possible ways to
# decode the given Morse code message into a string. This
# generator is written recursively to find all the possible
# first characters, followed by the recursive decodings of
# the rest of the message.
def decode_morse(message):
    if message == "":
        yield ""
    else:        
        for i in range(1, min(len(message) + 1, 5)):
            prefix = message[:i]
            if prefix in codes:
                head = codes[prefix]
                for follow in decode_morse(message[i:]):
                    yield head + follow

if __name__ == "__main__":
    from random import sample
    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [word.strip() for word in f if len(word) < 8]
    print(f"Read a list of {len(wordlist)} words.")

    # Convert to set for a quick lookup of individual words.
    words = set(wordlist)

    for text in sample(wordlist, 20):
        enc = encode_morse(text)
        print(f"The word {text!r} encodes in Morse to {enc!r}.")
        print(f"The Morse code message {enc!r} decodes to words:")
        dec = [word for word in decode_morse(enc) if word in words]
        for word in dec:
            print(f"{word!r} split as {encode_morse(word, ' ')}")
        print("")
        
# Exercise for the reader: find the word whose encoding in Morse
# can be decoded to largest possible number of different words.