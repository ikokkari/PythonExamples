# This example demonstrates a bunch of Python features for functional
# programming. This means that functions are treated as data that can
# be stored to variables, passed to other functions, returned from
# functions as results, created on the fly etc.

# Defining anonymous functions with lambda.
is_positive = lambda x: x > 0
print(is_positive(42))
print(is_positive(-99))
square = lambda x: x*x

# Functional programming basic commands map, filter and reduce. Note that
# these both return iterator objects instead of performing the computation
# right away, so we now force the computation to take place with list().
print("The positive elements are: ", end = '')
print(list(filter(is_positive, [-7, 8, 42, -1, 0])))
print("The squares of first five positive integers are: ", end = '')
print(list(map(square, [1, 2, 3, 4, 5])))

# Reduce is a handy operation to repeatedly combine first two elements
# of the given sequence into one, until only one element remains.

from operator import mul
from functools import reduce, partial
print(reduce(mul, [1,2,3,4,5], 1)) # 1 * 2 * 3 * 4 * 5

def falling_power(n, k):
    return reduce(mul, reversed(range(n-k+1,n+1)))

def rising_power(n, k):
    return reduce(mul, range(n, n+k))

print(f"Falling power of 10 to 3 equals {falling_power(10, 3)}.")
print(f"Ordinary power of 10 to 3 equals {10**3}.")
print(f"Rising power of 10 to 3 equals {rising_power(10, 3)}.")

# Determine whether the sequence x, f(x), f(f(f(x))), ... becomes
# periodic after some point. A computer science classic without
# needing more than O(1) extra memory.
def is_eventually_periodic(f, x, giveup = 1000):
    tortoise, hare = x, f(x)    
    while tortoise != hare and giveup > 0:
        tortoise = f(tortoise)
        hare = f(f(hare))
        giveup -= 1
    return tortoise == hare

# Next, let's examine how functions can be given to other functions as
# parameters, and returned as results to the caller. To demonstrate this,
# let's write a function negate that can be given any predicate function,
# and it creates and returns a function that behaves as the negation of
# its parameter.

def negate(f):
    # Nothing says that we can't define a function inside a function.
    # Since we don't know what parameters f takes, we write our function
    # to accept any arguments and keyword arguments.
    def result(*args, **kwargs):
        return not f(*args, **kwargs)
    return result # return the function that we just defined

# Let's try this out by negating the following simple function.

def is_odd(x):
    return x % 2 != 0

is_even = negate(is_odd)
print(is_even)     # <function result at ....>
print(f"Is 2 even? {is_even(2)}")  # True
print(f"Is 3 even? {is_even(3)}")  # False

# Partial evaluation or "currying" means fixing some of the parameter
# values of a function to create a function that takes fewer parameters
# but is otherwise the same.

def foo(a, b, c):
    return a + (b * c)

# Create a version of foo with parameter b fixed to -1.
foob = partial(foo, b = -1)
print(f"After partial application, foob(2, 5) equals {foob(a = 2, c = 5)}.")

# Sometimes functions can take a long time to calculate, but we know that
# they will always return the same result for the same parameters. The
# function memoize takes an arbitrary function as a parameter, and creates
# and returns a new function that gives the same results as the original,
# but remembers the results that it has already computed and simply looks
# up those results that have previously been calculated.

def memoize(f):
    results = {}   # empty dictionary, as nothing has been computed yet
    def lookup_f(*args):
        res = results.get(args, None)        
        if res == None:
            res = f(*args)      # calculate the result
            results[args] = res # and store it in dictionary
        return res
    # Alias the local variable so that it can be seen from outside.
    lookup_f.results = results
    return lookup_f

# The famous Fibonacci series. Trust me that this stupid implementation
# would take nearly forever if called for n in largish double digits.

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# print(fib(200))    # way longer than the lifetime of universe
oldfib = fib         # keep a reference to the original slow function
fib = memoize(fib)   # however, memoization makes it all smooth
print(fib(200))      # 453973694165307953197296969697410619233826

print(f"fib is oldfib = {fib is oldfib}") # False
print(f"The memoized fib contains {len(fib.results)} cached results.")

# Hofstadter's recursive Q-function, memoized for efficiency.
# http://paulbourke.net/fractals/qseries/

def hof_q(n):
    if n < 3: return 1
    return hof_q(n - hof_q(n-1)) + hof_q(n - hof_q(n-2))
hof_q = memoize(hof_q)

print(f"HofQ(100) = {hof_q(100)}.")

# We can also perform the memoization explicitly. Since the function
# arguments are assumed to be nonnegative integers, the computed results
# can be stored in a list. Otherwise, some kind of dictionary would have
# to be used.

Q = [ 0, 1, 1 ]
def hof_qt(n):
    if n >= len(Q):
        for i in range(len(Q), n + 1):
            Q.append(Q[i - Q[i-1]] + Q[i - Q[i-2]])
    return Q[n]

print(f"HofQt(1000000) = {hof_qt(1000000)}.")
print(f"HofQt table contains {len(Q)} cached entries.")

# Wouldn't it be "groovy" to memoize the memoize function itself, so that
# if some function has already been memoized, the same function won't be
# memoized again but its previously memoized version is returned?

memoize = memoize(memoize)

def divisible_by_3(x):
    return x % 3 == 0

f1 = memoize(divisible_by_3)
f2 = memoize(divisible_by_3)   # already did that one
print(f"f1 is f2 = {f1 is f2}.") # True

# We can use the memoization technique to speed up checking whether the
# so-called Collatz sequence starting from the given number eventually
# reaches 1. The function collatz(n) tells how many steps this takes.

@memoize
def collatz(n):
    if n == 1:
        return 0
    elif n % 2 == 0:
        return 1 + collatz(n // 2)
    else:
        return 1 + collatz(3 * n + 1)

lc = max(((collatz(i), i) for i in range (1, 10**6)))
print(f"Collatz sequence from {lc[1]} contains {lc[0]} steps.")
print(f"Stored {len(collatz.results)} results. Some of them are:")
from random import randint
for i in range(10):
    v = randint(1, 10**6 - 1)
    print(f"From {v}, sequence contains {collatz.results[(v,)]} steps.")

# Sometimes we use some simple function only in one place. With lambdas,
# such a function can be defined anonymously on the spot, provided that
# the function can written as a single expression. For example, use the
# previous negate to a lambda predicate that checks if its parameter is
# negative or zero, to give a function is_positive.

is_positive = negate(lambda x: x <= 0)
print(is_positive(2))  # True
print(is_positive(-2)) # False

# The famous Thue-Morse sequence for "fairly taking turns".

__tm_call_count = 0

@memoize
def thue_morse(n, sign):
    global __tm_call_count
    __tm_call_count += 1
    if n == 1:
        return '0' if sign == 0 else '1'
    else:      
        return thue_morse(n-1, sign) + thue_morse(n-1, 1-sign)

print("Thue-Morse sequences from 2 to 10 are:")
for i in range(2, 11):
    print(f"{i}: {thue_morse(i, 0)}")
    
# Memoization of recursions that have repeating subproblems is awesome.
print(f"Computing those required {__tm_call_count} recursive calls.")

# The next function can be given any number of functions as parameters,
# and it creates and returns a function whose value is the maximum of
# the results of any of these functions.

def max_func(*args):
    funcs = args
    def result(*args):
        return max((f(*args) for f in funcs))
    return result

# Try that one out with some polynomials that we create as a lambda
# to be used as throwaway arguments of max_func.

f = max_func(lambda x: -(x*x) + 3*x - 7,   # -x^2+3x-7
             lambda x: 4*x*x - 10*x + 10,  # 4x^2-10x+10
             lambda x: 5*x*x*x - 20)       # 5x^3-20

print("Maximums given by the three functions for -5, ..., 5 are:")
print([f(x) for x in range(-5, 5)])

# Here is another function decorator that maintains a count attribute
# to keep track of how many times the function has been called. Since
# nested functions cannot reassign a variable in the outer function,
# but can change the contents of the object that the variable refers
# to, we define the variable count to be a one-element mutable list.
# Even though we can't reassign this variable, we can reassign the
# value of its one element, following the letter of the law if not its
# spirit.

def counter(f):
    count = [0]
    def cf(*args, **kwargs):
        nonlocal count
        count[0] += 1
        return f(*args, **kwargs)
    def get_count():
        return count[0]
    def reset_count():
        count[0] = 0
    cf.get_count = get_count
    cf.reset_count = reset_count
    return cf

# Demonstrate the previous decorator by counting how many times the
# sorting algorithm computes the given key...

def kf(x):
    return x
kf = counter(kf)

sorted(range(-100, 100), key = kf, reverse = True)
print(f"The key was computed {kf.get_count()} times.")

# The key is computed only once per element, cached and then used in
# element comparisons. Let's see if this changes for a wider range...

kf.reset_count()
sorted(range(-100000, 100000), key = kf, reverse = True)
print(f"The key was computed {kf.get_count()} times.")

# Another sometimes handy feature of Python is the ability to compile
# and execute new code dynamically on the fly, in any desired context.
# However, be careful using eval and exec to strings that originate
# from outside your program, as this opens a doorway for a malicious
# attacker to execute hostile code in your computer.

myglobals = { "x":10, "y":20 }
code = "print (x+y)"   # a super simple example program to run
exec(code, myglobals)  # 30
def myfun():
    x = 40
    y = 50
    # The built-in functions globals and locals return dictionaries
    # of the current global and local variables, respectively.
    return locals()
eval(code, myfun())    # 90