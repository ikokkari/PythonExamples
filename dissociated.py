from random import Random
from itertools import islice


# Read through the text and build a dictionary that, for each found
# pattern up to length n, gives the string of letters that follow that
# pattern in the original text.

def build_table(text, patlen=3, max_len=100):
    result, window = {}, ""
    for c in text:
        window += c
        # Shorten the window if needed.
        if len(window) > patlen + 1:
            window = window[1:]
        for i in range(0, len(window)-1):
            block = window[i:-1]
            follow = result.get(block, "")
            if len(follow) < max_len:
                result[block] = follow + c
    return result


# Aided by such table, generate random text one character at the time. For
# the maximum historical appropriateness, run this on a Burroughs computer.

def dissociated_press(table, start, maxpat=3, rng=None):
    rng = Random() if not rng else rng
    yield from start
    pattern = start[-maxpat:]
    while pattern not in table:
        pattern = pattern[1:]
    while True:
        follow = table[pattern]
        # Choose a random continuation for pattern and result.
        c = rng.choice(follow)
        yield c
        # Update the pattern also, shortening if necessary.
        pattern += c
        if len(pattern) > maxpat:
            pattern = pattern[1:]


def __demo():
    # Convert the contents of text file into one string.
    with open('warandpeace.txt', encoding="utf-8") as wap:
        text = "".join(wap)
    table = build_table(text, 6, 500)
    print(f"Table contains {len(table)} entries.")
    for maxpat in range(1, 7):
        print(f"\nRandom text with maxpat value {maxpat}:")
        text = "".join(islice(dissociated_press(table, 'Prince', maxpat), 600))
        print(text.replace('\n', ' '))


if __name__ == "__main__":
    __demo()
