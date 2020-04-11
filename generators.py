# A generator is a function that, unlike a regular function that
# always forgets what it has done and starts from beginning each
# time it is called, a generator remembers where it left off and
# continues from there at the next call. In Python, generators
# are an easy way to define lazy sequences that produce their
# elements one element at the time, only doing any work when
# actually asked to do so.

# There is nothing in the laws of nature or man that says that
# a lazy sequence could not just as well be infinite. The users
# of that sequence can always decorate it with itertools.islice
# to extract the finite prefix.

# To get started, the classic chestnut of Fibonacci numbers.

def fibonacci():
    yield 1
    yield 1
    curr, prev = 2, 1    
    while True: # Infinite loop for infinite sequence...
        yield curr # Good thing execution automatically pauses here.
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
# produces is finite.

def collatz(start):
    while True:
        yield start
        if start == 1: break
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
    yield from primes # Handy syntactic sugar for yield inside for-loop
    current = 13
    while True:        
        for divisor in primes:
            if current % divisor == 0:
                break
            if divisor * divisor > current:
                primes.append(current)
                yield current
                break
        current += 2

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
# grid of pairs (x, y) where x and y are natural numbers, and
# you need to find some pair (x, y) that satisfies the thing
# that your code is looking for. Use the all_pairs generator
# to systematically sweep through this infinite plane until
# you find the (x, y) that is closest to origin (0, 0).

# One more infinite generator, the Kolakoski sequence whose
# elements describe the run-length encoding of that sequence.
# That is, the sequence describes its own structure.
# https://en.wikipedia.org/wiki/Kolakoski_sequence

# The "double-ended queue" or "deque" allows efficient push
# and pop operations from both ends of the queue, whereas a
# Python list only allows efficient operations in one end.
from collections import deque

def kolakoski(n = 2):
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
        
    
# Since a generator can take parameters, we can write a iterator
# decorator that modifies the result of any existing iterator. We
# don't have to care how that iterator was originally defined, as
# long at it somehow produces new values. This gives our decorators
# a maximally general nature.

# Let through every k:th element and discard the rest.
def every_kth(it, k):
    count = k
    for x in it:
        count -= 1
        if count == 0:            
            yield x
            count = k

# Duplicate each element k times.
def stutter(it, k):
    for x in it:
        for i in range(k):
            yield x

# Extract all n-element sublists of the sequence from iterator.
def ngrams(it, n):
    result = []
    for v in it:
        result.append(v)
        if len(result) >= n:
            yield result
            result = result[1:]

# Extract all unique permutations of 0, ..., n-1 from the sequence,
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
            out = curr[0] # Note the outgoing element
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

# Functions every_kth and stutter cancel each other out.
print("Collatz sequence starting from 12345 is:")
print(list(every_kth(stutter(collatz(12345), 3) ,3)))

msg = "Hello world, how are you today?"
print("A string split into three consecutive words, overlapping:")
print(list(ngrams(msg.split(" "), 3)))

# Extract the unique permutations from the list.
items = [0, 2, 1, 0, 1, 2, 0, 0, 2, 2, 0, 1]
print(f"Unique 3-permutations of {items} are:")
print(list(unique_permutations(items, 3)))

# Since the iterator produces values one at the time, we could
# analyze sequences too long to fit in memory all at once. First,
# generator that produces random numbers in 0, ..., n - 1 so that
# a number that was seen recently cannot be emitted this round.

import random
def tabu_generator(n, len_, recent = None):
    if recent == None:
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
    print(f"Using tabu length {recent}, found {total} unique permutations.")

# Constructing the shortest possible sequence that contains all
# permutations of {0, ..., n-1} is an unsolved mathematical problem.
# Google "greg egan haruhi superpermutation" for an interesting story.

# The itertools module defines tons of handy functions to perform
# computations on existing iterators, to be combined arbitrarily.

import itertools as it

# Python's built in function enumerate is handy if you also need
# the position of each iterated element. The hand decorator
# itertools.islice achieves the same end as the square bracket
# slicing opreator applied to eager sequences, and its common
# use is to turn an infinite sequence into a finite one.

print("Here are the first 5 prime numbers that contain their own index:")
print(list(it.islice(((i, p) for (i, p) in enumerate(primes()) if str(i) in str(p)), 5)))

# Take primes until they become greater than thousand.
print("Here is every seventh prime number up to one thousand:")
print(list(it.takewhile( (lambda x: x <= 1000), every_kth(primes(), 7))))

print("Here are the first 1000 elements of Kolakoski(2):")
print("".join((str(x) for x in it.islice(kolakoski(2), 1000))))

print("Here are the first 1000 elements of Kolakoski(3):")
print("".join((str(x) for x in it.islice(kolakoski(3), 1000))))

print("Here are 100 random numbers from increasing scale:")
print(", ".join((str(x) for x in it.islice(scale_random(123, 10, 5), 100))))

print("Here are 100 random numbers from different scale:")
print(", ".join((str(x) for x in it.islice(scale_random(123, 5, 10), 100))))

# Iterators can be combined into various combinatorial possibilities.
# Again, even though there are exponentially many elements produced,
# these elements are generated lazily one at the time as needed. We
# could iterate through trillions of combinations without running out
# of memory, assuming we had the patience to wait out the answer.

# For small n, these combinations are still pretty tolerable. You can
# try the effect of increasing n (just by little!) to see how the
# sequences grow exponentially.

n = 4   # Try 5 or 6.

print(f"Here are all possible permutations of {list(range(1, n+1))}.")
print(list(it.permutations(range(1, n + 1))))

print(f"Here are all possible 3-combinations of {list(range(1, n+1))}.")
print(list(it.combinations(range(1, n + 1), 3)))

print(f"Here are all possible replacement combinations of {list(range(1, n+1))}.")
print(list(it.combinations_with_replacement(range(1, n + 1), 3)))

# For more examples of iterators and generators, see the itertools
# recipes section in Python documentation.