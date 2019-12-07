# A set is a list, but it has no indexing, and is optimized for checking
# if the set currently contains the given element, and the set union and
# intersection operations. A set can be built from a list, a tuple or any
# other iterable. Duplicate elements are discarded, so Larry will be in
# the first set only once despite being listed twice.

names1 = { 'Larry', 'Johnny', 'Billy', 'Mary', 'Larry' }
names2 = { 'Max', 'Lena', 'Larry', 'Billy', 'Tina' }

# Membership check is done with the operators 'in' and 'not in'
print('Tony' in names1)        # False
print('Mary' in names1)        # True
print('Johnny' not in names1)  # False

# The basic set theoretical operations are handily available as methods.

union = names1.union(names2)
difference = names1.difference(names2)
intersection = names1.intersection(names2)

print(union)       # {'Lena', 'Johnny', 'Max', 'Billy', 'Larry', 'Tina', 'Mary'}
print(difference)  # {'Mary', 'Johnny'}
print(intersection)# {'Billy', 'Larry'}

# Sets do not allow indexing, but they do allow iteration. There are no
# guarantees about the order in which the elements are iterated, since the
# internal implementation of the set may organize the elements any which
# way it wants to make the operations faster.

for x in names2:
    print(f"{x} is in the second set.") 

# A dictionary is a mapping that associates values to keys. Python has a
# dictionary data type in the language itself. To create a dictionary
# object, simply list the pairs of keys and values between curly braces,
# each key separated from its value with a colon.

scores = { 'Mary': 14, 'Tony': 8, 'Billy': 20, 'Lena': 3}

# Since the same notation of curly braces is used for both sets and
# dictionaries, I wonder which one {} is? (It's a dictionary.)

print("The type of {} " f"is {type({})}.") # <class 'dict'>

# A dictionary can be "indexed" with its keys.

print(scores['Mary'])                # 14
scores['Lena'] = scores['Lena'] + 5  # Lena scores 5 more points
print(scores['Lena'])                # 8
scores['Anne'] = 12                  # add Anne in the dictionary
del scores['Tony']                   # and remove Tony

# Trying to index a dictionary with a nonexistent key would be a runtime
# error. To avoid this, use the method get that takes the key and the
# default value to use in case the key is nowhere in the dictionary:

print(scores.get('Alice', 0))        # 0

# Iterating through a dictionary goes through its keys, and iterating
# through the items of the dictionary goes through a sequence of tuples
# of (key, value) pairs. Again, there is no guarantee of iteration order.

print([x for x in scores])           # ['Billy', 'Lena', 'Anne', 'Mary']
print([x for x in scores.items()])
# [('Billy', 20), ('Lena', 8), ('Anne', 12), ('Mary', 14)]

# Each dictionary can contain only one entry for keys that are equal
# in the sense of operator ==, even if these objects are separate.
numdic = { 42: "Hello", 42.0: "World" } # Spyder gives a warning...
print(42 == 42.0)    # True (implicit cast)
print(42 is 42.0)    # False
print(numdic[42])    # World
print(numdic[42.0])  # World