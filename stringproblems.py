# Convert the words in the text to title case. (Not same as uppercase.)

def title_words(text):
    prev, result = ' ', ''
    for c in text:
        if prev.isspace() and not c.isspace():
            result += c.title()
        else:
            result += c
        prev = c
    return result

# Eliminate the consecutive duplicate characters from a string.

def eliminate_duplicates(text):
    prev, result = None, ''    
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

# The classic way to test whether two strings are anagrams. They are
# if and only if sorting both gives the same end result.

def are_anagrams(word1, word2):
    # A quick rejection test to avoid the expensive operation.
    if len(word1) != len(word2):
        return False
    # Perform the expensive operation to find out the truth.
    return sorted(word1) == sorted(word2)

# The string module has handy data and methods for text processing.

from string import ascii_letters as letters
from string import ascii_uppercase as au
from string import ascii_lowercase as al

au_c = au[13:] + au[:13]
al_c = al[13:] + al[:13]

# Obfuscate the given text using the ROT-13 encoding:
# https://en.wikipedia.org/wiki/ROT13

def rot13(text):
    result = ''
    for c in text:
        idx = au.find(c) # Is c an uppercase character?
        if idx > -1:
            result += au_c[idx]
        else:
            idx = al.find(c) # Is c a lowercase character?
            if idx > -1:
                result += al_c[idx]
            else:
                result += c # Other characters are taken as is.
    return result

from random import choice

# Given a sentence and a function wf that converts one word, translate
# the entire sentence. Since whitespace and punctuation must be kept
# as they were in the original sentence, we can't just use "split" to
# separate the sentence into words, since this would lose the track
# of what the whitespace and punctuation were in the original text.
# Instead, break the sentence into words the hard way.

def translate_words(sentence, wf):
    result, word = '', ''    
    for c in sentence:
        is_letter = c in letters
        if is_letter: # add the letters into the current word
            word += c
        elif len(word) > 0 and not is_letter: # non-letter ends the word
            result += wf(word) + c # add the translated word
            word = '' # and start the next word from empty
        else:
            result += c # non-letters added to result as is
    if len(word) > 0: # the possibly remaining word at end of sentence
        result += wf(word)
    return result

# Convert the given sentence to pig latin. Note how the function to
# convert one word is defined inside this function, to be passed to
# the previous translate_words function as its second argument f.

def pig_latin(sentence):
    def trans(word):
        cap = word[0].isupper()
        idx = 0
        while idx < len(word) and word[idx] not in "aeiouAEIOUY":
            idx += 1
        if idx == 0: # the word starts with vowel
            return word + "way"
        else:
            if cap:
                head = word[idx].upper() + word[idx + 1:]
            else:
                head = word[idx:]
            return head + word[:idx].lower() + "ay"
    return translate_words(sentence, trans)

# Convert the given sentence to ubbi dubbi. Same logic as previous.

def ubbi_dubbi(sentence):
    def convert(c):
        if c in 'aeiouyAEIOUY':
            if c.isupper(): return "Ub" + c.lower()
            else: return "ub" + c
        else: return c
    def trans(word):
        return "".join([convert(c) for c in word])
    return translate_words(sentence, trans)

# The trickiest conversion gives us a choice of how to convert each
# letter. Let us maintain a dictionary that maps each letter to the
# list of the possibilities.

def tutnese(sentence):
    reps =   {  "b": ["bub"],
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
                "z": ["zub", "zug"] }
    def trans(word):
        result, skip = '', False        
        for (idx, c) in enumerate(word):
            if skip:
                skip = False
                continue
            c = c.lower()
            if idx < len(word) - 1 and c == word[idx + 1].lower():
                if c in "aeiouy":
                    dup = "squat"
                else:
                    dup = "squa"
                if word[idx].isupper():
                    dup = dup[0].upper() + dup[1:]
                result += dup + c
                skip = True # skip the duplicated letter after this one
            else:
                if c in reps:
                    rep = choice(reps[c])
                    if word[idx].isupper():
                        rep = rep[0].upper() + rep[1:]
                    result += rep
                else:
                    result += word[idx]
        return result
    return translate_words(sentence, trans)    

# Convert an integer into its English language name.

# http://lcn2.github.io/mersenne-english-name/tenpower/tenpower.html
__pows = (("thousand", 3), ("million", 6), ("billion", 9),
          ("trillion", 12), ("quadrillion", 15), ("quintillion", 18),
          ("sextillion", 21), ("septillion", 24), ("octillion", 27),
          ("nonillion", 30), ("decillion", 33), ("undecillion", 36),
          ("duodecillion", 39), ("tredecillion", 42),
          ("quattuordecillion", 45), ("quindecillion", 48),
          ("sexdecillion", 51), ("eptendecillion", 54),
          ("octadecillion", 57), ("novemdecillion", 60),
          ("vigintillion", 63), ("unvigintillion", 66),
          ("duovigintillion", 69), ("trevigintillion", 72),
          ("quattuorvigintillion", 75), ("quinvigintillion", 78),
          ("sexvigintillion", 81), ("septenvigintillion", 84),
          ("octavigintillion", 87), ("novemvigintillion", 90),
          ("trigintillion", 93), ("untrigintillion", 96),
          ("duotrigintillion", 99)
          )

# Dictionary comprehension, analogous to list comprehension.
__pows = { p:n for (n, p) in __pows }

# Return the English name of a three-digit integer.
def __int_to_eng(n):
    if n < 20: # Numbers 0 to 19 with a simple lookup table.
        return ["ERROR", "one", "two", "three", "four", "five",
                "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen"][n]
    elif n < 100: # Numbers 20 to 99, tens again with a lookup table.
        tens = ["", "", "twenty", "thirty", "forty", "fifty", 
                "sixty", "seventy", "eighty", "ninety"][n // 10]
        if n % 10 != 0:
            return f"{tens}-{__int_to_eng(n % 10)}"            
        else:
            return tens
    else: # Numbers 100 to 999
        if n % 100 == 0:
            return f"{__int_to_eng(n // 100)} hundred"            
        else:
            return f"{__int_to_eng(n // 100)} hundred and {__int_to_eng(n % 100)}"            
               
__googol = 10 ** 100

# Construct the English name of any integer.
def int_to_english(n):
    if n < 0: # Negative numbers
        return "minus " + int_to_english(-n)
    if n == 0: # Zero as a special case
        return "zero"
    if n >= __googol: # huge numbers
        first = int_to_english(n // __googol)
        rest = int_to_english(n % __googol)
        if rest == "zero":
            return f"{first} googol"
        else:
            return f"{first} googol and {rest}"
    result, p = [], 0
    while n > 0:
        trip = n % 1000
        n = n // 1000
        if trip > 0:
            if p == 0:
                result.append(__int_to_eng(trip))
            else:
                result.append(__int_to_eng(trip) + " " + __pows[p])
        p += 3
    return " ".join(reversed(result))

                    
if __name__ == "__main__":
    text = "Ilkka Kokkarinen"
    print(f"Unique chars of {text} are {unique_chars(text)}.")
    for x in [42, 3**7, 6**20, -(2**100), 9**200, 10**500]:
        print(f"{x} written in English is {int_to_english(x)}.")
    print("Here are integers 0-100 sorted in alphabetical order:")
    print(sorted(range(0, 101), key = int_to_english))
    print("Here are integers 0-100 sorted in order of name lengths:")
    print(sorted(range(0, 101), key = lambda x: (len(int_to_english(x)), x)))
    print("The numbers that do not contain the letter 'o':")
    print([x for x in range(1000) if 'o' not in int_to_english(x)])
    s = "Hello world! How are you?"
    print(f"Original string is : {s!r}")
    s = rot13(s)
    print(f"After ROT-13, it is: {s!r}")
    s = rot13(s)
    print(f"Another ROT-13, it is: {s!r}")
    print("\nNext, some conversions to secret languages.")
    sentences = [
        'What does this become? We are eager to see!',
        'Another one, just for fun.',
        'Do you know the famous Variety headline "Stix nix hix pix"?'   
    ]
    for sentence in sentences:
        print(f"Original:   {sentence}")
        print(f"Pig latin:  {pig_latin(sentence)}")
        print(f"Ubbi dubbi: {ubbi_dubbi(sentence)}")
        print(f"Tutnese:    {tutnese(sentence)}")

    print("\nFinally, let's check out the anagram tester.")
    print(f"Are 'tater' and 'rater' anagrams? {are_anagrams('tater', 'rater')}")
    print(f"Are 'search' and 'chaser' anagrams? {are_anagrams('search', 'chaser')}")