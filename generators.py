from random import Random
from fractions import Fraction

# For the Aronson sequence below

from int_to_english import int_to_english

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


def fibonacci(a=1, b=1):
    yield a
    yield b
    curr, prev = a + b, b
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
        for _ in range(v):
            yield v
        v += 1


# Finite for all values of start, or infinite for some? Nobody knows!
# In general, no algorithm can exist that could analyze the given
# generator source code and determine whether the sequence that it
# produces is finite or infinite.

def collatz(start):
    curr = start
    while True:
        yield curr
        if curr == 1:
            break
        curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1


# A generator that produces random integers with an ever-increasing
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
    rng = Random(seed)
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
    # Collect the primes that we discover into primes list.
    primes_ = [2, 3, 5, 7, 11, 13]
    # Handy syntactic sugar for yield inside for-loop
    yield from primes_
    curr = 17
    while True:
        for divisor in primes_:
            if curr % divisor == 0:
                break
            if divisor * divisor > curr:
                primes_.append(curr)
                yield curr
                break
        curr += 2


# Theon's Ladder, devised by Theon of Smyrna (ca. 140 B.C), is a sequence
# of rational numbers that converges to square root of two. This method
# generalizes for the square roots of any integer n. This generator
# produces Fractions a/b that denote the numerator and denominator
# of that fraction. The infinite sequence of Fraction(a, b) converges
# rapidly to the square root of n.

def theons_ladder(n=2, a=1, b=1):
    while True:
        f = Fraction(a, b)
        yield f
        # Let the Fraction class simplify these numbers.
        a, b = f.numerator, f.denominator
        # Original Theon's ladder was just n = 2.
        a, b = a + n * b, a+b


# The next technique comes handy sometimes. Iterate through all integer
# pairs of the form (a, b) where a and b are nonnegative integers so
# that every such pair is visited exactly once.

def all_pairs():
    s = 0  # In each anti-diagonal of the infinite 2D grid, a+b == s.
    while True:
        for a in range(0, s + 1):
            yield a, s-a
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
        prev = prev+1 if prev < n else 1
        for i in range(v):
            q.append(prev)


# Another cute self describing sequence, this one with words.

def aronson(letter='t'):
    n, owed, fragment = 1, [], f'Letter {letter} is in positions '
    while True:
        yield from fragment
        owed.extend(i+n for (i, c) in enumerate(fragment) if c == letter)
        n += len(fragment)
        fragment, owed = int_to_english(owed[0]) + ', ', owed[1:]


# Since a generator can take parameters, we can write a iterator
# decorator that modifies the result of any existing iterator. We
# don't have to care how that iterator was originally defined, as
# long at it somehow produces new values. This gives our decorators
# a maximally general nature.

# Let through every k:th element and discard the rest.

def every_kth(seq, k: int):
    count = k
    for x in seq:
        count -= 1
        if count == 0:
            yield x
            count = k


# Duplicate each element k times.

def stutter(seq, k):
    for x in seq:
        for _ in range(k):
            yield x


def __demo():

    # Python built-in function next allows you to extract elements from a
    # lazy sequence.

    fib_list = []
    fibs = fibonacci();
    for _ in range(20):
        fib_list.append(next(fibs))
    print("First twenty Fibonacci numbers are:")
    print(", ".join(str(f) for f in fib_list))

    # Functions every_kth and stutter cancel each other out.
    print("Collatz sequence starting from 12345 is:")
    print(list(every_kth(stutter(collatz(12345), 3), 3)))

    # Take primes until they become greater than one thousand.
    print("Here is every seventh prime number up to one thousand:")
    print(list(takewhile((lambda x: x <= 1000), every_kth(primes(), 7))))

    print("Here are the first 1000 elements of Kolakoski(2):")
    print("".join(str(x) for x in islice(kolakoski(2), 1000)))

    print("Here are the first 1000 elements of Kolakoski(3):")
    print("".join(str(x) for x in islice(kolakoski(3), 1000)))

    print("First 1000 characters of modified Aronson infinite t-sentence:")
    print("".join(islice(aronson(), 1000)))

    print("First 1000 characters of modified Aronson infinite e-sentence:")
    print("".join(islice(aronson('e'), 1000)))

    print("Here are 100 random numbers from increasing scales:")
    print(", ".join(str(x) for x in islice(scale_random(123, 10, 5), 100)))

    print("Here are 100 random numbers from another scale:")
    print(", ".join(str(x) for x in islice(scale_random(123, 5, 10), 100)))

    print("Let us examine Theon's ladder for square root of 7.")
    for i, f in enumerate(islice(theons_ladder(7), 50)):
        print(f"{i}: a = {f.numerator}, b = {f.denominator} error = {float(7 - f*f):.11}")

    print("For c = 2, terms in even positions of Theon's ladder give precisely")
    print("the Pythagorean triples whose legs differ by exactly one:")
    for f in islice(theons_ladder(2), 0, 40, 2):
        a, b = f.numerator, f.denominator
        h, s, e = b, 1, b
        while s < e:
            m = (s+e) // 2
            v = m**2 + (m+1)**2
            if v < h*h:
                s = m+1
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
    print(list(permutations(range(1, n+1))))

    print(f"Here are all possible 3-combinations of {list(range(1, n+1))}.")
    print(list(combinations(range(1, n+1), 3)))

    print(f"Here are all possible 3-multicombinations of {list(range(1, n+1))}.")
    print(list(combinations_with_replacement(range(1, n+1), 3)))


# For good examples of iterators and generators in action, check
# out the itertools recipes section in the Python documentation.

if __name__ == "__main__":
    __demo()
