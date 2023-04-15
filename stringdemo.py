import unicodedata as uu  # properties of Unicode characters
from string import Template
from string import capwords

# Ordinary string literals in Python. Escape sequences can be used
# to embed various special characters inside string literals.

s1 = "Hello there,\tworld!"
s2 = ""

# Python 3 strings are sequences of arbitrary Unicode characters.

for code in range(100, 10100, 500):
    cc = chr(code)
    s2 += cc
    name, cat = uu.name(cc), uu.category(cc)
    print(f"Character {cc} at code point {code} is {name}, in category {cat}.")

# Old time byte strings can contain only ASCII characters 0-127.

sb = b'Only ASCII characters allowed here!\x60'

print(f"String s1 is <{s1}>.")
print(f"String s2 is <{s2}>.")
print(f"String sb is {sb}.")

a = 42
b = 123.45678

# Python formatted string. There is a whole minilanguage available.

s3 = f"a is now {a} (which is {a:x} in hex), and b is now {b:.3f} \
which is {b:e} in scientific notation."
print(s3)   # note the correct rounding of floating point number b

# The string does not remember where its characters came from.

a = 99
print(s3)   # still says that a is 42

s4 = f"a is now {a}, b is now {b:7.3}."
print(s4)   # Here a is 99

# Format placeholders are evaluated once. They are compiled to Python
# bytecode before executing the program, so syntax errors are revealed
# before the script starts running. Uncomment to see this happen.

# print(f"a is now {a:!4&^#}")

a = 42
print(s4)  # a is still 99 inside the string

# And yet another way to compose strings from smaller pieces. Very
# few examples of people actually using this scheme have been found.
# The mystery deepens.

tt = Template("$who likes $food.")

# Python's flexibility to allow arbitrary keyword arguments in functions
# really displays its power and usefulness here.
print(tt.substitute(who="Bob",  food="sushi"))
print(tt.substitute(who="Jack", food="steak"))

# The old-timey string interpolation operator % behaves like in C.

s2 = "a is now %3d, b is now %.4f." % (a, b)
print(s2)

# Strings are iterable, and can be processed as iterables.

it = iter(s1)
print(next(it))  # H
print(next(it))  # e
for x in it:
    print(ord(x), end=' ')  # whole bunch of Unicode codepoints
print()  # line break

# Raw strings can be handy with regexes and other systems that need
# special characters differently from Python.

s5 = r'Bunch of % \ special characters as they are.'
print(s5)

# Unicode has lots of crazy stuff.
# https://mortoray.com/2013/11/27/the-string-type-is-broken/

s6 = u'noe\u0308l'
print(s6)
print("".join(reversed(s6)))  # reversing unicode is tricksy
print(s6[::-1])  # how to reverse a Python string

# Taken from "WTF Python". What is going on here?
value = 11
valuе = 32    # Linters in PyCharm and such reveal the subterfuge
print(value)  # 11
print(valuе)  # 32

# Some handy methods on strings.

print(s1.title())
print(s1.upper())
print(s1.lower())
print(s1.capitalize())

# Add whitespace to left, right or both sides to reach given length.

print('1234'.center(10))
print('1234'.ljust(10))
print('1234'.rjust(10))

# In principle all string operations could be done using methods
# that we already have, but it's pointless to reinvent the wheel
# unless you feel like exercising.

s = "let us capitalize every word of this sentence."
print(capwords(s))
# This one would not be too difficult to do on our own.
print(" ".join([x.capitalize() for x in s.split()]))
