# A set is collection with no indexing, but it is optimized for
# quickly determining whether the set currently contains some
# particular element, along with the set theoretical operations
# such as union and intersection. A set can be built from a list,
# a tuple or any other iterable.

# Duplicate elements are discarded, so Larry will be in the first
# set only once despite being listed twice.

names1 = {'Larry', 'Johnny', 'Billy', 'Mary', 'Larry'}
names2 = {'Max', 'Lena', 'Larry', 'Billy', 'Tina'}

# Membership check is done with the operators 'in' and 'not in'.

for name in ['Tony', 'Mary', 'Johnny']:
    print(f"Is {name} in names1? {name in names1}")

# The basic set theoretical operations are available as methods.

union = names1.union(names2)
difference = names1.difference(names2)
intersection = names1.intersection(names2)

print(f"Union of names is {union}.")
print(f"Their difference is {difference}.")
print(f"Their intersection is {intersection}.")

# Sets do not allow indexing, but they do allow iteration. The
# guarantee of iteration order depends on the Python version. Old
# versions guaranteed only that the iteration order stays the same
# in consecutive iterations, provided that the set is not mutated
# in between. Since Python 3.7, the iteration order is guaranteed
# to be same as the insertion order, which comes handy sometimes.

print("First time through this set:")
for x in names2:
    print(f"{x} is in the second set.")

print("Second time through the same set:")
for x in names2:
    print(f"{x} is in the second set.")

# A dictionary is a mapping that associates values to keys. Python
# has a dictionary data type in the language itself. To create a
# dictionary object, simply list the pairs of keys and values
# between curly braces, each key separated from its value with a
# colon.

scores = {'Mary': 14, 'Tony': 8, 'Billy': 20, 'Lena': 3}

# Since the same notation of curly braces is used for both sets and
# dictionaries, I wonder which one {} is? (It's a dictionary.)

print("The type of {} " f"is {type({})}.")  # <class 'dict'>

# A dictionary can be "indexed" with its keys.

print(scores['Mary'])                # 14
scores['Lena'] = scores['Lena'] + 5  # Lena scores 5 more points
print(scores['Lena'])                # 8
scores['Anne'] = 12                  # add Anne in the dictionary
del scores['Tony']                   # and remove Tony

# Trying to index a dictionary with a nonexistent key would be a
# runtime KeyError. To avoid this, use the method get that takes
# the key and the default value to use whenever the key is not in
# the dictionary:

print(scores.get('Alice', 0))        # 0

# Iterating through a dictionary goes through its keys. Iterating
# through the items of the dictionary goes through a sequence of
# tuples of (key, value) pairs. The guarantees for iteration order
# are the same as they are for sets.

print([x for x in scores])
# ['Billy', 'Lena', 'Anne', 'Mary']

print([x for x in scores.items()])
# [('Billy', 20), ('Lena', 8), ('Anne', 12), ('Mary', 14)]

# One dictionary can contain only one entry for equal keys in the
# sense of operator ==, even when these objects are distinct.

numdic = {42: "Hello", 42.0: "World"}  # pyflakes gives a warning...
print(42 == 42.0)    # True (implicit cast)
print(42 is 42.0)    # False (here to show that ints are not floats)
print(numdic[42])    # World (and yet both 42 and 42.0 work the same)
print(numdic[42.0])  # World (when used as dictionary keys)
