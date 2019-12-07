# Python list comprehensions can be used to build up lists of answers.

# Squares of numbers from 1 to 99 that contain digit "3".
a = [ x * x for x in range(1, 100) if "3" in str(x)]
print(a)

# Since a comprehension can be made out of any existing sequence,
# more complex lists can be created out of existing comprehensions.

# The members of previous list that contain are between 500 and 2000.

b = [x for x in a if 500 < x < 2000]
print(b)

# List comprehensions can do a lot of work that we later do with loops.
# For example, let's find all the Unicode characters that are lowercase
# letters and produce a list of them.

import unicodedata as ud

letter_category = ud.category('a')

c = [chr(c) for c in range(100000) if ud.category(chr(c)) == letter_category]
print("Here are the Unicode characters that are lowercase letters:")
print("".join(c)) # There are quite a few.
print("")

# If the filtering depends also on the position of the element in the
# sequence, the Python function enumerate produces a sequence that consists
# of pairs of positions and the original elements in those positions.

d = "".join([ x for (i, x) in enumerate(list("Hello world!")) if i % 2 == 0 ])
print(f"Every other character produces string {d!r}")

d = "".join([ x for x in "Hello world, how are you there?" if x != ' '])
print(f"Removing whitespaces produces string {d!r}")

# A word starts at a non-whitespace character that either starts the whole thing
# or is preceded by a whitespace character.

text = "Let us try to capitalize every word in this silly little sentence."
text = "".join(
    [ (x.upper() if (i == 0 or text[i-1] == ' ') else x) for (i, x) in enumerate(text) ]
    )
print(text)

# Dictionaries can be built up with analogous dictionary comprehensions.

e = { x:x*x for x in range(100) }
print(e[5], e[55])

# Let's find all integer names in the current namespace and add them up.
# Note that since dir returns a list of strings, each name as a string, we
# need to acquire the current namespace as a dictionary from which we can
# then look up the objects associated with those names.

v1 = 42
v2 = 99
gl = globals() # Acquire the dictionary of current namespace
f = sum([gl[x] for x in dir() if type(gl[x]) == type(42)])
print(f"The sum of current integer variables equals {f}.")

# The list comprehension generates a list of all elements to exist in memory
# simultaneously, which may be prohibitive if the number of elements is very
# large, even astronomical. An iterator comprehension produces an iterator
# that produces the elements one at the time as needed by the computation.

# Squares of the first googol integers.

h = ( x * x for x in range(10 ** 100) )

# Notice how we didn't run out of memory. Many functions that operate on
# iterators are smart enough to stop once they know the answer, so they will
# not get stuck if the iterator sequence is very large or even infinite.

print(f"Does there exist an integer greater 40? {any(x > 40 for x in h)}")
print(f"Are all integers divisible by 7? {all(x % 7 == 0 for x in h)}" )

# Since the actual elements can be computed arbitrarily from the elements of
# the original sequence, we can find out the positions where the original
# elements satisfy some particular condition.

g1 = ( 29 % n == 0 for n in range(3, 29, 2) )
g2 = ( 45 % n == 0 for n in range(3, 45, 2) )

# Beware of the fact that in a generator expression, the for-part is
# evaluated at declaration, whereas the if-part is evaluated at execution.
words = ["hello", "there", "world"]
five = (word for word in words if word in words)
words = ["hello", "ilkka"]
print(list(five)) # ['hello']

# The Python functions all and any can be used to check if any or all elements
# of a sequence, produced either with comprehension or not, have some desired
# property. (Note that for empty sequence, all is trivially true, and any is
# trivially false.)

print(f"Is the number 29 a prime number? {not any(g1)}")
print(f"Is the number 45 a prime number? {not any (g2)}")

text = "Hello, world!"
s = [ ud.category(x) == ud.category(' ') for x in text ]
print(f"Does the string {text!r} contain any spaces? {any(s)}")

# An inner comprehension can be nested inside the evaluation of an outer
# comprehension, to produce a sequence whose elements are sequences.

u1 = [ [ x for x in range(n + 1) ] for n in range(10) ]
print(u1)

# This technique allows us to partition a sequence into another sequence
# of its consecutive elements, either overlapping or not.

words = "Hello there, world! How are you doing today on this fine sunny day of coding?".split()

# Overlapping sequences of 3 consecutive elements by having the range of n skip by default 1.
u2 = [ " ".join([words[x] for x in range(n, n + 3) ]) for n in range(len(words) - 2 ) ]
print(u2)

# Non-overlapping sequences of 3 consecutive elements by having the range of n skip by 3.
u3 = [ " ".join([words[x] for x in range(n, n + 3) ]) for n in range(0, len(words) - 2, 3 ) ]
print(u3)