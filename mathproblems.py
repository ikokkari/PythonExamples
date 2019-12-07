# The oldest algorithm in recorded history, Euclid's algorithm to find
# the greatest common divisor of two nonnegative integers.

def euclid_gcd(a, b, verbose = False):
    while b > 0:
        a, b = b, a % b
        if verbose:
            print(f"a is {a}, b is {b}")
    return a

# Generate the Collatz series from the given starting value.
# https://en.wikipedia.org/wiki/Collatz_conjecture

def collatz(start):
    curr, result = start, []
    if curr < 1:
        return []
    while curr > 1:
        result.append(curr)
        if curr % 2 == 0:
            curr = curr // 2
        else:
            curr = 3 * curr + 1
    result.append(1)
    return result

# Given the previous ability to generate the Collatz series starting
# from the given number, determine which number from start to end - 1
# produces the longest Collatz series, and return that number.

def longest_collatz(start, end):
    best = start
    best_len = len(collatz(start))
    for x in range(start + 1, end):
        curr_len = len(collatz(x))
        if curr_len > best_len:
            best_len = curr_len
            best = x
    return best

# If you add up the sum of digits of a positive integer until only
# a single digit remains, what is digit do you end up with?

def final_digit(n):
    while n > 9:
        n = sum([int(d) for d in str(n)])
    return n

# Another algorithm from the ancient world, Heron's square root method
# to numerically iterate the guess for the square root of the positive
# real number x. (This algorithm generalizes to arbitrary roots, and in
# fact turns out to be special case of Newton's numerical iteration
# with the function whose root we want to solve hardcoded to square root.) 

def heron_root(x):
    if x < 0:
        raise ValueError("Square roots of negative numbers not allowed")
    guess = x / 2
    prev = 0
    while guess != prev: # This will converge in float precision.
        prev = guess
        guess = (guess + x / guess) / 2
    return guess

# Converting Roman numerals and positional integers back and forth makes
# for interesting and education excample of loops, lists and dictionaries.

symbols_encode = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'),
    (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'),
    (5, 'V'), (4, 'IV'), (1, 'I')
]

def roman_encode(n):
    if n < 1:
        raise ValueError("Romans did not have zero or negative numbers")
    result = ''
    for (v, s) in symbols_encode:
        while v <= n: # same symbol can be used several times 
            result += s
            n -= v
    return result

# Dictionaries are handy to map symbols into the values that they encode.

symbols_decode = {
    'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1
}

def roman_decode(s):
    result = 0
    prev = 0
    for c in reversed(s): # Loop through symbols from right to left
        v = symbols_decode[c]
        if prev > v:
            result -= v
        else:
            result += v
        prev = v
    return result        

# Whenever you have two functions that are each other's inverses, it is
# quite easy to test them by looping through some large number of possible
# inputs to first, and verifying that both functions really invert the
# result produced by the other.

def test_roman():
    for n in range(1, 5000):
        if n != roman_decode(roman_encode(n)):
            return False
    return True

# Another famous numerical method to find the root of the function f within
# the given tolerance, looking for solution from real interval [x0, x1].

def secant_method(f, x0 = 0, x1 = 1, tol = 0.000000001, verbose = False):
    fx0 = f(x0)
    fx1 = f(x1)
    while abs(x1 - x0) > tol:
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        fx2 = f(x2)
        x0, x1, fx0, fx1 = x1, x2, fx1, fx2
        if verbose:
            print(f"x = {x0:.15f}, diff = {abs(x1-x0):.15f}")
    return (x0 + x1) / 2

if __name__ == "__main__":
    print("Greatest common divisor of 123456 and 654321, visualized:")
    euclid_gcd(123456, 654321, verbose = True)
    print(f"Roman numbers conversion works? {test_roman()}")
    print(roman_decode(roman_encode(1234)))
    print(f"Heron square root of 2 equals {heron_root(2)}.")

    # How many numbers are longer written in Arabic than in Roman?
    shorter = [str(x) for x in range(1, 5000) if len(str(x)) > len(roman_encode(x))]
    print(f"Numbers longer written in Arabic than in Roman are: {', '.join(shorter)}")

    # Random sampling is often a good way to estimate the behaviour of
    # some process for which we don't know the analytical solution.
    from random import randint    
    digits = [final_digit(randint(2, 1000) ** randint(2, 1000)) for i in range(3000)]    
    print("For random integer powers, the final digit counts are:")
    counts = [(i, digits.count(i)) for i in range(1, 10)]
    # Strange result. Why does that happen?
    print(", ".join([f"{i}->{c}" for (i, c) in counts]))
        
    def testfunc(x):
        return 4 * x**4 - 17 * x**3 + 10 * x**2 + 8
    print("Let us test out the secant method.")
    r = secant_method(testfunc, -1, 3, verbose = True)
    print(f"Found root at {r:.6} where testfunc gives {testfunc(r):.6}")