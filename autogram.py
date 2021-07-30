from random import Random
from int_to_english import int_to_english


# Find an autogram, a text that describes in English how many times
# each letter appears inside it. As with many of the 109 lab problems,
# this example was inspired by the works of the late great Martin
# Gardner and his collected columns on recreational mathematics in
# the Scientific American magazine.

def autogram_finder(text, rng, verbose=True, perturb=20):
    letters, rounds = "abcdefghijklmnopqrstuvwxyz", 0
    count, best = [rng.randint(2, 50) for _ in letters], 0

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
        same = "".join([c for (i, c) in enumerate(letters)
                        if count[i] == actual[i]])
        # Replace the previous best solution, if this one is better.
        if len(same) > best:
            best = len(same)
            if verbose:
                print(f"\n{filled}")
                print(f"Actual: {', '.join([f'{l}:{c}' for l, c in zip(letters, actual)])}")
                print(f"Matched {len(same)} letters '{same}'.")
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

__text = """This zesty, bookish and joyful quip was composed by
Ilkka Kokkarinen to serve as an example for this course, and it
contains $a a's, $b b's, $c c's, $d d's, $e e's, $f f's, $g g's,
$h h's, $i i's, $j j's, $k k's, $l l's, $m m's, $n n's, $o o's,
$p p's, $q q's, $r r's, $s s's, $t t's, $u u's, $v v's, $w w's,
$x x's, $y y's and finally, to top it all off, $z z's."""
__text = __text.replace("\n", " ")
__text = __text.replace("\t", " ")

# This zesty, bookish and joyful quip was composed by Ilkka
# Kokkarinen to serve as an example for this course, and it
# contains thirteen a's, three b's, four c's, five d's,
# forty-seven e's, thirteen f's, one g's, eleven h's, twenty
# i's, two j's, seven k's, twelve l's, three m's, twenty-five
# n's, twenty-three o's, five p's, two q's, sixteen r's,
# forty-one s's, thirty-three t's, six u's, eleven v's, nine
# w's, four x's, eleven y's and finally, to top it all off,
# two z's.

# (Count them if you don't believe me.)


def __autogram_demo():
    # When using a randomized algorithm, it is good to used a fixed
    # seed to make the results repeatable.
    autogram_finder(__text, Random(12345), True, 20)


if __name__ == '__main__':
    __autogram_demo()
