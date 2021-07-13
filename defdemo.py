from itertools import accumulate
from math import log
import random

# When we are building complex programs, or just a library of
# useful code for other programmers to use as part of their
# programs, we write our code as functions. When you define a
# function of your own, you have to define the parameters it
# expects, followed by a code block telling what you do with
# those parameters.

# Factorial of n is the product of positive integers up to n.


def factorial(n):
    """Return the factorial of a positive integer.
    n -- The positive integer whose factorial is computed.
    """
    total = 1
    for i in range(2, n + 1):
        total *= i
    return total

# The return statement at the end of the function is used to
# tell what the function gives back to whoever calls it. Now
# we can invoke our function wherever we want, for whatever
# parameter values we wish, as if the Python language itself
# had been extended to have the factorial function:


print(factorial(5))
print(factorial(10))
print(factorial(100))

# docstring is automatically placed in object under name __doc__
print(factorial.__doc__)

# Note that def is a statement just like any other, so that the previous
# function calls would not have worked before the def was executed. In a
# sense, def is really an assignment that assigns the function name to a
# function object, as opposed to a string or an integer. The function names
# are variables, just like any other variables, and could be later be
# assigned to point some place else.

f = factorial    # copy a reference to the function object
factorial_30 = f(30)   # make an actual function call
print(factorial_30)    # 265252859812191058636308480000000

# All right, that out of the way, let's write some more functions that
# operate on lists. First, find the largest element in the list. We do
# this by iterating over the elements of the list


def maximum(seq):
    """ Return the largest element in sequence."""
    if not seq:
        raise ValueError("Empty list has no maximum")
    first = True
    for x in seq:
        if first or x > king:
            king = x
            first = False
    return king


print(maximum([5, 2, 8, 1, 0, 9, 6]))  # 9

# We could have just used Python's built-in max function...

print(max([5, 2, 8, 1, 0, 9, 6]))      # 9

# Next, a function that creates and returns another list whose
# each element equals the sum of the elements in the original
# list up to that index.


def accum(seq):
    result = []
    total = 0
    for x in seq:
        total += x
        result.append(total)
    return result


print(accum([1, 2, 3, 4, 5]))  # [1, 3, 6, 10, 15]

# Alternatively, the library itertools offers a bunch of functions that
# take an iterable and perform some kind of transformation on it, giving
# you another iterable as a result. For example, accumulate is one of the
# functions already defined there.

print(list(accumulate([1, 2, 3, 4, 5])))

# Select precisely the elements that are larger than their predecessor.


def select_upsteps(seq):
    prev = None
    result = []
    for x in seq:
        if prev is None or x > prev:
            result.append(x)
        prev = x
    return result


print(select_upsteps([4, 8, 3, 7, 9, 1, 2, 5, 6]))

# https://www.johndcook.com/blog/2011/10/19/leading-digits-of-factorials/
# Compute the factorials up to n! and count how many times each digit
# from 1 to 9 appears as the first digit of those factorials.


def leading_digit_list(n):
    prod = 1  # The current factorial
    digits = [0] * 10  # Create a list full of zeros
    for i in range(1, n + 1):
        lead = int(str(prod)[0])  # Extract highest order digit
        digits[lead] += 1
        prod = prod * i  # Next factorial, from the current one
    return digits


# https://en.wikipedia.org/wiki/Benford%27s_law


def output_leading_digits(n):
    digits = leading_digit_list(n)
    benford = [100 * (log(d+1, 10) - log(d, 10)) for d in range(1, 11)]
    print("\nDigit Observed  Benford")
    for i in range(1, 10):
        pct = 100 * digits[i] / n
        print(f"{i:5d}{pct:9.2f}{benford[i-1]:9.2f}")
    print("")


# Calling a function creates a new namespace separate from that of
# the caller's namespace. Let us demonstrate that with an example.

xx = 42  # Name xx defined outside the function.


def scope_demo():
    """Demonstrate the behaviour of local and global variables."""
    # print(f"xx is now {xx}") # error, Python compiles entire function
    xx = 99  # Name xx defined inside the function.
    print(f"xx is now {xx}")
    # Access a variable in the gglobal namespace.
    print(f"global xx is now {globals()['xx']}")

    def inner():
        return 4 + xx  # what is this bound to?
    return inner


print(f"Scope demo result is {scope_demo()}.")

# By the way, the above should lay to rest all the silly ideas of how
# "Python is not a compiled language".

# However, argument objects are passed to functions by reference, so
# the names in both caller and function namespace refer to the same
# data object. Therefore, if a function modifies that object, that
# modification persists to when execution returns to the caller.

items = [1, 2, 3, 4, 5]
print(f"Items is now: {items}")  # [1, 2, 3, 4, 5]


def demonstrate_parameter_passing(x):
    x[2] = 99


demonstrate_parameter_passing(items)
print(f"Items is now: {items}")  # [1, 2, 99, 4, 5]

# Next, let's write a function that allows us to roll a die a given
# number of times, and return the sum of these rolls. This function
# shows how to generate a random integer from the given range (once
# again, the upper bound is exclusive) and how to use default parameters.


def roll_dice(rolls, faces=6):
    """Roll a die given number of times and return the sum.
    rolls -- Number of dice to roll.
    faces -- Number of faces on a single die.
    """
    total = 0
    for x in range(rolls):
        total += random.randint(1, faces)
    return total


total1 = roll_dice(10, 12)
print(f"Rolling a 12-sided die 10 times gave a total of {total1}.")

# With a default parameter, we don't need to give its value.
total2 = roll_dice(6)
print(f"Rolling a 6-sided die 10 times gave a total of {total2}.")


# Fizzbuzz is a mental game where you try to list the numbers from
# start to end but so that if a number is divisible by 3, you say
# "fizz", and if a number is divisible by 5, you say "buzz", and
# if divisible by both 3 and 5, you say "fizzbuzz".

def fizzbuzz_translate(n):
    """Convert positive integer n to its fizzbuzz representation."""
    if n % 5 == 0 and n % 3 == 0:
        return 'fizzbuzz'
    elif n % 5 == 0:
        return 'buzz'
    elif n % 3 == 0:
        return 'fizz'
    else:
        return str(n)


print("Let's play a game of fizzbuzz from 1 to 100.")
print(", ".join([fizzbuzz_translate(y) for y in range(1, 101)]))
