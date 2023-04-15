from bisect import bisect_left, bisect_right
from itertools import islice
from random import Random


# Recursively fill an n-by-n box of letters so that every row and
# every column is a different n-letter word. This generator finds
# all possible ways to fill in the i:th horizontal word, given the
# previous i-1 horiz-ontal and vert-ical words. If babbage is set
# to True, the horizontal and vertical words are the same, for a
# much simpler version of this problem.

# For example, the incomplete square with two rows and columns
# filled in so far with the four words
#
# hello
# oasis
# tt
# ee
# ln
#
# would be represented by parameter values n = 5, i = 2, vv = 0,
# horiz = ['hello', 'oasis'] and vert = ['hotel', 'eaten']. The
# parameter vv flips between 0 and 1 to indicate whether the
# level parameter i should be incremented in the next call.


def wordfill(n, i, horiz, vert, wordlist, vv, babbage=False):
    # Entire square is complete when rows 0, ..., n-1 are filled.
    if i == n:
        yield horiz  # Success!
    else:
        # Vertical words constrain the next horizontal word.
        prefix = "".join([w[i] for w in vert])
        # Find the first word that starts with that prefix.
        idx = bisect_left(wordlist, prefix)
        # Iterate over words that start with that prefix.
        while idx < len(wordlist) and wordlist[idx].startswith(prefix):
            word = wordlist[idx]
            # Try using that word as the horizontal word.
            if not (word in horiz or word in vert):
                horiz.append(word)
                if babbage:  # Horizontal and vertical words equal
                    w = wordfill(n, i+1, horiz, horiz, wordlist, 0, True)
                else:  # Mirror the square around diagonal for the call
                    w = wordfill(n, i+vv, vert, horiz, wordlist, 1-vv)
                yield from w
                horiz.pop()
            idx += 1


def __demo():
    n = 6  # Size of each individual word square.
    rows, cols = 1, 1   # How big a grid of squares we want.

    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [x.strip() for x in f]
    print(f"Read in a word list of {len(wordlist)} words.")
    wordlist = [x for x in wordlist if len(x) == n]
    print(f"There remain {len(wordlist)} words of length {n}.")

    result = []
    rng = Random(12345)
    while len(result) < rows * cols:
        # The first word on the first row.
        w1 = rng.choice(wordlist)
        # Find the section of words that start with same letter.
        i1 = bisect_left(wordlist, w1[0])
        # Words starting with 'a' end at words starting with 'b'...
        i2 = bisect_right(wordlist, chr(ord(w1[0]) + 1))
        # Choose one of those words as the first vertical word.
        w2 = w1
        while w1 == w2:
            w2 = wordlist[rng.randint(i1, i2-1)]
        print(f"Trying out starting words {w1}, {w2}...", end=" ")
        found = False
        # Even if a generator can produce many solutions, we can still
        # be content with just one solution this time. One is an integer
        # same as any other integer, as far as islice is concerned.
        for sol in islice(wordfill(n, 1, [w1], [w2], wordlist, 0), 1):
            result.append(sol)
            found = True
        print("Those worked!" if found else "Nope!")

    print(f"Printing out {rows * cols} found word squares.\n")
    print("-" * ((n+3) * cols + 1))
    for row in range(rows):
        idx = row * cols
        for j in range(n):
            print("| ", end="")
            for i in range(idx, idx + cols):
                print(result[i][j], end=" | ")
            print("")
        print("-" * ((n + 3) * cols + 1))


if __name__ == "__main__":
    __demo()
