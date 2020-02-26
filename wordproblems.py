from random import choice, sample
from bisect import bisect_left, bisect_right

# Compute a histogram of individual characters in words.

def histogram(words):
    result = {}
    for word in words:
        for c in word:
            result[c] = result.get(c, 0) + 1
    return result

# Find all words that are palindromes.

def palindromes(words):
    return [x for x in words if x == x[::-1]]

# Find all words that are a different word when read backwards. 

def semordnilap(words):
    wset = set(words)
    return [x for x in words if x != x[::-1] and x[::-1] in wset]

# Find all the rotodromes, words that become other words when rotated.

def rotodromes(words):
    def _is_rotodrome(word, wset):
        for i in range(1, len(word)):
            w2 = word[i:] + word[:i]
            if w2 != word and w2 in wset:
                return True
        return False
    wset = set(words)
    return [x for x in words if _is_rotodrome(x, wset)]

# Find the "almost palindromes", words that become palindromes when
# one letter is tactically removed.

def almost_palindromes(words):    
    def almost(word):
        for i in range(len(word) - 1):
            w2 = word[:i] + word[i+1:]
            if w2 == w2[::-1]:
                return True
        return False
    return [x for x in words if len(x) > 2 and almost(x)]

# Rotate the consonants of the text cyclically, keeping the rest of
# the characters as they are, and maintaining the capitalization of
# the individual characters. For example, "Ilkka" becomes "Iklka".

__cons = "bcdfghjklmnpqrstvwxyz"
__cons += __cons.upper()

def rotate_consonants(text, off = 1):
    # Find the positions of all consonants in text.
    cons_pos = [i for (i, c) in enumerate(text) if c in __cons]
    # Process the text one character at the time.
    result, pos = '', 0    
    for (i, c) in enumerate(text):
        if c in __cons:
            # Location of the next consonant in the consonant list.
            succ = (pos + off) % len(cons_pos)
            # Maintain the capitalization.
            if c.isupper():
                result += text[cons_pos[succ]].upper()
            else:
                result += text[cons_pos[succ]].lower()
            pos = (pos + 1) % len(cons_pos)
        else:
            # Take the character into result as is.
            result += c
    return result

# Stolen from "Think Python: How To Think Like a Computer Scientist"

# Regular expressions can come handy in all kinds of string problems.
import re

# Find the words that contain at least three duplicated letters.

def triple_duplicate(words):
    return [x for x in words if len(re.findall(r'(.)\1', x)) > 2]

# Find the words that contain three duplicated letters all together.

def consec_triple_duplicate(words):
    return [x for x in words if len(re.findall(r'(.)\1(.)\2(.)\3', x)) > 0]

# How many words can be spelled out using only given characters?

def limited_alphabet(words, chars):
    # A regular expression used many times is good to precompile
    # into the matching machine for speed and efficiency.
    pat = re.compile('^[' + chars + ']+$')
    return [word for word in words if pat.match(word)]    

# Stolen from Programming Praxis. Given text string and integer 
# k, find and return the longest substring that contains at most
# k different characters inside it.

def longest_substring_with_k_chars(text, k = 2):
    # The k most recently seen characters mapped to the last
    # position index of where they occurred.
    last_seen = {}
    len_, max_, maxpos = 0, 0, 0
    for (i, c) in enumerate(text):        
        # If no conflict, update the last_seen dictionary.
        if len(last_seen) < k or c in last_seen:
            last_seen[c] = i
            len_ += 1
            if len_ > max_:
                max_ = len_
                maxpos = i - max_ + 1
        else:
            # Find the least recently seen character.
            min_, minc = len(text), '$'
            for cc in last_seen:
                if last_seen[cc] < min_:
                    min_ = last_seen[cc]
                    minc = cc
            # Remove it from dictionary...
            last_seen.pop(minc)
            # ... and bring the current character to its place.
            last_seen[c] = i
            len_ = i - min_
    # Extract the longest found substring as the answer.
    return text[maxpos:maxpos + max_]

# Given a sorted list of words and the first word, construct a
# word chain in which each word starts with the suffix of the
# previous word with the first k characters removed, for example
# ['grama', 'ramal', 'amala', 'malar', 'alarm'] for k = 1.

# Since words are sorted, we can use binary search algorithm to
# quickly find the sublist whose words start with the given prefix. 

def word_chain(words, first, k = 1, len_ = 3):
    # Recursive algorithm to complete the given wordlist.
    def backtrack(chain):
        # If the wordlist is long enough, return it.
        if len(chain) == len_:
            return chain
        # Extract the suffix of the last word of the wordlist.
        suffix = chain[-1][k:]
        # Extract the words that start with that suffix.
        start = bisect_left(words, suffix)
        end = bisect_right(words, suffix + k * 'z')
        # Try out those words one at the time.
        for idx in range(start, end):
            word = words[idx]
            if len(word) > len(chain[-1]) - k and word not in chain:
                # Extend the wordlist with this word.
                chain.append(word)
                if backtrack(chain): # Solution found
                    return chain
                # Remove that word and try the next one.
                chain.pop()
            
        return None    
    return backtrack(first)    


# What words remain words by removing one character? Create and return
# a list whose i:th element is a dictionary of all such words of length
# i, mapped to the list of words of length i-1 that they can be turned
# into by removing one letter.

def remain_words(words):
    result = [ [], [x for x in words if len(x) == 1] ]
    wl = 2
    while True:
        nextlevel, hasWords = { }, False        
        for w in (x for x in words if len(x) == wl):
            shorter = []
            for i in range(0, wl - 1):
                ww = w[:i] + w[i+1:] # word w with i:th letter removed
                if ww in result[wl - 1]:
                    shorter.append(ww)
            if len(shorter) > 0:
                nextlevel[w] = shorter
                hasWords = True
        if hasWords:
            result.append(nextlevel)
            wl += 1
        else:
            return result

# Generate a table of all anagrams from the given words.
def all_anagrams(words):
    godel = {}
    # The first 26 prime numbers, one for each letter from a to z.
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    for word in words:
        m = 1
        for c in word:
            # ord(c) gives the Unicode integer codepoint of c.
            m *= primes[ord(c) - ord('a')]
        # All anagrams have the same godel number, due to commutativity
        # of integer multiplication and the Fundamental Theorem of
        # Arithmetic that says every integer has one prime factorization.
        godel[m] = godel.get(m, []) + [word]
    return godel


if __name__ == "__main__":
    with open('words_alpha.txt', encoding="utf-8") as f:
        words = [x.strip() for x in f]    
    print(f"Read in {len(words)} words.")
    
    # Binary search can quickly find all words with given prefix.
    for prefix in ["aor", "jim", "propo"]:
        result = []
        idx = bisect_left(words, prefix)
        while idx < len(words) and words[idx].startswith(prefix):
            result.append(words[idx])
            idx += 1
        result = ", ".join(result)
        print(f"\nWords that start with {prefix!r} are {result}.")
    
    # How about finding all words that end with given suffix?
    words_r = [word[::-1] for word in words]
    words_r.sort()
    for suffix in ["itus", "roo", "lua"]:
        suffix = suffix[::-1]
        result = []
        idx = bisect_left(words_r, suffix)
        while idx < len(words_r) and words_r[idx].startswith(suffix):
            result.append(words_r[idx][::-1])
            idx += 1
        result = ", ".join(result)
        print(f"\nWords that end with {suffix[::-1]!r} are {result}.")
    
    hist = histogram(words).items()
    hist = sorted(hist, key = (lambda x: x[1]), reverse = True)    
    print("\nHistogram of letters sorted by their frequencies:")
    print(hist)
    
    pals = palindromes(words)
    print(f"\nThere are {len(pals)} palindromes. ", end = "")
    print("Some of them are:")
    print(", ".join(sample(pals, 10)))
    
    sems = semordnilap(words)    
    print(f"\nThere are {len(sems)} semordnilaps. Some of them are:")
    print(", ".join(sample(sems, 10)))
    
    almost = almost_palindromes(words)
    print(f"\nThere are {len(almost)} almost palindromes. ", end = "")
    print("Some of them are:")
    print(", ".join(sample(almost, 10)))
    
    print("\nLet us next look for some rotodromes.")
    for i in range(2, 13):
        rotos = rotodromes([w for w in words if len(w) == i])
        print(f"There are {len(rotos)} rotodromes of length {i}. ", end = "")
        print(f"Some of them are:")
        print(f"{', '.join(sample(rotos, min(10, len(rotos))))}.")
    
    name = 'Donald Erwin Knuth'
    print(f"\nSome consonant rotations of {name!r}.")
    for off in range(-5, 6):
        print(f"{off:2}: {rotate_consonants(name, off)}")
    
    print("\nWords that contain triple duplicate character:")
    for word in triple_duplicate(words):
        print(word, end = ' ')
    
    print("\n\nWords that contain consecutive triple duplicate:")
    for word in consec_triple_duplicate(words):
        print(word, end = ' ')
    
    print("\n\nWords that contain only hexadecimal digits [a-f]:")
    for word in limited_alphabet(words, "abcdef"):
        print(word, end = ' ')
    
    print("\n\nWords that contain only vowels:")
    for word in limited_alphabet(words, "aeiouy"):
        print(word, end = ' ')
    
    print("\n\nWords spelled with upside down calculator:")
    for word in limited_alphabet(words, "oieslbg"):
        print(word.upper(), end = ' ')
    
    text = "ceterumautemcenseocarthaginemessedelendam"
    print(f"\n\nThe text is '{text}'.")
    print("Let's print out its longest substrings with k letters.")
    for k in range(1, 16):
        print(f"k = {k:2}: {longest_substring_with_k_chars(text, k)}")
    
    print(f"\nHow about the longest 10-char substring of War and Peace?")
    with open('warandpeace.txt', encoding="utf-8") as wap:
        text = " ".join(wap)
    text.replace("\n", " ")
    print(f"It is:{longest_substring_with_k_chars(text, 10)}")
    
    print("\nNext, some word chains of five-letter words.")
    words5 = [word for word in words if len(word) == 5]
    count, total = 0, 0
    while count < 10:
        total += 1
        first = choice(words5)
        best = [first]
        while len(best) < 5:
            better = word_chain(words5, [first], 1, len(best) + 1)
            if better:
                best = better
            else:
                break
        if len(best) > 3:
            print(f"{first}: {best}")
            count += 1
    print(f"Found {count} word chains after trying {total} firsts.")
    
    print("\nSome letter eliminations:")
    elim_dict_list = remain_words(words)
    startwords = list(elim_dict_list[8])
    for i in range(10):
        word = choice(startwords)
        while len(word) > 1:
            print(word, end = " -> ")
            word = choice(elim_dict_list[len(word)][word])
        print(word)
        
    print("\nLet us compute all anagrams for the six letter words.")
    words6 = [word for word in words if len(word) == 6]
    anagrams = all_anagrams(words6)
    print("The anagram groups with eight or more members are:")
    for li in (x for x in anagrams if len(anagrams[x]) >= 8):
        print(", ".join(anagrams[li]))