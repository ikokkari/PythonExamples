from fractions import Fraction
from decimal import Decimal, getcontext
from math import fsum


def demonstrate_imprecision():
    # Floating point can represent exactly only terminating series of
    # powers of two. All three numbers are unrepresentable.
    if 0.1 + 0.2 == 0.3:
        print("Mathematics works as it should, no problemo!")
    else:
        print("Basic arithmetic has gone topsy turvy!")

    # Decimal to the rescue!
    if Decimal(0.1) + Decimal(0.2) == Decimal(0.3):
        print("Decimal works just fine!")
    else:
        print("The Decimals! They do nothing!")

    # Always create a Decimal object from a string, otherwise you get
    # an exact representation of a number that is already inexact.
    if Decimal("0.1") + Decimal("0.2") == Decimal("0.3"):
        print("All is well in the world again!")

    # Precision of floating point does not work out well when adding
    # numbers of vastly different magnitudes.
    print(sum([3e30, 1, -3e30]))   # 0.0
    # Better.
    print(fsum([3e30, 1, -3e30]))  # 1.0


def decimal_precision_demo():
    a = Decimal("0.2")
    b = Decimal("0.3")
    print(a * b)    # 0.06
    a = Decimal("0.2000")
    b = Decimal("0.3000")
    print(a * b)     # 0.06000000
    a = Decimal("0.12345")
    b = Decimal("0.98765")
    print(a * b)    # 0.1219253925
    getcontext().prec = 5
    a = Decimal("0.12345")
    b = Decimal("0.98765")
    print(a * b)    # 0.12193
    # Unlike machine floats, Decimal values cannot under- or overflow
    a = Decimal("0.1") ** 1000
    print(a)
    a = Decimal("2") ** 10000
    print(a)


def infinity_and_nan_demo():
    ninf = float('-inf')
    pinf = float('inf')
    print(f"Plus infinity minus 7 equals {(pinf - 7)}.")
    print(f"Plus infinity plus infinity equals {(pinf + pinf)}.")
    print(f"Minus infinity times minus 4 equals {(ninf * -4)}.")
    nan = pinf + ninf
    print(f"Infinity minus infinity equals {nan}.")
    print(f"nan equals nan is {nan == nan}.")


def harmonic(n):
    total = Fraction(0)
    for i in range(1, n+1):
        total += Fraction(1, i)
    return total


def estimate_pi(n):
    total = Fraction(0)
    for i in range(1, n+1):
        total += Fraction(1, i*i)
    return total * 6


def __demo():
    demonstrate_imprecision()
    decimal_precision_demo()
    infinity_and_nan_demo()
    pi = estimate_pi(10000)
    getcontext().prec = 10
    print("Estimating pi: ", end="")
    print((Decimal(str(pi.numerator)).sqrt() /
           Decimal(str(pi.denominator)).sqrt()))


if __name__ == "__main__":
    __demo()
