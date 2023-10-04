from math import log
from random import Random

# When we are building complex programs, or just a library of
# useful code for other programmers to use as part of their
# programs, we write our code as functions. When you define a
# function of your own, you have to define the parameters it
# expects, followed by a code block telling what you do with
# those parameters.

# When using pseudorandom numbers, hardcode the seed to make the
# results of your program reproducible.

rng = Random(12345)

# Factorial of n is the product of positive integers up to n.


def factorial(n):
    """Return the factorial of a positive integer.
    n -- The positive integer whose factorial is computed.
    """
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

# The return statement at the end of the function is used to
# tell what the function gives back to whoever calls it. Now
# we can invoke our function wherever we want, for whatever
# parameter values we wish, as if the Python language itself
# had been extended to have the factorial function:


# All right, that out of the way, let's write some more functions that
# operate on lists. First, find the largest element in the list, same
# as the Python built-in function max.


def maximum(items):
    """ Return the largest item in the given items."""
    if not items:  # Testing whether the sequence is empty
        # This is how you make a function crash for invalid arguments.
        raise ValueError("Empty list has no maximum")
    king = None
    for e in items:
        if king is None or e > king:
            king = e
    return king


# Next, a function that creates and returns another list where
# each element equals the sum of the elements in the original
# list up to that index.

def accumulate(items):
    result, total = [], 0
    for e in items:
        total += e
        result.append(total)
    return result


# Select precisely the elements that are larger than their predecessor.

def select_upsteps(items):
    prev, result = None, []
    for e in items:
        if prev is None or e > prev:
            result.append(e)
        # The current element becomes previous element for the next round.
        prev = e
    return result


# https://www.johndcook.com/blog/2011/10/19/leading-digits-of-factorials/
# Compute the factorials up to n! and count how many times each digit
# from 1 to 9 appears as the first digit of those factorials.

def leading_digit_list(n):
    current_factorial = 1  # The current factorial
    digits = [0] * 10  # Create a list full of zeros
    for i in range(1, n+1):
        lead = int(str(current_factorial)[0])  # Extract highest order digit
        digits[lead] += 1
        current_factorial *= i  # Next factorial, computed from the current one
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


# Let's roll some random dice like in the game of Dungeons & Dragons.

def roll_dice(rolls, faces=6):
    """Roll a die given number of times and return the sum.
    rolls -- Number of dice to roll.
    faces -- Number of faces on a single die.
    """
    total = 0
    for _ in range(rolls):  # Anonymous variable _ whose value is not needed in body
        total += rng.randint(1, faces)
    return total


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


def fizzbuzz(start=1, end=101):
    """Play the game of fizzbuzz from start to end, exclusive."""
    result = []
    for n in range(start, end):
        result.append(fizzbuzz_translate(n))
    result = ", ".join(result)
    return result


def demo_all():
    print(f"Factorial of 5 equals {factorial(5)}.")
    print(f"Factorial of 20 equals {factorial(20)}.")
    print(f"Factorial of 100 equals {factorial(100)}.")

    # docstring is automatically placed in object under name __doc__
    print("Here is the documentation string for the factorial function:")
    print(factorial.__doc__)

    items = [5, 2, -42, 8, 1, 1, 0, 9, 6]
    print(f"Maximum of {items} is {maximum(items)}.")  # 9

    print(f"These items accumulate to {accumulate(items)}.")

    print(f"Their upsteps are {select_upsteps(items)}.")

    print("\nIn factorials from 0 to 1000, the leading digits are as follows:")
    for (i, c) in enumerate(leading_digit_list(1000)):
        print(f"The digit {i} is the leading digit {c} times.")

    print("\nHere is the table of percentages versus Benford's law.")
    output_leading_digits(1000)

    total1 = roll_dice(10, 12)
    print(f"Rolling a 12-sided die 10 times gave us the total of {total1}.")

    # With a default parameter, we don't need to give its value.
    total2 = roll_dice(6)
    print(f"Rolling a 6-sided die 10 times gave us the total of {total2}.")

    print("\nTo finish up, let's play Fizzbuzz from 1 to 100.")
    print(fizzbuzz(1, 100))


# Code to be executed when the script is run as a program, instead of being
# imported into another program.

if __name__ == "__main__":
    demo_all()
