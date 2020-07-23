import random


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
            # Store only the first mlen occurrences of pattern.
            if len(follow) < mlen:
                result[pattern[j:]] = follow + next_char
    return result


# Using the previous table, generate m characters of random text.

def dissociated_press(table, m, result, maxpat=3):
    pattern = result[:min(len(result), maxpat)]
    while m > 0:
        follow = table.get(pattern, "")
        if(len(follow) > 0):
            # Choose a random continuation for pattern and result.
            c = random.choice(follow)
            result += c
            pattern += c
            m -= 1
            # Shorten the pattern if it grows too long.
            if len(pattern) > maxpat:
                pattern = pattern[1:]
        else:  # Nothing for the current pattern, so shorten it.
            pattern = pattern[1:]
    return result


if __name__ == "__main__":
    # Convert the contents of text file into one string.
    with open('warandpeace.txt', encoding="utf-8") as wap:
        text = "".join(wap)
    table = build_table(text, 6, 500)
    print(f"Table contains {len(table)} entries.")
    for maxpat in range(1, 7):
        print(f"\nRandom text with maxpat value {maxpat}:")
        text = dissociated_press(table, 600, "A", maxpat)
        print(text.replace('\n', ' '))
