# A name refers only to its present value, but has no history of
# where that value came from.

a = 42
b = a + 1

print(f"a equals {a}, b equals {b}")  # 42, 43

# This is illustrated by Python not behaving like a spreadsheet.

a = 99

print(f"a equals {a}, b equals {b}")  # 99, 43

# The name is not the same thing as the object that it refers to.
# Whenever a name occurs in an expression, it means the object that
# the name currently points to.

a = "9999"
b = str(9999)

print("Results for two strings '9999'")

print(f"a == b: {a==b}\na is b: {a is b}")

# Actual memory addresses are dependent on the underlying system. The
# only thing guaranteed is that separate objects will have separate
# memory addresses.

print(f"id(a) equals {id(a)}, id(b) equals {id(b)}")

# Integers are a bit funny; small integers are stored in a special way.

a = 5
b = 5

print("Results for integer value 5:")

print(f"a == b: {a==b}\na is b: {a is b}")

# There is an upper limit to such caching, though.

a = 10**100
b = 10**100

print("Results for one googol:")

print(f"a == b: {a==b}\na is b: {a is b}")

# Whenever a variable appears in an expression, its value is substituted
# in its place. Therefore, id(a) gives you the memory address where the
# object that a currently points to is stored. There is no mechanism to
# acquire the memory address where the variable itself is stored in the
# memory.

a = "yeah"

# Notice how id(a) is different from what it was before.

print(f"id(a) equals {id(a)}, id(b) equals {id(b)}")

# When elements are placed in lists, sets and other collections, that
# collection contains object references, not the names.

items = [a, a, a]
print(items)  # ['yeah', 'yeah', 'yeah']

a = "nope"
print(items)  # ['yeah', 'yeah', 'yeah']

# If the same object is placed in multiple places of a list or other
# collection, all those places in collection refer to the same object.

first = [1, 2, 3]
# Three references to the same object.
second = [first, first, first]

print(second)  # [[1,2,3], [1,2,3], [1,2,3]]
first[0] = 99
print(second)  # [[99,2,3], [99,2,3], [99,2,3]]

# A list can contain itself as an element. Perfectly legal, although weird.

first.append(first)
print(first)  # Smart function realizes it has an infinite cycle.

# Splicing a list or other sequence creates a whole new object.

a = [1, 2, 3, 4, 5]
b = a[2:4]
a[2] = 99
print(a)  # [1, 2, 99, 4, 5]
print(b)  # [3, 4]

# However, dictionary views are live pointing to the underlying data.

d = {1: "yeah", 2: "nope", "foo": 42, 1.3: a}
dk = d.keys()
print(dk)  # a dict_keys object
del d[1]
print(dk)  # dict_keys with no more 1
