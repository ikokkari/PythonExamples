def create_zigzag(rows, cols, start = 1):
    rows = [list(range(x, x + cols))
            for x in range(start, start + rows * cols, cols)]
    return [(row if idx % 2 == 0 else list(reversed(row)))
            for (idx, row) in enumerate(rows)]


def bulgarian_solitaire(piles, k):
    goal, count = list(range(1, k+1)), 0
    while True:
        if len(piles) == k and sorted(piles) == goal:
            return count
        count += 1
        piles = [p - 1 for p in piles if p > 1] + [len(piles)]


vows = 'aeiouAEIOU'
def reverse_vowels(text):
    vowels, result = [c for c in text if c in vows], ''
    for c in text:
        if c in vows:
            ch = vowels.pop()
            ch = ch.upper() if c in vows[-5:] else ch.lower()
            result += ch
        else:
            result += c
    assert len(vowels) == 0
    return result