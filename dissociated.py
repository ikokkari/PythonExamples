import random
from itertools import islice


# Read through the text and build a dictionary that, for each found
# pattern up to length n, gives the string of letters that follow that
# pattern in the original text.

def build_table(text, n=3, mlen=100):
    result = {}
    for i in range(len(text) - n - 1):
        # The n-character string starting at position i.
        pattern = text[i:i+n]
        # The character that follows that pattern.
        next_char = text[i + n]
        # Update the dictionary for each suffix of the current pattern.
        for j in range(n):
            follow = result.get(pattern[j:], "")
            # Store only the first mlen occurrences of each pattern.
            if len(follow) < mlen:
                result[pattern[j:]] = follow + next_char
    return result


# Aided by such table, generate random text one character at the time.

def dissociated_press(table, start, maxpat=3):
    yield from start
    pattern = start[-maxpat:]
    while pattern not in table:
        pattern = pattern[1:]
    while True:
        follow = table[pattern]
        # Choose a random continuation for pattern and result.
        c = random.choice(follow)
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
        text = "".join(islice(dissociated_press(table, 'Queen', maxpat), 600))
        print(text.replace('\n', ' '))


if __name__ == "__main__":
    __demo()
