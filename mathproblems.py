# The oldest algorithm in recorded history, Euclid's algorithm to find
# the greatest common divisor of two nonnegative integers.

def euclid_gcd(a, b, verbose = False):
    while b > 0:
        a, b = b, a % b
        if verbose:
            print(f"a={a}, b={b}")
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

# Continued fractions are an alternative way to represent integer
# fractions as a sequence of smallish integers. If a/b is rational,
# the resulting continued fraction is finite. For irrational numbers
# the continued fraction is infinite, but for some numbers such as
# the golden ratio have a nice continued fraction form that can be
# used to approximate that irrational number to any precision.
# https://en.wikipedia.org/wiki/Continued_fraction    

# This assumes that 0 < a < b. To work for all rational numbers,
# the whole integer part must be encoded separately, and the
# actual continued fraction merely handles the fractional part.

def f_to_cf(a, b, verbose = False):
    result = []
    while a > 0 and b > 1:
        # As we see, the core operation is same as in euclid_gcd.
        if verbose:
            print(f"a={a}, b={b}")
        q, r = b // a, b % a        
        result.append(q) # This time we store the quotient info
        a, b = r, a
    return result

# Converting a continued fraction into an ordinary fraction is
# best done "inside out", a principle that works for many other
# problems also. It is how expressions are evaluated, after all.

from fractions import Fraction

def cf_to_f(items):
    result = None
    for e in reversed(items):
        if result == None:
            result = e
        else:
            result = e + Fraction(1, result)
    return result

# Another algorithm from the ancient world, Heron's square root method
# to numerically iterate the guess for the square root of the positive
# real number x. (This algorithm generalizes to arbitrary roots, and in
# fact turns out to be special case of Newton's numerical iteration
# with the function whose root we want to solve hardcoded to square root.) 

def heron_root(x):
    if x < 0:
        raise ValueError("Square roots of negative numbers not allowed")
    guess, prev = x / 2, 0    
    while guess != prev: # This will converge in float precision.
        prev, guess = guess, (guess + x / guess) / 2        
    return guess

# Converting Roman numerals and positional integers back and forth
# makes for interesting and educational excample of loops, lists
# and dictionaries.

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

# Dictionaries map symbols into the values that they encode.

symbols_decode = {
    'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1
}

def roman_decode(s):
    result, prev = 0, 0    
    for c in reversed(s): # Loop through symbols from right to left
        v = symbols_decode[c]
        # One-liner version of if-else to choose between two values.
        result += (v if prev <= v else -v)
        prev = v
    return result        

# Whenever you have two functions that are each other's inverses, it is
# easy to test them by looping through some large number of possible
# inputs and verifying that both functions really invert the result
# produced by the other.

def test_roman():
    for n in range(1, 5000):
        if n != roman_decode(roman_encode(n)):
            return False
    return True


if __name__ == "__main__":
    a, b = 2*3*3*13*17*49, 3*5*5*7*33*19    
    print(f"Greatest common divisor of {a} and {b}, visualized:")
    euclid_gcd(a, b, verbose = True)
    print(f"Roman numbers conversion works? {test_roman()}")
    print(f"Heron square root of 2 equals {heron_root(2)}.")

    print(f"Continued fraction for {a}/{b} is {f_to_cf(a, b, True)}.")

    # How many numbers are longer written in Arabic than in Roman?
    shorter = [x for x in range(1, 5000) if len(str(x)) > len(roman_encode(x))]
    shorter = [f"{x} ({roman_encode(x)})" for x in shorter]
    print(f"Numbers longer written in Arabic than in Roman are: {', '.join(shorter)}")
    
    # Let us approximate the Golden Ratio using the first 150 terms
    # from its infinitely long continued fraction representation.
    # https://en.wikipedia.org/wiki/Golden_ratio
    grf = cf_to_f([1] * 150) # Handy to create a list of identical items
    from decimal import getcontext, Decimal
    getcontext().prec = 50   # Number of decimal places used in Decimal   
    grd = Decimal(grf.numerator) / Decimal(grf.denominator)
    print("In 50 decimal places, the golden ratio is approximately:")
    print(f"{grd}")
    # Correct answer copied from Wolfram Alpha:
    #print("1.6180339887498948482045868343656381177203091798058")