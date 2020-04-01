from random import Random

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

def pangram_finder(text, rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    count, best = [rng.randint(2, 50) for i in range(26)], 0
    
    while True:
        # Fill in text placeholders with names for each number.
        filled = text
        for i, c in enumerate(letters):
            filled = filled.replace(f"${c}", int_to_english(count[i]))       
        # Count the actual counts of letters.
        lfill = filled.lower()
        actual = [lfill.count(c) for c in letters]
        # Find the letters whose counts are correct.
        same = "".join([c for (i, c) in enumerate(letters) if count[i] == actual[i]])
        # Replace previous best solution, if this one is better.
        if len(same) > best:
            best = len(same)
            print(f"\n{filled}")
            print(f"Actual: {', '.join([f'{l}:{c}' for (l, c) in zip(letters, count)])}")
            print(f"Same: {same} {len(same)}")
            if best == 26:
                return
        count = actual
        # Perturb some incorrect count a little to get the system
        # out of some local loop that it has got itself stuck inside.
        idx = rng.randint(0, 25)
        if chr(ord('a') + idx) not in same:
            count[idx] += rng.randint(1, 10)

# Replace this sentence with something else, and have the
# above autogram finder run overnight in hopes of finding
# the right numbers to substitute to make the sentence work.
    
text = """This zesty, bookish and joyful quip was composed by
Ilkka Kokkarinen to serve as an example for this course, and it
contains $a a's, $b b's, $c c's, $d d's, $e e's, $f f's, $g g's,
$h h's, $i i's, $j j's, $k k's, $l l's, $m m's, $n n's, $o o's,
$p p's, $q q's, $r r's, $s s's, $t t's, $u u's, $v v's, $w w's,
$x x's, $y y's and finally, as amazing as it may seem, $z z's."""
    
if __name__ == '__main__':
    for x in [42, 3**7, 6**20, -(2**100), 9**200, 10**500]:
        print(f"{x} written in English is {int_to_english(x)}.")
    print("Here are integers 0-100 sorted in alphabetical order:")
    print(sorted(range(0, 101), key = int_to_english))
    print("Here are integers 0-100 sorted in order of name lengths:")
    print(sorted(range(0, 101), key = lambda x: (len(int_to_english(x)), x)))
    print("The numbers that do not contain the letter 'o':")
    print([x for x in range(1000) if 'o' not in int_to_english(x)])
    
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    pangram_finder(text, Random(1234))