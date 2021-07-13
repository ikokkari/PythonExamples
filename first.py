# Python comes with a bunch of good libraries that define all kinds of
# functions so that we don't need to write them ourselves. For example,
# let us import the math library and showcase some of its functions.

import math

# Exact integer fractions are not in the Python core language itself,
# but the handy library fractions defines them as a type that you can
# use as you would any other type.

from fractions import Fraction

# A Python program consists of a series of statements that, when
# that program is run, are executed in the order that they are
# listed. The simplest statement is an assignment that associates
# a value to a name. This statement creates a name and initializes
# it to the value of the right-hand side expression that can be
# a mere constant or a more complicated expression.

a = 42
b = a * 2 - 3

# Python can also represent and handle text strings. They are given
# between either single or double quotes. You can take your pick
# which type of quote you prefer. Using one kind of quote allows
# the use of other type inside the string.

c = 'Hello world'
d = "Another 'string' given between double quotes"

# The print function outputs the value of its parameter on the console.

print(a)  # outputs '42'
print(b)  # outputs '81'
print(c)  # outputs 'Hello world'
print(d)  # outputs 'Another 'string' given between double quotes'

# Note that every variable only remembers its value, not where the value
# originally came from. So even though b was defined with the assignment
# b = a * 2 - 3, it doesn't remember this, and thus changing the value
# of a later has no effect on the value of b.

a = 17
print(b)   # still 81, has not magically become 31

# Conversely, the input function prompts the user to type in some input.
# The input is always read as a string, even if the user enters a number.
# But conversions between different types are easy to do in Python.

print("I shall now ask you a few questions.")
name = input("What is your name? ")
age = int(input("How old are you? "))

# When you do more complicated output that consists of pieces of data,
# it is sometimes handy to format the answer at once. When formatting
# a string, curly braces {} are used as placeholders whose values are
# given as parameters to format.

answer = f"Your name is {name} and you are {age} years old."
print(answer)

# Once you don't need some name and value any more, you can use the
# operator del to remove that name from the namespace.

del d

# Trying to use the value of d now would crash the program. However,
# it is perfectly fine to create the name again.

d = 'This is yet another string in our first program.'
print(d)


# After importing math in the beginning, the high school math
# functions are defined, and we can use them. However, in the
# namespace they are under the separate namespace math, so to
# access these names, we need to use the prefix 'math' to get
# to that namespace.

x = 1.2345678
print(math.sqrt(x))
print(math.cos(x))
print(math.exp(x))
print(math.pow(x, math.pi))

# Python even supports complex numbers right out of the box, and its
# arithmetic operations just do the complex number arithmetic.

z1 = complex(4, -2)  # 4 - 2j
z2 = complex(-3, 1)  # -3 + j
z3 = z1 * z2         # -10+10j
print(f"The real part is {z3.real} and the imaginary part is {z3.imag}.")

# However, Python uses floating point arithmetic for complex numbers.

f1 = Fraction(-2, 7)  # a fraction from two integers
f2 = Fraction('5/9')  # a fraction from a string
f3 = f1 * f2
print(f"The product of {f1} and {f2} equals {f3}.")  # -10/63

# Joe and Moe are peeling potatoes. Working by himself, Joe could peel
# the entire pile in three hours, whereas Moe could peel the same pile
# in five hours. How long will it take for these two men to peel the
# potatoes if they work together? (No, the answer is *not* four hours,
# the simple average of three and five.)

joe_speed = Fraction(1, 3)
moe_speed = Fraction(1, 5)
together = joe_speed + moe_speed
time = 1 / together
print(f"Together, Joe and Moe finish in {time} hours.")

# Remember that strings and integers are not the same thing, even as
# they can be trivially converted to one another.

a = 22 + 22
print(a)         # 44
b = '22' + '22'  # string addition works as plain concatenation
print(b)         # '2222', not '44'
c = int('22') + int('22')
print(c)         # 44

# The built-in function type tells you the type of something.

print(type(a))      # <class 'int'>
print(type(b))      # <class 'str'>
print(type(False))  # <class 'bool'>

# Assignment is actually smart enough so that multiple assignments can be
# performed in a single step. Since all right hand side expressions are
# evaluated before the assignment, this does the right thing even when
# we are doing the naive swap.

x, y = 17, 42
print(f"Before swap, x equals {x}, and y equals {y}.")  # 17 42
x, y = y, x
print(f"After swap, x equals {x}, and y equals {y}.")  # 42 17

# In basic arithmetic, division is handled with a couple of different
# operators depending on what kind of division you want. Couple of
# things about them can first be surprising.

print(11 / 4)    # 2.75, the usual everyday division
print(11 / -4)   # -2.75
print(11 // 4)   # 2, integer division with duplicated slash
print(11 // -4)  # -3, not -2, as integer division uses floor
print(11 % 4)    # 3, % is the integer division remainder operator
print(-11 % 4)   # 1
print(11 % -4)   # -1

# Last, in addition to all the values that we have, there is a built-in
# special value None that means that a name has no value. (Chew on
# that for a moment.) A name being defined but not having a value is a
# different thing than that name not existing at all.

idontknow = None
print(idontknow)
del idontknow
print(idontknow)   # crash with NameError
