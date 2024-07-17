from random import Random


# The oldest algorithm in recorded history, Euclid's GCD algorithm
# finds the greatest common divisor of two non-negative integers.
# (This function is already in the math module as math.gcd.)

def euclid_gcd(a, b, verbose=False):
    while b > 0:
        a, b = b, a % b
        if verbose:
            print(f"a={a}, b={b}")
    return a


# This algorithm could even be extended to find two numbers x and y
# that satisfy ax + by = gcd(a, b), which will be useful in various
# mathematical algorithms.

# Generate the Collatz 3n+1 series from the given starting value.
# https://en.wikipedia.org/wiki/Collatz_conjecture

def collatz(start):
    n, result = start, [start]
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        result.append(n)
    return result


# A fun little "gem" from one of the books of Ross Honsberger.
# Given a list of four natural numbers, repeatedly replace each
# number with the absolute difference between that number and
# its cyclic predecessor. This will eventually converge to all
# four numbers being equal to some final number n. The function
# returns a tuple (n, c) where c is the count of how many steps
# were needed to reach the goal.

def iterate_diff(items, verbose=False):
    count = 0
    while not all(e == items[0] for e in items):
        new, prev = [], items[-1]
        for e in items:
            new.append(abs(e-prev))
            prev = e
        items = new
        if verbose:
            print(items, end=" -> ")
        count += 1
    print("\n" if verbose else "", end="")
    return items[0], count


# What is the relationship between the final value and the four
# original values? What happens if items contains some other
# number of elements than only four? Would the convergence of
# this system still be guaranteed? Curious students might want
# to investigate this phenomenon.


# Another algorithm from the ancient world, Heron's square root
# method to numerically iterate the guess for the square root of
# the positive real number x. (This algorithm generalizes to any
# roots, and in fact turns out to be special case of Newton's
# numerical iteration with the function whose root we want to
# solve hardcoded to square root.)

def heron_root(x):
    if x < 0:
        raise ValueError("Square roots of negative numbers are not allowed")
    guess, prev = x / 2, 0
    # Fingers crossed, this will converge in float precision.
    while guess != prev:
        prev = guess
        guess = (guess + x / guess) / 2
    return guess


# Converting Roman numerals and positional integers back and forth
# makes for interesting and educational example of loops, lists
# and dictionaries.

symbols_encode = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
    (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]


def roman_encode(n):
    if n < 1:
        raise ValueError("Can't convert {n}; Romans did not know zero or negative numbers")
    result = ''
    for (v, s) in symbols_encode:
        while v <= n:  # same symbol can be used several times
            result += s
            n -= v
    return result


# Dictionaries map symbols into the values that they encode.

symbols_decode = {
    'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1
}


def roman_decode(s):
    result, prev = 0, 0
    for c in reversed(s.upper()):  # Loop right to left
        v = symbols_decode[c]
        result += (v if prev <= v else -v)
        prev = v
    return result


# Whenever two functions are each other's inverses, it is easy to
# test them by looping through some large number of possible inputs
# and verify that both functions invert the result produced by
# the other. This does not guarantee these functions to be correct,
# though, just that if they are wrong, they both are wrong in the
# same particular way.

def test_roman():
    for n in range(1, 5000):
        if n != roman_decode(roman_encode(n)):
            return False
    return True


# Whenever a problem is stated in terms of integers, you should aim
# to solve it with integer arithmetic, and use floating point values
# only if absolutely necessary. Even in that case, never ever compare
# two computed floating point values for equality! Since floating point
# values are approximations, it just never makes sense to compare them
# with the operator ==. The most commonly seen Python constructs that
# tend to produce floating point numbers would be ordinary division /
# and sqrt, pow and basically any functions in the math module.

# As an example of how to do things with integers, here is the integer
# root function that finds the largest a so that a**k <= n. Note how
# the logic of this function does not depend on the fact that the
# function is specifically the integer root, but can be adjusted to
# produce the solution of any other monotonically ascending function.

def integer_root(n, k=2):
    # Find a and b so that a <= x <= b for the real answer x.
    a, b = 0, 1
    # Find some big enough b. More sophisticated schemes also exist
    # to quickly find some b > x that does not overshoot too much.
    # As long as b > x, the rest of the algorithm works, but it is
    # always better to keep these numbers and the count of operations
    # as small as possible.
    while b**k < n:
        a, b = b, b*10  # Exponential growth for b
    # Pinpoint the actual integer root with repeated halving.
    while a < b:
        m = (a+b) // 2  # Careful to use // instead of / here.
        # Also, be careful with the asymmetry a <= m < b. This
        # has caught many a programmer unaware. When a + 1 == b,
        # also m == a then, and assigning a = m would do nothing!
        if (m+1)**k > n:
            b = m  # Since m < b, this advances for sure.
        else:
            a = m+1  # Since a <= m < b, this advances for sure.
        # Either way, the interval from a to b is cut in half.
        # When a and b are integers, they will eventually meet.
        # When a and b are fractions or such, stop once b - a is
        # less than some small epsilon tolerance that you accept
        # as being "Close enough for the government work!"
    return a


def __demo():
    a, b = 2*3*3*13*17*49, 3*5*5*7*19*33
    print(f"Greatest common divisor of {a} and {b}, verbose:")
    euclid_gcd(a, b, verbose=True)
    print(f"\nRoman numbers conversion works? {test_roman()}")
    print(f"\nHeron square root of 2 equals {heron_root(2)}.")

    print("\nHere are some Collatz sequences.")
    for n in [17, 100, 1234567]:
        print(f"{n} reaches 1 with the steps {collatz(n)}")

    print("\nHere are the convergences of some four-lists:")
    rng = Random(12345)
    for i in range(50):
        items = [rng.randint(1, 10 + 10 * i) for _ in range(4)]
        (n, c) = iterate_diff(items, False)
        print(f"{items} converges to {n} in {c} steps.")

    print("\nNext, some integer square roots.")
    for n in [49, 50, 1234567, 10**10]:
        s = integer_root(n)
        print(f"Integer square root of {n} equals {s}.")

    # Here is a humongous number and its integer square root.
    n = 123**456
    s = str(integer_root(n))
    print(f"Integer square root of 123**456 has {len(s)} digits.")
    print(f"First five digits are {s[:5]}, and last five digits are {s[-5:]}.")

    # Which integers are longer written in Arabic than in Roman?
    shorter = [x for x in range(1, 5000) if len(str(x)) > len(roman_encode(x))]
    shorter = ', '.join([f"{x} ({roman_encode(x)})" for x in shorter])
    print(f"\nNumbers longer in Arabic than Roman: {shorter}")


if __name__ == "__main__":
    __demo()
