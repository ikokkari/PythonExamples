import random
from fractions import Fraction
from autogram import int_to_english

# The itertools module defines tons of handy functions to perform
# computations on existing iterators, to be combined arbitrarily.

from itertools import takewhile, islice, permutations, combinations, combinations_with_replacement

# The "double-ended queue" or "deque" allows efficient push
# and pop operations from both ends of the queue, whereas a
# Python list only allows efficient operations in one end.

from collections import deque

# A generator is a function that, unlike a regular function that
# always forgets what it has done and starts from beginning each
# time it is called, a generator remembers where it left off and
# continues from there at the next call. In Python, generators
# are an easy way to define lazy sequences that produce their
# elements one element at the time, only doing any work when
# actually asked to do so.

# There is nothing in the laws of nature or man that says that
# a lazy sequence could not just as well be infinite. The users
# of that sequence can (and always should) decorate it with
# itertools.islice to extract the finite prefix instead of
# using more low-level old-timey and non-Pythonic techniques.

# To get started, the classic chestnut of Fibonacci numbers.
# It's like that one is a law of some sorts for CS instructors.


def fibonacci():
    yield 1
    yield 1
    curr, prev = 2, 1
    while True:  # Infinite loop for infinite sequence...
        yield curr  # Pause to give out this element.
        curr, prev = curr + prev, curr


# One one, two twos, three threes, four fours, five fives, ...
# Nested loops come often handy here, although since our goal is
# to replace loops with lazy sequences, this function could be
# written in a more pretty form with itertools functions.

def pyramid_series():
    v = 1
    while True:
        for i in range(v):
            yield v
        v += 1


# Finite for all values of start, or infinite for some? Nobody knows!
# In general, no algorithm can exist that could analyze the given
# generator source code and determine whether the sequence that it
# produces is finite or infinite.

def collatz(start):
    while True:
        yield start
        if start == 1:
            break
        elif start % 2 == 0:
            start = start // 2
        else:
            start = 3 * start + 1


# A generator that produces random integers with an ever increasing
# scale. Handy for generating random test cases in tester.py that
# produce test cases from all scales so that the first test cases
# are guaranteed to be small. The scale determines how wide range
# the random increase from the previous element is taken. After
# every skip elements, the scale gets multiplied by its original value.
# Everything is again nice and tight integer arithmetic. (Well, I
# guess that inside a computer, everything is integer arithmetic
# anyway...)

def scale_random(seed, scale, skip):
    # The seed value determines the future random sequence.
    rng = random.Random(seed)
    curr, count, orig = 1, 0, scale
    while True:
        curr += rng.randint(1, scale)
        yield curr
        count += 1
        if count == skip:
            scale = scale * orig
            count = 0


# Prime numbers, remembering all the prime numbers generated so far. To
# test whether a number is prime, it is sufficient to test divisibility
# only by the smaller primes found so far.

def primes():
    primes = [2, 3, 5, 7, 11]
    # Handy syntactic sugar for yield inside for-loop
    yield from primes
    curr = 13
    while True:
        for divisor in primes:
            if curr % divisor == 0:
                break
            if divisor * divisor > curr:
                primes.append(curr)
                yield curr
                break
        curr += 2


# Theon's Ladder, devised by Theon of Smyrna (ca. 140 B.C), is a series
# of rational numbers that converge to square root of two. This method
# generalizes for the square roots of any integer c. This generator
# produces two-tuples (a, b) that denote the numerator and denominator
# of that fraction, the infinite sequence converges to square root of n.

def theons_ladder(n=2, a=1, b=1):
    while True:
        yield a, b
        # Original Theon's ladder was just n = 2.
        a, b = a + n * b, a + b


# The next technique comes handy sometimes. Iterate through all
# pairs of the form (a, b) where a and b are nonnegative integers
# so that every such pair is visited exactly once.

def all_pairs():
    s = 0
    # In each antidiagonal of the infinite 2D grid, a + b == s.
    while True:
        for a in range(0, s + 1):
            yield(a, s - a)
        s += 1

# That one is handy when you need to loop through the infinite
# quadrant of pairs (a, b) where a and b are natural numbers,
# and you need to find some pair (a, b) that satisfies the thing
# that your code is looking for. Use the all_pairs generator
# to systematically sweep through this infinite plane until
# you find the (a, b) that is closest to origin (0, 0).


# The Kolakoski sequence whose elements describe the run-length
# encoding of that very same sequence. That is, this sequence
# describes its own structure. (Keanu says whoa.)
# https://en.wikipedia.org/wiki/Kolakoski_sequence

def kolakoski(n=2):
    yield 1
    yield 2
    # The queue q contains the part of the sequence that has
    # been computed but not yet yielded.
    q, prev = deque([2]), 2
    while True:
        v = q.popleft()
        yield v
        prev = prev + 1 if prev < n else 1
        for i in range(v):
            q.append(prev)


# Another cute self describing sequence, this one with words.

def aronson(letter='t', start='Letter t is in positions '):
    n, tees, curr = 1, [], start
    while True:
        yield from curr
        tees.extend([i + n for (i, c) in enumerate(curr) if c == letter])
        n += len(curr)
        curr, tees = int_to_english(tees[0]) + ', ', tees[1:]


def aronson2(letter='t', start='Letter t is in positions '):
    tees = [i + 1 for (i, c) in enumerate(start) if c == letter]
    n = len(start) + 1
    yield from start

    while True:
        i, tees = tees[0], tees[1:]
        word = int_to_english(i) + ", "
        yield from word
        tees.extend([i + n for (i, c) in enumerate(word) if c == letter])
        n += len(word)

# Since a generator can take parameters, we can write a iterator
# decorator that modifies the result of any existing iterator. We
# don't have to care how that iterator was originally defined, as
# long at it somehow produces new values. This gives our decorators
# a maximally general nature.

# Let through every k:th element and discard the rest.

def every_kth(seq, k):
    count = k
    for x in seq:
        count -= 1
        if count == 0:
            yield x
            count = k


# Duplicate each element k times.

def stutter(seq, k):
    for x in seq:
        for i in range(k):
            yield x


# Extract all unique permutations of 0, ..., n-1 from sequence,
# assuming that sequence contains only values in 0, ..., n-1.

def unique_permutations(it, n):
    # Set of permutations that we have already seen before.
    seen = set()
    # Current sublist of n most recent elements.
    curr = []
    # Counts of how many times each value occurs in current sublist.
    counts = [0 for i in range(n)]
    # How many of those counts are ones, for quick lookup.
    ones = 0
    # Iterate through the values produced by the iterator.
    for v in it:
        curr.append(v)
        # If sublist is too long, shorten it from the front.
        if len(curr) > n:
            out = curr[0]  # Make note of the outgoing element.
            curr = curr[1:]
            # Update the count for the outgoing element out.
            counts[out] -= 1
            if counts[out] == 1:
                ones += 1
            elif counts[out] == 0:
                ones -= 1
        # Update the count for the current element.
        counts[v] += 1
        if counts[v] == 1:
            ones += 1
            # If each value occurs exactly once, this is a permutation.
            if ones == n:
                currt = tuple(curr)
                if currt not in seen:
                    seen.add(currt)
                    yield currt
        elif counts[v] == 2:
            ones -= 1



# Since the iterator produces values one at the time, we could
# analyze sequences too long to fit in memory all at once. First,
# generator that produces random numbers in 0, ..., n-1 so that
# a number that was seen recently cannot be emitted this round.

def tabu_generator(n, len_, recent=None):
    if recent is None:
        recent = n // 2
    tabu = []
    while len_ > 0:
        v = random.randint(0, n-1)
        if v not in tabu:
            yield v
            tabu.append(v)
            if len(tabu) > recent:
                tabu = tabu[1:]
            len_ -= 1


# Count how many permutations occur for different values of recent.

for recent in range(0, 6):
    itemgen, total = tabu_generator(8, 10**5, recent), 0
    for perm in unique_permutations(itemgen, 8):
        total += 1
    print(f"With tabu length {recent}, {total} unique permutations.")

# Constructing the shortest possible sequence that contains all
# permutations of {0, ..., n-1} is an unsolved mathematical problem.
# Google "greg egan haruhi superpermutation" for an interesting story.

# Functions every_kth and stutter cancel each other out.
print("Collatz sequence starting from 12345 is:")
print(list(every_kth(stutter(collatz(12345), 3), 3)))

# Extract the unique permutations from the list.
items = [0, 2, 1, 0, 1, 2, 0, 0, 2, 2, 0, 1]
print(f"Unique 3-permutations of {items} are:")
print(list(unique_permutations(items, 3)))

# Take primes until they become greater than thousand.
print("Here is every seventh prime number up to one thousand:")
print(list(takewhile((lambda x: x <= 1000), every_kth(primes(), 7))))

print("Here are the first 1000 elements of Kolakoski(2):")
print("".join((str(x) for x in islice(kolakoski(2), 1000))))

print("Here are the first 1000 elements of Kolakoski(3):")
print("".join((str(x) for x in islice(kolakoski(3), 1000))))

print("First 2000 characters of modified Aronson infinite t-sentence:")
print("".join(islice(aronson(), 2000)))

print("First 2000 characters of modified Aronson infinite e-sentence:")
print("".join(islice(aronson('e', 'Letter e is in positions '), 2000)))

print("Here are 100 random numbers from increasing scales:")
print(", ".join((str(x) for x in islice(scale_random(123, 10, 5), 100))))

print("Here are 100 random numbers from another scale:")
print(", ".join((str(x) for x in islice(scale_random(123, 5, 10), 100))))

print("Let us examine Theon's ladder for square root of 7.")
for i, (a, b) in enumerate(islice(theons_ladder(7), 30)):
    f = Fraction(a, b)
    f = f * f
    print(f"{i}: a = {a}, b = {b} error = {float(7 - f):.11}")

print("For c = 2, terms in even positions of Theon's ladder give")
print("us Pythagorean triples whose legs differ by exactly one:")
for (a, b) in islice(theons_ladder(2), 0, 40, 2):
    h, s, e = b, 1, b
    while s < e:
        m = (s + e) // 2
        v = m**2 + (m+1)**2
        if v < h * h:
            s = m + 1
        else:
            e = m
    print(f"({s}, {s+1}, {h})", end=" ")
print()

# What other mysteries of number theory are hiding inside this
# ladder for various other starting values of a, b and c?

# Iterators can be combined into various combinatorial possibilities.
# Again, even though there are exponentially many elements produced,
# these elements are generated lazily one at the time as needed. We
# could iterate through trillions of combinations without running out
# of memory, assuming we had the patience to wait out the answer.

# For small n, these combinations are still pretty tolerable. You can
# try the effect of increasing n (just by little!) to see how the
# sequences grow exponentially.

n = 4   # Try also 5 or 6.

print(f"Here are all possible permutations of {list(range(1, n+1))}.")
print(list(permutations(range(1, n + 1))))

print(f"Here are all possible 3-combinations of {list(range(1, n+1))}.")
print(list(combinations(range(1, n + 1), 3)))

print(f"Here are all possible 3-multicombinations of {list(range(1, n+1))}.")
print(list(combinations_with_replacement(range(1, n + 1), 3)))

# For good examples of iterators and generators in action, check
# out the itertools recipes section in the Python documentation.
