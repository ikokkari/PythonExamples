from random import Random
from bisect import bisect_left, bisect_right


# Use binary search to determine if the given word is in the sorted wordlist.

def is_legal_word(word, words):
    idx = bisect_left(words, word)
    return idx < len(words) and words[idx] == word


# Compute a histogram of individual characters in words.

def histogram(words):
    result = {}
    for word in words:
        for c in word:
            result[c] = result.get(c, 0) + 1
    return result


# Find all words that are find_palindromes.

def find_palindromes(words):
    return [word for word in words if word == word[::-1]]


# Find all words that are a different word when read backwards.

def find_semordnilaps(words):
    return [word for word in words if word != word[::-1] and is_legal_word(word[::-1], words)]


# Find all rotodromes, words that become other words when rotated.

def find_rotodromes(words):

    # Define a nested helped function to perform the filtering.
    def is_rotodrome(word):
        for i in range(1, len(word)):
            rotated_word = word[i:] + word[:i]
            if word != rotated_word and is_legal_word(rotated_word, words):
                return True
        return False

    return [word for word in words if is_rotodrome(word)]


# Find the "almost palindromes", words that become palindromes when
# one letter is tactically removed.

def find_almost_palindromes(words):
    def is_almost_palindrome(word):
        # Words that are already palindromes don't count.
        if word != word[::-1]:
            # Loop through the positions to remove a character.
            for i in range(len(word)):
                removed_word = word[:i] + word[i + 1:]
                if removed_word == removed_word[::-1]:
                    return True
        return False

    return [word for word in words if len(word) > 2 and is_almost_palindrome(word)]


# Rotate the consonants of the text cyclically, keeping the rest of
# the characters as they are, and maintaining the capitalization of
# the individual characters. For example, "Ilkka" becomes "Iklka".

__cons = "bcdfghjklmnpqrstvwxyz"
__cons += __cons.upper()


def rotate_consonants(text, off=1):
    # Find the positions of all consonants in text.
    cons_pos = [i for (i, c) in enumerate(text) if c in __cons]
    # Process the text one character at the time.
    result, pos = '', 0
    for (i, c) in enumerate(text):
        if c in __cons:
            # Location of the next consonant in the consonant list.
            succ = (pos + off) % len(cons_pos)
            # The consonant that comes into the current position i.
            sc = text[cons_pos[succ]]
            # Maintain the capitalization.
            result += sc.upper() if c.isupper() else sc.lower()
            # Next consonant and incoming consonant advance in lockstep.
            # pos = (pos + 1) % len(cons_pos)
            pos += 1
        else:
            # Take the character into result as is.
            result += c
    return result


# Find the words that contain at least three duplicated letters.

def triple_duplicates(words):
    result = []
    for word in words:
        count = 0
        prev = '$'
        for c in word:
            if c == prev:
                count += 1
                prev = '$'
            else:
                prev = c
        if count > 2:
            result.append(word)
    return result


# How many words can be spelled out using only given characters?

def limited_alphabet(words, chars):
    return [word for word in words if all(c in chars for c in word)]


# From Programming Praxis. Given text string and integer k,
# find and return the longest substring that contains at most
# k different characters inside it.

def longest_substring_with_k_chars(text, k=2):
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

def word_chain(words, first, k=1, len_=3):
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
                if backtrack(chain):  # Solution found
                    return chain
                # Remove that word and try the next one.
                chain.pop()

        return None

    return backtrack(first)


# What words remain words after removing one character? Create and return
# a list whose i:th element is a dictionary of all such words of length
# i, mapped to the list of words of length i-1 that they can be turned
# into by removing one letter.

def remain_words(words):
    result = [[], [x for x in words if len(x) == 1]]
    word_length = 2
    while True:
        next_level, has_words = {}, False
        for w in (x for x in words if len(x) == word_length):
            shorter = []
            for i in range(0, word_length - 1):
                ww = w[:i] + w[i + 1:]  # word with i:th letter removed
                if ww in result[word_length - 1]:
                    shorter.append(ww)
            if len(shorter) > 0:
                next_level[w] = shorter
                has_words = True
        if has_words:
            result.append(next_level)
            word_length += 1
        else:
            return result


# Generate a table of all anagrams from the given word list.

# The first 26 prime numbers, one for each letter from a to z.

__primes = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17,
            'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
            'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73,
            'v': 79, 'w': 83, 'x': 89, 'y': 97, 'z': 101}


def prime_code(word):
    code = 1
    for c in word:
        code *= __primes.get(c, 1)
    return code


def all_anagrams(words):
    codes = {}
    for word in words:
        code = prime_code(word)
        # All anagrams have the same prime code, thanks to the
        # commutativity of integer multiplication combined with
        # the Fundamental Theorem of Arithmetic that says every
        # integer has exactly one prime possible factorization.
        codes[code] = codes.get(code, []) + [word]
    return codes


def __demo():

    rng = Random(12345)

    with open('words_sorted.txt', encoding="utf-8") as f:
        words = [x.strip() for x in f]
    print(f"Read in {len(words)} words.")

    # Binary search can quickly find all words with given prefix.
    for prefix in ['aor', 'jims', 'propo']:
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
        result.sort()
        result = ", ".join(result)
        print(f"\nWords that end with {suffix[::-1]!r} are {result}.")

    hist = histogram(words).items()
    hist = sorted(hist, key=lambda x: x[1], reverse=True)
    print("\nHistogram of letters sorted by their frequencies:")
    print(hist)

    pals = find_palindromes(words)
    print(f"\nThere are {len(pals)} palindromes. ", end="")
    print("Some of them aresa.:")
    print(", ".join(rng.sample(pals, 10)))

    sems = find_semordnilaps(words)
    print(f"\nThere are {len(sems)} semordnilaps. Some of them are:")
    print(", ".join(rng.sample(sems, 10)))

    almost = find_almost_palindromes(words)
    print(f"\nThere are {len(almost)} almost palindromes. ", end="")
    print("Some of them are:")
    print(", ".join(rng.sample(almost, 10)))

    print("\nLet us next look for some rotodromes.")
    for n in range(2, 13):
        rotos = find_rotodromes([word for word in words if len(word) == n])
        print(f"There are {len(rotos)} rotodromes of length {n}.")
        print(f"Some of these rotodromes are:")
        print(f"{', '.join(rng.sample(rotos, min(10, len(rotos))))}.")

    name = 'Donald Erwin Knuth'
    print(f"\nSome consonant rotations of {name!r}.")
    for off in range(-5, 6):
        print(f"{off:2}: {rotate_consonants(name, off)}")

    print("\n\nWords that contain only hexadecimal digits [a-f]:")
    for word in limited_alphabet(words, "abcdef"):
        print(word, end=' ')

    print("\n\nWords that contain only vowels:")
    for word in limited_alphabet(words, "aeiouy"):
        print(word, end=' ')

    print("\n\nWords spelled with upside down calculator:")
    for word in limited_alphabet(words, "oieslbg"):
        print(word.upper(), end=' ')

    text = "ceterumautemcenseocarthaginemessedelendam"
    print(f"\n\nThe text is '{text}'.")
    print("Let's print out its longest substrings with k letters.")
    for k in range(1, 16):
        print(f"k = {k:2}: {longest_substring_with_k_chars(text, k)}")

    print(f"\nHow about the longest 10-char substring of War and Peace? It is:")
    with open('warandpeace.txt', encoding="utf-8") as wap:
        text = " ".join(wap)
    text.replace("\n", " ")
    print(f"{longest_substring_with_k_chars(text, 10)}")

    print("\nNext, some word chains of five-letter words.")
    words5 = [word for word in words if len(word) == 5]
    count, total = 0, 0
    while count < 10:
        total += 1
        first = rng.choice(words5)
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
    start_words = list(elim_dict_list[8])
    for n in range(10):
        word = rng.choice(start_words)
        while len(word) > 1:
            print(word, end=" -> ")
            word = rng.choice(elim_dict_list[len(word)][word])
        print(word)

    N, M = 7, 8
    print(f"\nLet us compute all anagrams for the {N}-letter words.")
    anagrams = all_anagrams(word for word in words if len(word) == N)
    print(f"The anagram groups with {M} or more members are:\n")

    # Note that anagrams is a dictionary that maps each prime codes
    # to lists of words that all share that same prime code.
    for code in (c for c in anagrams if len(anagrams[c]) >= M):
        print(", ".join(anagrams[code]))


if __name__ == "__main__":
    __demo()
