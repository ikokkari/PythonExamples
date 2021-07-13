# A tuple is essentially a list, but immutable. Tuples can be
# indexed and iterated just like lists. Tuples are useful, for
# example, in representing coordinates in fixed dimensions.

t1 = (1, 5, -2)
t2 = (6, -4, 9)

# Tuples can be assigned in one swoop under various combinations. These
# assignments are executed as if they were happening simultaneously.
# Note that it is the comma operator that creates the tuple, not the
# optional parentheses, but using the parentheses is still often clearer.

a, b = 1, 2
print(f"a is {a}, b is {b}")  # 1 2
b, a = a, b
print(f"a is {a}, b is {b}")  # 2 1

a, b, *c = 1, 2, 3, 4, 5
print(f"a is {a}, b is {b}, c is {c}")  # 1 2 [3, 4, 5]
a, *b, c, = 1, 2, 3, 4, 5
print(f"a is {a}, b is {b}, c is {c}")  # 1 [2, 3, 4] 5
*a, b, c = 1, 2, 3, 4, 5
print(f"a is {a}, b is {b}, c is {c}")  # [1, 2, 3] 4 5

# Parentheses disambiguate syntax in some situations. It is never
# never wrong to use redundant parentheses here, or for that matter,
# in any situation where these parentheses make the meaning clear
# to the reader. Who wants to memorize all the precedence and
# associativity rules of even one programming language, let alone
# a dozen different languages that you use sporadically?

t1 = 1, 2, 3, 4, 5    # a tuple of 5 elements, each an integer
t2 = 1, (2, 3, 4), 5  # a tuple of 3 elements, one of which is a tuple
print(f"len(t1) == {len(t1)}, len(t2) == {len(t2)}")
# a 5-element tuple whose middle element is boolean
t3 = 1, 2, 3 == 1, 2, 3
# a boolean result of comparing two tuples
t4 = (1, 2, 3) == (1, 2, 3)
print(t3)  # (1, 2, False, 2, 3)
print(t4)  # True

# Since tuples are immutable, the following would be errors:
# t1[2] = 7       # changing the element at the given index
# t1.append(10)   # append, or any other in-place modification

# As usual, things can be converted to other types as needed.

li = list(t1)     # create a list with the same elements
li.append(10)     # lists can be freely modified
tu = tuple(li)    # and then turned back into an unmodifiable tuple
print(tu)         # (1, 5, -2, 10)

# A tuple can even be empty, but a one-element tuple needs a silly trick
# to distinguish it from a scalar expression inside parentheses. The
# syntax of every programming language must be unambiguous so that every
# program and line of code means exactly one thing and that alone.

emptytuple = ()
singletontuple = (42,)
x = (42)  # an ordinary integer, defined in a redundant way

print(emptytuple, singletontuple, x)

# Tuple order comparison happens lexicographically. If the first element
# does not resolve the issue, look at second, and so on.

print((42, 1, 3) < (17, 1000000000, 99))  # False
print((42, 17, 99) < (42, 17, 100))  # True
