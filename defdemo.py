# When we are building complex programs, or just a library of useful code
# for other programmers to use as part of their programs, we write our code
# as functions. When you define a function, you tell what parameters it takes,
# followed by a code block telling what you do with those parameters.

# Factorial of n is the product of positive integers up to n.

def factorial(n):
    """Return the factorial of a positive integer.
    n -- The positive integer whose factorial is computed.
    """
    result = 1
    for x in range(2, n+1):
        result *= x
    return result

# The return statement at the end of the function is used to tell what the
# function gives back to whoever calls it. Now we can invoke our function
# wherever we want, for whatever parameter values we wish, as if the Python
# language itself had been extended to have the factorial function:

print(factorial(5))
print(factorial(10))
print(factorial(100))

# The docstring is automatically placed in object under name __doc__
print(factorial.__doc__)

# Note that def is a statement just like any other, so that the previous
# function calls would not have worked before the def was executed. In a
# sense, def is really an assignment that assigns the function name to a
# function object, as opposed to a string or an integer. The function names
# are variables, just like any other variables, and could be later be
# assigned to point some place else.

f = factorial    # copy a reference to the function object
result = f(30)   # make an actual function call
print(result)    # 265252859812191058636308480000000

# All right, that out of the way, let's write some more functions that
# operate on lists. First, find the largest element in the list. We do
# this by iterating over the elements of the list

def maximum(seq):
    """ Return the largest element in sequence.
    seq -- The sequence whose maximum we are looking for.
    """
    first = True
    for x in seq:
        if first or x > m:
            m = x
            first = False
    return m

print(maximum([5,2,8,1,0,9,6]))  # 9

# We could have just used Python's built-in max function...

print(max([5,2,8,1,0,9,6]))      # 9

# Next, a function that creates and returns another list whose each element
# equals the sum of the elements in the original list up to that index.

def accum(seq):
    """Given a sequence, return its accumulation sequence as a list.
    seq -- The sequence whose accumulation is computed.
    """
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

from itertools import accumulate
print(list(accumulate([1,2,3,4,5])))

# Select precisely the elements that are larger than their predecessor.

def select_upsteps(seq):
    prev = None
    result = []
    for x in seq:
        if prev == None or x > prev:
            result.append(x)
        prev = x
    return result

print(select_upsteps([4, 8, 3, 7, 9, 1, 2, 5, 6]))

# https://www.johndcook.com/blog/2011/10/19/leading-digits-of-factorials/
# Compute the factorials up to n! and count how many times each digit
# from 1 to 9 appears as the first digit of those factorials.

def leading_digit_list(n):
    prod = 1 # The current factorial
    digits = [0] * 10 # Create a list full of zeros
    for i in range(2, n+1):
        lead = ord(str(prod)[0]) - ord('0') # Compute first digit
        digits[lead] += 1
        prod = prod * i # The next factorial from the current one
    return digits

from math import log

# https://en.wikipedia.org/wiki/Benford%27s_law

def output_leading_digits(n):
    digits = leading_digit_list(n)    
    benford = [100 * (log(d+1, 10) - log(d, 10)) for d in range(1, 11)]
    print("\nDigit Observed  Benford")
    for i in range(1, 10):
        pct = 100 * digits[i] / n
        print(f"{i:5d}{pct:9.2f}{benford[i-1]:9.2f}")
    print("")

output_leading_digits(2000)

# Calling a function creates a new namespace separate from that of the
# caller's namespace. Let us demonstrate that with an example.

xx = 42
def scope_demo():
    """Demonstrate the behaviour of local and global variables.
    """
    # print(f"xx is now {xx}") # error, Python compiles entire function
    xx = 99
    print(f"xx is now {xx}") 
    # access a variable in the gglobal namespace
    print(f"global xx is now {globals()['xx']}")
    def inner():
        return 4 + xx # what is this bound to?
    return inner

print(f"Scope demo result is {scope_demo()}.")

# By the way, the above should lay to rest all the silly ideas of how
# "Python is not a compiled language".

# However, argument objects are passed to functions by reference, so
# the names in both caller and function namespace refer to the same
# data object. Therefore, if a function modifies that object, that
# modification persists to when execution returns to the caller.

items = [1,2,3,4,5]
print(f"Items is now: {items}")  # [1, 2, 3, 4, 5]
def demonstrate_parameter_passing(x):
    x[2] = 99
demonstrate_parameter_passing(items)
print(f"Items is now: {items}")  # [1, 2, 99, 4, 5]

# Next, let's write a function that allows us to roll a die a given
# number of times, and return the sum of these rolls. This function
# shows how to generate a random integer from the given range (once
# again, the upper bound is exclusive) and how to use default parameters.

import random

def roll_dice(rolls, faces = 6):
    """Roll a die given number of times and return the sum.
    rolls -- Number of dice to roll.
    faces -- Number of faces on a single die.    
    """
    total = 0
    for x in range(rolls):
        total += random.randrange(1, faces+1)
    return total

print("Rolling a 12-sided die 10 times gave a total of %d" % roll_dice(10, 12))
# With a default parameter, we don't need to give its value
print("Rolling a 6-sided die 10 times gave a total of %d" % roll_dice(10))

# Note that default parameter values are computed only once at the
# function declaration.

val = 42
def foo(x = val):
    return x
val = 99
def bar(x = val):
    return x
print("foo() equals %d, bar() equals %d" % ( foo(), bar() )) # 42 99

# Fizzbuzz is a game where you try to list the numbers from start to end
# but so that if a number is divisible by 3, you say "fizz", and if a
# number is divisible by 5, you say "buzz", and if by both 3 and 5, you
# say "fizzbuzz".

def fizzbuzz_translate(n):
    """Convert positive integer n to its fizzbuzz representation.
    n -- The positive integer to convert.
    """
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
    
# Next, let us write a function that evaluates a polynomial, given in
# the list of coefficients, at the given point x.

def evaluate_poly(coeff, x):
    """Evaluate the polynomial, given as coefficient list, at point x.
    coeff -- Sequence of coefficients that define the polynomial.
    x -- The point in which to evaluate the polynomial.
    """
    result = 0.0
    power = 1.0 # Current power of x
    for c in coeff:
        result += c * power # Add current term to result
        power *= x # Next power from current with one multiplication
    return result

# Evaluate 5x^3-10x^2+7x-6 at x = 3. Note how coefficients are listed
# in the increasing order of the exponent of the term.

print(evaluate_poly([-6, 7, -10, 5], 3))  # 60.0

# A function that returns either True or False is called a predicate. It
# checks whether the given parameter values have some particular property.
# For example, the simple predicate that checks if its parameter is odd:

def is_odd(n):
    """A simple function to check if an integer is odd.
    n -- The integer whose oddness we want to determine.
    """
    if n % 2 == 0:
        return False
    else:
        return True

# Predicates can be themselves be passed as parameters to higher-level
# functions that take functions are parameters. Such predicates can then
# be used in, for example, conditional list comprehensions. Here, we
# list the squares of odd numbers from 0 to 100.

oddsquares = [x*x for x in range(100) if is_odd(x)]
print(oddsquares)
                
# Next, we examine how to write a function that can be called with any
# number of arguments. If the function's last parameter starts with an
# asterisk, that parameter is a list that collects all the parameters
# given to it after the possible other, normal arguments.

def gimmeanyargs(*args):
    # inside the function, args is an ordinary list.
    print("All right, you gave me the following arguments:")
    for a in args:
        print(a)

gimmeanyargs(42, "Hello world", -8.4, evaluate_poly)

# If we even wanted to allow any keyword arguments, one more parameter
# after *args starting with ** will collect all those.

def gimmeanything(*args, **kwargs):
    gimmeanyargs(*args)  # might as well use the function that we have
    print("And then you gave me these keyword arguments:")
    # inside the function, kwargs is an ordinary dictionary.
    for kwa in kwargs.items():
        print(kwa)

gimmeanything(55, "foobar", name='Billy', age=24)