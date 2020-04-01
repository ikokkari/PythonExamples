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
        return tens if n % 10 == 0 else f"{tens}-{__int_to_eng(n % 10)}" 
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
        return f"{first} googol" if rest == "zero" else f"{first} googol and {rest}"
    # Otherwise, break the number into blocks of three and convert.
    result, p = [], 0
    while n > 0:
        trip, n = n % 1000, n // 1000        
        if trip > 0:
            if p == 0:
                result.append(__int_to_eng(trip))
            else:
                result.append(__int_to_eng(trip) + " " + __pows[p])
        p += 3
    return " ".join(reversed(result))

# Find an autogram, a text that describes in English how many times
# each letter appears inside it. As with many of the 109 lab problems, 
# this example was inspired by the works of the late great Martin
# Gardner and his collected columns on recreational mathematics in
# the Scientific American magazine.
    
def autogram_finder(text, rng, verbose=True, perturb = 20):
    letters, rounds = "abcdefghijklmnopqrstuvwxyz", 0
    count, best = [rng.randint(2, 50) for c in letters], 0
    
    while True:
        rounds += 1
        # Fill in text placeholders with names for each number.
        filled = text
        for n, c in zip(count, letters):
            filled = filled.replace(f"${c}", int_to_english(n))
        filled = filled.replace("$$", int_to_english(sum(count)))
        # Count the actual counts of letters.
        lfill = filled.lower()
        actual = [lfill.count(c) for c in letters]
        # Find the letters whose counts are correct.
        same = "".join([c for (i, c) in enumerate(letters) if count[i] == actual[i]])
        # Replace the previous best solution, if this one is better.
        if len(same) > best:
            best = len(same)
            if verbose:
                print(f"\n{filled}")
                print(f"Actual: {', '.join([f'{l}:{c}' for (l, c) in zip(letters, actual)])}")
                print(f"Matched {len(same)} letters '{same}' in {rounds} rounds.")
            if best == 26:
                return filled
        count = actual
        # Perturb some incorrect count a little to get the system
        # out of some local loop that it has got itself stuck inside.
        idx = rng.randint(0, len(letters) - 1)
        if letters[idx] not in same or rng.randint(0, 99) < perturb:
            count[idx] += rng.randint(1, 10)

# Replace this text with something else, and then have the
# above autogram finder run overnight in hopes of finding
# the right numbers to make the sentence work. Inside text,
# $c is the count for the character c, and $$ is the total
# number of letters in the text. (That one makes the search
# far more difficult.)
    
text = """This zesty, bookish and joyful quip was composed by
Ilkka Kokkarinen to serve as an example for this course, and it
contains $a a's, $b b's, $c c's, $d d's, $e e's, $f f's, $g g's,
$h h's, $i i's, $j j's, $k k's, $l l's, $m m's, $n n's, $o o's,
$p p's, $q q's, $r r's, $s s's, $t t's, $u u's, $v v's, $w w's,
$x x's, $y y's and finally, to top it all off, $z z's."""
text = text.replace("\n", " ")
text = text.replace("\t", " ")

# This zesty, bookish and joyful quip was composed by Ilkka
# Kokkarinen to serve as an example for this course, and it
# contains thirteen a's, three b's, four c's, five d's,
# forty-seven e's, thirteen f's, one g's, eleven h's, twenty
# i's, two j's, seven k's, twelve l's, three m's, twenty-five
# n's, twenty-three o's, five p's, two q's, sixteen r's,
# forty-one s's, thirty-three t's, six u's, eleven v's, nine
# w's, four x's, eleven y's and finally, to top it all off,
# two z's.


if __name__ == '__main__':
    for x in [42, 3**7, 6**20, -(2**100), 9**200, 10**500]:
        print(f"{x} written in English is {int_to_english(x)}.")
    print("Here are integers 0-100 sorted in alphabetical order:")
    print(sorted(range(0, 101), key = int_to_english))
    print("Here are integers 0-100 sorted in order of name lengths:")
    print(sorted(range(0, 101), key = lambda x: (len(int_to_english(x)), x)))
    print("The numbers that do not contain the letter 'o':")
    print([x for x in range(1000) if 'o' not in int_to_english(x)])
   
    # When using a randomized algorithm, it is good to used a fixed
    # seed to make the results repeatable.
    autogram_finder(text, Random(9999), perturb = 0)