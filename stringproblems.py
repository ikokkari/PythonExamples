# The string module has handy data and methods for text processing.

from string import ascii_letters as letters
from string import ascii_uppercase as au
from string import ascii_lowercase as al
from random import Random


# Convert words in the text to title case. (Not same as uppercase.)

def title_words(text):
    prev, result = " ", ""
    for c in text:
        if prev.isspace() and not c.isspace():
            result += c.title()
        else:
            result += c
        prev = c
    return result


# Eliminate the consecutive duplicate characters from a string.

def eliminate_duplicates(text):
    prev, result = None, ""
    for c in text:
        if c != prev:
            result += c
            prev = c
    return result


# Given a text string, create and return another string that contains
# each character only once, in order that they occur in the text.

def unique_chars(text):
    result, seen = '', set()
    for c in text:
        if c not in seen:
            result += c
            seen.add(c)
    return result


# The classic way to test whether two strings are anagrams. They
# are if and only if sorting both gives the same end result.

def are_anagrams(word1, word2):
    # A quick screening test to avoid the more expensive sort operation.
    # If pass, perform the expensive operation to find out the truth.
    return len(word1) == len(word2) and sorted(word1) == sorted(word2)


# Obfuscate the given text using the ROT-13 encoding. Easy to do with
# building a conversion dictionary with dictionary comprehension.
# https://en.wikipedia.org/wiki/ROT13

def rot13(text):
    # Conversion dictionary for characters.
    rot = {a: b for (a, b) in zip(au + al, au[13:] + au[:13] + al[13:] + al[:13])}
    # Convert to ROT-13 by converting characters separately.
    return "".join([rot.get(c, c) for c in text])


# Translate the entire sentence given a function word_func that converts
# one word. Since whitespace and punctuation characters must be kept
# as they were in the original sentence, we can't just use "split" to
# separate the sentence into words, since this would lose the track
# of what the whitespace and punctuation were in the original text.
# Instead, we have to break the sentence into words the hard way.

def translate_words(sentence, word_func):
    result, word = '', ''
    for c in sentence:
        is_letter = c in letters
        if is_letter:  # add the letters into the current word
            word += c
        elif len(word) > 0 and not is_letter:  # non-letter ends word
            result += word_func(word) + c  # add the translated word
            word = ''  # and start the next word from empty
        else:
            result += c  # non-letters added to result as is
    if len(word) > 0:  # the possibly remaining word at end of sentence
        result += word_func(word)
    return result


# Convert the given sentence to pig latin. Note how the function to
# convert one word is defined inside this function, to be passed to
# the previous translate_words function as its second argument f.

def pig_latin(sentence):
    def trans(word):
        cap = word[0].isupper()
        pos = 0
        # Skip all the consonants at the start of the word.
        while pos < len(word) and word[pos] not in "aeiouAEIOUY":
            pos += 1
        if pos == 0:  # The word starts with vowel.
            return word + "way"
        else:
            head = word[pos].upper() + word[pos + 1:] if cap else word[pos:]
            return head + word[:pos].lower() + "ay"
    return translate_words(sentence, trans)


# Convert the given sentence to ubbi dubbi. Same logic as previous.

def ubbi_dubbi(sentence):
    def convert(c):
        if c in 'aeiouyAEIOUY':
            if c.isupper():
                return "Ub" + c.lower()
            else:
                return "ub" + c
        else:
            return c

    def trans(word):
        return "".join([convert(c) for c in word])

    return translate_words(sentence, trans)


# The trickiest conversion gives us a choice of how to convert each
# letter. Let us maintain a dictionary that maps each letter to the
# list of the possibilities.

def tutnese(sentence):
    reps = {"b": ["bub"],
            "c": ["cash", "coch"],
            "d": ["dud"],
            "f": ["fuf", "fud"],
            "g": ["gug"],
            "h": ["hash", "hutch"],
            "j": ["jay", "jug"],
            "k": ["kuck"],
            "l": ["lul"],
            "m": ["mum"],
            "n": ["nun"],
            "p": ["pup", "pub"],
            "q": ["quack", "queue"],
            "r": ["rug", "rur"],
            "s": ["sus"],
            "t": ["tut"],
            "v": ["vuv"],
            "w": ["wack", "wash"],
            "x": ["ex", "xux"],
            "y": ["yub", "yuck"],
            "z": ["zub", "zug"]}

    def trans(word, rng=None):
        if not rng:
            rng = Random(12345)
        result, skip = '', False
        for (pos, c) in enumerate(word):
            if skip:
                skip = False
                continue
            c = c.lower()
            if pos < len(word) - 1 and c == word[pos + 1].lower():
                if c in "aeiouy":
                    dup = "squat"
                else:
                    dup = "squa"
                if word[pos].isupper():
                    dup = dup[0].upper() + dup[1:]
                result += dup + c
                skip = True  # skip the duplicate after this one
            else:
                if c in reps:
                    rep = rng.choice(reps[c])
                    if word[pos].isupper():
                        rep = rep[0].upper() + rep[1:]
                    result += rep
                else:
                    result += word[pos]
        return result
    return translate_words(sentence, trans)


def __demo():
    text = "hello there, how are you doing?"
    print(f"Original string is: {text}")
    print(f"Unique chars of {text} are: {unique_chars(text)}.")
    print(f"Removing duplicates gives: {eliminate_duplicates(text)}")
    print(f"Converted to titlecase gives: {title_words(text)}\n")

    text = "Hello world! How are you?"
    print(f"Original string is : {text!r}")
    text = rot13(text)
    print(f"After ROT-13, it is: {text!r}")
    text = rot13(text)
    print(f"Another ROT-13, it is: {text!r}")
    print("\nNext, some conversions to secret languages.")
    sentences = [
        'What does this become? We are eager to see!',
        'Another one, just for fun.',
        'Do you know the famous Variety headline "Stix nix hix pix"?'
    ]
    for sentence in sentences:
        print(f"\nOriginal:   {sentence}")
        print(f"Pig latin:  {pig_latin(sentence)}")
        print(f"Ubbi dubbi: {ubbi_dubbi(sentence)}")
        print(f"Tutnese:    {tutnese(sentence)}")

    print("\nFinally, let's check out the anagram tester.")
    tater_rater = are_anagrams('tater', 'rater')
    print(f"Are 'tater' and 'rater' anagrams? {tater_rater}")
    search_chaser = are_anagrams('search', 'chaser')
    print(f"Are 'search' and 'chaser' anagrams? {search_chaser}")


if __name__ == "__main__":
    __demo()
