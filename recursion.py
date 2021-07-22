from functools import lru_cache
from fractions import Fraction

# Many problems can be solved surprisingly easily by first
# solving a smaller version of that problem, whose result is
# then productively used in solving the original problem. The
# classic textbook first example of recursion is factorial
# whose formula n! = 1 * 2 * ... * (n-1) * n is self-similar.


@lru_cache()
def factorial(n, verbose=False):
    if verbose:
        print(f"enter with n = {n}")
    if n < 2:
        result = 1                      # base case
    else:
        result = n * factorial(n - 1, verbose)   # linear recursive call
    if verbose:
        print(f"Returning {result} from {n}")
    return result


# Well, that was nothing much to write home about, since we
# already did that with iteration. However, it turns out that
# in theory, what you can do with recursion you can also do with
# iteration, and vice versa. However, in practice one of the
# techniques can be vastly superior for some problems. A couple
# of example problems where the recursive solution is easier
# than iteration. First, the classic Towers of Hanoi puzzle.
# http://en.wikipedia.org/wiki/Towers_of_Hanoi

def hanoi(src, tgt, n):
    if n < 1:
        return None
    mid = 6 - src - tgt
    hanoi(src, mid, n - 1)
    print(f"Move top disk from peg {src} to peg {tgt}.")
    hanoi(mid, tgt, n - 1)


# For computing high integer powers, binary power is more efficient
# than repeated multiplication n - 1 times.

def binary_power(a, n, verbose=False):
    if verbose:
        print(f"Entering binary_power({n}).")
    if n < 0:
        raise ValueError(f"Negative exponent {n} not allowed.")
    elif n == 0:
        result = 1
    elif n % 2 == 0:
        result = binary_power(a * a, n // 2, verbose)
    else:
        result = a * binary_power(a * a, (n - 1) // 2, verbose)
    if verbose:
        print(f"Exiting binary_power({n}) with {result}.")
    return result


# Flattening a list that can contain other lists as elements is a
# classic list programming exercise. This being Python, the correct
# "duck typing" spirit of checking of something is an iterable
# sequence is to check if it allows creation of iterator objects
# with the magic method __iter__, that is, for our purposes it acts
# like a sequence.

def flatten(items):
    result = []
    for x in items:
        if hasattr(x, '__iter__'):  # is x an iterable?
            result.extend(flatten(x))
        else:
            result.append(x)
    return result


# http://en.wikipedia.org/wiki/Subset_sum_problem
# The subset sum problem asks if it is possible to select a subset
# of given items (all assumed to be integers) that together add up
# exactly to goal. If no solution exists, the function returns None,
# otherwise it returns the lexicographically highest sublist of
# items whose elements together add up exactly to the goal.

def subset_sum(items, goal):
    if goal == 0:
        return []
    if len(items) == 0 or goal < 0:
        return None
    last = items.pop()
    # Take the last element into chosen subset
    answer = subset_sum(items, goal - last)
    if answer is not None:
        answer.append(last)
    else:
        # Try not taking last element into subset
        answer = subset_sum(items, goal)
    items.append(last)
    return answer


# Hofstadter's recursive Q-function, memoized for efficiency.
# http://paulbourke.net/fractals/qseries/

@lru_cache(maxsize=10000)
def hof_q(n):
    if n < 3:
        return 1
    else:
        return hof_q(n - hof_q(n - 1)) + hof_q(n - hof_q(n - 2))


# The famous Thue-Morse sequence for "fairly taking turns". To
# illustrate the power of memoization, let's use a global count
# of how many times the function has been called.

__tm_call_count = 0


@lru_cache(maxsize=10000)
def thue_morse(n, sign):
    global __tm_call_count
    __tm_call_count += 1
    if n < 2:
        return f"{str(sign)}"
    else:
        return thue_morse(n - 1, sign) + thue_morse(n - 1, 1 - sign)


# An interesting problem from "Concrete Mathematics". A row of aging
# barrels is filled with wine at year 0. After each year, a portion
# of the aged wine from each barrel is poured in the next barrel from
# end to beginning. The wine taken from last barrel is bottled for
# sale, and the first barrel is refilled with new wine. What is the
# composition of the given barrel after the number of years?

@lru_cache(maxsize=10000)
def wine(barrel, age, year, pour=Fraction(1, 2)):
    # Imaginary "zero" barrel to represent incoming flow of new wine.
    if barrel == 0:
        return Fraction(1) if age == 0 else 0
    # In the initial state, all barrels consist of new wine.
    elif year == 0:
        return 1 if age == 0 else 0
    # Recursive formula for proportion of wine of age a.
    else:
        return (1 - pour) * wine(barrel, age - 1, year - 1) +\
               pour * wine(barrel - 1, age - 1, year - 1)


# The knight's tour problem is another classic. Given an n*n chessboard,
# and the start coordinates of the knight, find a way to visit every
# square on the board exactly once, ending up in some neighbour of
# the square that the knight started from.
# http://en.wikipedia.org/wiki/Knight's_tour

def knight_tour(n=8, sx=1, sy=1):
    # List to accumulate the moves during the recursion.
    result = []
    # Squares that the tour has already visited.
    visited = set()
    # Eight possible moves of a chess knight.
    moves = ((2, 1), (1, 2), (2, -1), (-1, 2),
             (-2, 1), (1, -2), (-2, -1), (-1, -2))

    # Test whether square (x, y) is inside the chessboard. We use
    # the 1-based indexing here, as is normally done by humans.
    def inside(x, y):
        return 0 < x <= n and 0 < y <= n

    # Find all the unvisited neighbours of square (x, y).
    def neighbours(x, y):
        return [(x+dx, y+dy) for (dx, dy) in moves
                if inside(x+dx, y+dy)
                and (x+dx, y+dy) not in visited]

    # Try to generate the rest of the tour from square (cx, cy).
    def generate_tour(cx, cy):
        result.append((cx, cy))
        if len(result) == n*n:
            # The tour must be closed to be considered success.
            return (sx - cx, sy - cy) in moves
        visited.add((cx, cy))
        for (nx, ny) in neighbours(cx, cy):
            if generate_tour(nx, ny):
                return True
        # Undo the current move
        result.pop()
        visited.remove((cx, cy))
        return False
    if generate_tour(sx, sy):
        return result
    else:
        return None


# Ackermann function is a function that grows fast. Really,
# really, really fast. In fact, you could fill our universe
# with the word "really", and that still wouldn't be enough
# words "really" to describe its unimaginable growth.
# http://en.wikipedia.org/wiki/Ackermann_function

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


def __demo():
    print(f"The factorial of 10 equals {factorial(10)}.")

    print("\nSolution for Towers of Hanoi with three disks:")
    hanoi(1, 3, 3)

    items = [1, 4, 7, 10, 15, 22, 23, 30, 32]
    print(f"\nSolving subset sum with {items}:")
    for goal in range(100, 110):
        print(f"Goal {goal}: solution {subset_sum(items, goal)!r}")

    print("\nFlattening the list produces the following:")
    print(flatten([1, (42, 99), [2, [3, [4, [5], 6], 7], 8], 9]))

    print("\nHere is a closed knights tour on a 6-by-6 chessboard:")
    print(knight_tour(6, 1, 1))

    print(f"\nAckermann(3, 3) = {ackermann(3, 3)}.")
    print(f"Ackermann(3, 4) = {ackermann(3, 4)}.")
    # print(f"Ackermann(4, 4) = {ackermann(4, 4)}.")
    # would give error "recursion limit exceeded"

    print(f"\nSteps of computing binary_power(2, 100) are:")
    bp = binary_power(2, 100, True)
    print(f"The result is {bp}.")

    # Gold testing means testing a function against some existing
    # "golden" function already known to be correct.
    assert 2**10001 == binary_power(2, 10001)

    # Python functions are polymorphic in that they don't care about
    # the actual type of their argument, as long as the arguments have
    # the capabilities expected from them.
    b = Fraction(4, 5)
    print(f"\n{b} raised to 100th power equals {binary_power(b, 100)}.")

    print("\nHere are the first 500 items of Hofstadter's Q-series:")
    print(", ".join((str(hof_q(n)) for n in range(501))))

    year = 10
    print(f"\nAfter year {year}, the wine barrels consist of (year:portion):")
    for b in range(1, 6):
        comps = [f"{a}:{wine(b, a, year)}" for a in range(1, year + 1)]
        print(f"Barrel {b}: {', '.join(comps)}.")

    print("\nThe Thue-Morse sequences from 2 to 10 are:")
    for i in range(2, 11):
        print(f"{i}: {thue_morse(i, 0)}")
    print(f"\nExecuted total of {__tm_call_count} calls to Thue-Morse.")


if __name__ == "__main__":
    __demo()
