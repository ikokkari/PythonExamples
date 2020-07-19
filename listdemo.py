# List is the basic data structure of Python. It consists of a
# sequence of elements listed between square brackets, separated
# by commas. Here we create a simple five-element list.

a = [1, 2, 3, 4, 5]

# The function len gives the length of the list that you apply it
# to. In fact, not just a list, but any sequence type of Python,
# of which a list is merely one. Strings are also sequences, and
# we will see more sequence types later.

print(len(a))  # 5
s = "Hello there, reader"
print(len(s))  # 19

# An individual element in a list can be accessed by indexing.
# The list indices start from 0, so a[0] is the first element of
# the list a, a[1] is the second element, and so on. A negative
# index is computed from the end of the list.

print(a[0])   # 1
print(a[3])   # 4
print(a[-1])  # 5

# To check whether the list contains a given element, use operator in.
# It only checks if the element is somewhere, but doesn't give its index.
# The operator result is a Python's built-in truth value True or False.

print(3 in a)   # True
print(13 in a)  # False

# Python lists have handy methods to manipulate that list. Some of the
# more important and useful ones are demonstrated below.

a.append(6)  # append a single element to the end of the list
more = [7, 8, 9]
a.extend(more)  # append each element of another sequence
a.remove(2)  # removes the element 2 (note: NOT at the index 2)
del a[2]     # removes the element that is at the index 2

print(a)     # [1, 3, 5, 6, 7, 8, 9]

a.reverse()  # rearranges the contents of the list
print(a)     # [9, 8, 7, 6, 5, 3, 1]

a.sort()     # rearranges the contents of the list
print(a)     # [1, 3, 5, 6, 7, 8, 9]

# Whereas indexing gives you an individual element, slicing gives you a
# part of the list between the start and the end index, copied into a
# separate list. The start index is inclusive, whereas the end index is
# exclusive.

b = a[2:4]   # from index 2 to index 3
print(b)     # [5, 6]
c = a[3:]    # missing end index means "up to the end"
print(c)     # [6, 7, 8, 9]
c = a[:3]    # missing start index means "from the start"
print(c)     # [1, 3, 5]

# So far, all elements in the above lists were integers. This doesn't need
# to be so, since Python lists are heterogeneous, so each element can be
# any legal Python object... even another list. Or, like, whatever.

d = ["Hello", 17, -84.123, type(42)]
print(d)     # ['Hello', 17, -84.123, <class 'int'>]
d.append([1, 2, 3, 4, 5])  # make the last element be an entire list
print(d)     # ['Hello', 17, -84.123, <class 'int'>, [1, 2, 3, 4, 5]]
print(d[3])  # [1, 2, 3, 4, 5]

# The way Python associates names to values is that values are stored
# somewhere in the memory, and the names in a given namespace point to
# these values. When you assign a name to another name, both names point
# to the same data object, and changing this data from one name also
# changes it for the other name.

a = [1, 2, 3]
b = a       # now a is b, that is, id(a) == id(b)
del(a[1])   # remove element 2 from the list object
print(b)    # [1, 3]

# However, when you use a reference inside a list, its value is stored
# at that point, so changing that reference later has no effect on the
# contents of that list.

a = 2
b = [1, a, 3]
print(b)    # [1, 2, 3]
a = 42
print(b)    # [1, 2, 3]

# A tricksy question: can you tell what happens here?

c = [1, 2]
c.append(c)  # append list c to itself, creating an infinite loop
print(c)     # [1, 2, [...]]

# If you want to create a separate copy of a list, instead of
# having both names point to the same list, the canonical Python
# trick is to use slicing without either start or end.

a = [1, 2, 3]
b = a[:]    # slicing always creates a separate copy
del(a[1])   # that modifying the original does not affect
print(a)    # [1, 3]
print(b)    # [1, 2, 3]

# The canonical trick to create a reversed copy of the list.
a = [1, 2, 3]
print(a[::-1])  # [3, 2, 1]
print(a)        # [1, 2, 3]

# I wonder what methods there are already defined in lists?
# The Python function dir returns a list of names defined
# inside the given namespace.

print("Names defined in global namespace are:")
print(dir())
print("Names defined inside the empty list object [] are:")
print(dir([]))  # names inside list object
print("Names defined inside the dir function are:")
print(dir(dir))
# Python functions are also data objects. Any object that has a the name
# __call__ defined inside it is a function that can be called in Python.
print("Names defined in the global namespace are:")
print(dir.__call__())
