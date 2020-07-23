import bisect
import random


# Recursively fill an n-by-n box of letters so that every row and
# every column is some n-letter word. The call finds all the
# possible ways to fill in the i:th horizontal word, given the
# previous i - 1 horizontal and vertical words. If babbage is
# set to True, the word square must have same rows and columns.

# For example, the incomplete square
#
# hello
# oasis
# tt
# ee
# ln
#
# would be represented by parameter values n = 5, i = 2, vv = 0,
# horiz = ['hello', 'oasis'] and vert = ['hotel', 'eaten'].

def wordfill(n, i, horiz, vert, wordlist, vv, babbage=False):
    # Entire square is complete when rows 0, ..., n-1 are filled.
    if i == n:
        yield horiz
    else:
        # Vertical words constrain the next horizontal word.
        prefix = "".join([w[i] for w in vert])
        # Find the first word that starts with that prefix.
        idx = bisect.bisect_left(wordlist, prefix)
        # Iterate over words that start with that prefix.
        while idx < len(wordlist) and wordlist[idx].startswith(prefix):
            word = wordlist[idx]
            # Try using that word as the horizontal word.
            if not (word in horiz or word in vert):
                horiz.append(word)
                if babbage:  # Horizontal and vertical words equal
                    w = wordfill(n, i+1, horiz, horiz, wordlist, 0, True)
                else:
                    w = wordfill(n, i+vv, vert, horiz, wordlist, 1-vv)
                yield from w
                horiz.pop()
            idx += 1


if __name__ == "__main__":
    import itertools as it

    n = 5   # Size of each individual word square.

    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [x.strip() for x in f]
    print(f"Read in a word list of {len(wordlist)} words.")
    wordlist = sorted([x for x in wordlist if len(x) == n])
    print(f"There remain {len(wordlist)} words of length {n}.")

    wordset = set(wordlist)
    rows, cols = 2, 3
    result = []
    while len(result) < rows * cols:
        # The first word on the first row.
        w1 = random.choice(wordlist)
        # Find the section of words that start with same letter.
        i1 = bisect.bisect_left(wordlist, w1[0])
        i2 = bisect.bisect_right(wordlist, chr(ord(w1[0]) + 1))
        # Choose one of those words as the first vertical word.
        w2 = wordlist[random.randint(i1, i2 - 1)]
        print(f"Trying out starting words {w1}, {w2}...", end=" ")
        found = False
        for sol in it.islice(wordfill(n, 1, [w1], [w2], wordlist, 0), 1):
            result.append(sol)
            found = True
        print("Those worked!" if found else "Nope!")

    print(f"Printing out {rows*cols} found word squares.\n")
    print("-" * ((n+3)*cols + 1))
    for row in range(rows):
        idx = row * cols
        for j in range(n):
            print("| ", end="")
            for i in range(idx, idx + cols):
                print(result[i][j], end=" | ")
            print("")
        print("-" * ((n + 3) * cols + 1))
