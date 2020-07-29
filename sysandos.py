import sys
import os
import numpy as np

print("Let's find out some properties of the system running this.")

print(f"Computation platform is {sys.platform}.")
print(f"File system encoding is {sys.getfilesystemencoding()}.")
print("Command line arguments received were:")

for arg in enumerate(sys.argv):
    print(f"Argument {arg[0]} is {arg[1]!r}.")

print("\nFinding out some information about Python environment.")

print(f"Current Python version is {sys.hexversion}.")
print(f"Current implementation is {sys.implementation}.")
print(f"Recursion limit is {sys.getrecursionlimit()} levels.")
fi = sys.float_info
print(f"For float values, maximum exponent is {fi.max_exp}.")
print(f"For float values, mantissa contains {fi.mant_dig} bits.")

# Create two names referring to the same dictionary object.

a = {"hello": 42, "world": 99}
b = a

print("\nMoving on to some introspection of the object heap.")

# This is 3 instead of 2, because the getrefcount function has a local
# parameter variable pointing to the object received by the function.

print(f"The dictionary object ref count is {sys.getrefcount(a)}.")
print(f"The dictionary size is {sys.getsizeof(a)} bytes.")

# The slack space in lists, sets and dictionaries makes the
# modifications faster.

a['yeah'] = 12345

# The reported size does not change when adding new element.

print(f"After add, the dictionary size is still {sys.getsizeof(a)} bytes.")

print("\nObserve the growth of slack space at the end of a list.")
items = []
prev = sys.getsizeof(items)
print(f"Initial size of an entirely empty list is {prev} bytes.")
for i in range(1000):
    items.append(i)
    curr = sys.getsizeof(items)
    if curr != prev:
        print(f"At append #{i}, size increases by {curr - prev} bytes.")
        prev = curr

# Each list contains references to objects, but the objects themselves
# are not part of the list, but stored separately in the object heap.

big = list(range(1000000))
print(f"\nSize of the big list is {sys.getsizeof(big)} bytes.")
items.append(list)
print(f"After appending big list, new size is {sys.getsizeof(items)} bytes.")

# For homogeneous arrays of fixed size, the internal representation
# used by numpy is far more economical, at the price of flexibility.

# Integers from range 0 to 1000000, each stored in exactly four bytes.

bign = np.arange(0, 1000000, dtype='uint32')

# This is 4000096, because of the info stored about numpy array
# itself, such as shape and element type.

print(f"Size of the numpy array is {sys.getsizeof(bign)} bytes.")

# Since string objects are immutable, Python stores them in a special way
# that allows it to reuse string literals instead of creating redundant
# copies of the same string content.

a = "Hello, yellow"
b = a

# This is 4 instead of 2, because of Python's internal reference, and
# the argument reference during the function call sys.getrefcount(a).

print(f"\nThe string object has {sys.getrefcount(a)} references.")  # 4
c = "Hello, yellow"
print(f"The string object has by {sys.getrefcount(a)} references.")  # 5
d = c[:]
print(f"The string object has {sys.getrefcount(a)} references.")  # 6
e = c[:5] + c[5:]
print(f"The string object has {sys.getrefcount(a)} references.")  # 6

# The module os allows us to access the file system. Let's take a look
# around the current directory and find all the .txt files inside it.

print("\nMoving on to os functionality...")
print(f"There are {os.cpu_count()} CPU's in this system.")
print(f"Here is a proper 200-byte random number: {str(os.urandom(200))}.")
names = os.listdir(".")
print(f"The current directory is: {os.path.abspath('.')}")
print(f"The current directory contains {len(names)} filenames.")
for name in names:
    if os.path.isfile(name) and name.endswith(".txt"):
        st = os.stat(name)  # an os.statresult object
        print(f"Found text file {name} of {st.st_size} bytes.")
        print(f"This file was last modified at time {st.st_mtime}.")
