# So that we can quickly search from the sorted __primelist.

import bisect
from math import sqrt

# This module defines utility functions that generate prime numbers
# so that these generated primes are cached for quick later access.

# The list of prime numbers that we know so far. This will grow,
# as these are just to "prime the pump", heh.

__primelist = [2, 3, 5, 7, 11]


# How far to expand the __primelist.

__prime_max = 10 ** 6


# Determine whether integer n is prime, by checking its divisibility
# by all known prime integers up to the square root of n.

def __is_prime(n):
    # To check whether n is prime, check its divisibility with
    # all known prime numbers up to the square root of n.
    upper = 1 + int(sqrt(n))
    # First ensure that we have enough primes to do the test.
    __expand_primes(upper)
    for d in __primelist:
        if n % d == 0:
            return False
        if d * d > n:
            return True
    return True


# Expand the list of known primes until it the highest integer that
# it contains is at least n.
def __expand_primes(n):
    # Start looking for new primes after the largest prime we know.
    m = __primelist[-1] + 2
    while n > __primelist[-1]:
        if __is_prime(m):
            __primelist.append(m)
        m += 2


# The public functions for the user code that imports this module.

# Determine if the parameter integer n is a prime number.

def is_prime(n):
    # Negative numbers, zero and one are not prime numbers.
    if n < 2:
        return False
    if n < __prime_max:
        # Expand the list of known primes until largest is >= n.
        __expand_primes(n)
        # Use binary search to determine if n is a prime.
        idx = bisect.bisect_left(__primelist, n)
        return __primelist[idx] == n
    else:
        # Determine primality of n the hard way.
        return __is_prime(n)


# Compute the k:th prime number in the sequence of all primes.
def kth_prime(k):
    # Expand the list of known primes until it contains at least k primes.
    while len(__primelist) < k + 1:
        __expand_primes(__primelist[-1] + 2)
    # Look up the k:th prime from the list of known primes.
    return __primelist[k]


# For demonstration purposes when not imported as a module.
def __demo():
    print("Here are the first 100 prime numbers.")
    print([kth_prime(k) for k in range(100)])
    print(f"The primelist now has {len(__primelist)} elements.")
    for k in (999, 9999, 99999):
        print(f"The {k}:th prime number is {kth_prime(k)}.")
        print(f"The primelist now has {len(__primelist)} elements.")
    print("Finally, let us find some Mersenne primes of form 2**n-1.")
    for p in range(40):
        n = 2**p - 1
        if is_prime(n):
            print(f"2**{p} - 1 = {n} is a Mersenne prime.")


if __name__ == "__main__":
    __demo()
