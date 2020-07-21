import functools
import operator
import itertools
from fractions import Fraction

# Many problems can be solved surprisingly easily by first
# solving a smaller version of that problem, whose result is
# then productively used in solving the original problem. The
# classic textbook first example of recursion is factorial.


def factorial(n):
    if n < 2:
        return 1                      # base case
    else:
        return n * factorial(n - 1)   # recursive call


# Functional programming version, if only for humour value:

def factorial_func(n):
    return functools.reduce(operator.mul, range(1, n+1))


# Why not Zoidb... itertools? Without more-itertools, we
# need to define the lazy last element extractor ourselves.

def last_elem(it):
    last = next(it)
    for c in it:
        last = c
    return last


def factorial_it(n):
    return last_elem(itertools.accumulate(
        range(1, n+1), operator.mul)
    )


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
        return
    mid = 6 - src - tgt
    hanoi(src, mid, n-1)
    print(f"Move top disk from peg {src} to peg {tgt}.")
    hanoi(mid, tgt, n-1)


# For computing high integer powers, binary power is more efficient
# than repeated multiplication n - 1 times.

def binary_power(a, n, verbose=False):
    if verbose:
        print(f"Entering binary_power({n}).")
    if n < 0:
        raise ValueError("Binary power negative exponent not allowed.")
    elif n == 0:
        result = 1
    elif n % 2 == 0:
        result = binary_power(a * a, n // 2, verbose)
    else:
        result = a * binary_power(a * a, (n-1) // 2, verbose)
    if verbose:
        print(f"Exiting binary_power({n}) with {result}.")
    return result


# Flattening a list that can contain other lists as elements is a
# classic list programming exercise. This being Python, the correct
# "duck typing" spirit of checking of something is a list is to
# check if it is iterable, that is, for our purposes it behaves
# like a list.

def flatten(li):
    result = []
    for x in li:
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
    answer = subset_sum(items, goal-last)
    if answer is not None:
        answer.append(last)
    else:
        answer = subset_sum(items, goal)
    items.append(last)
    return answer


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
        return x > 0 and y > 0 and x <= n and y <= n

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
# really, really fast. Faster than you can begin to imagine,
# until you have taken some decent theory of computability
# courses. And probably not even then.
# http://en.wikipedia.org/wiki/Ackermann_function

def ackermann(m, n):
    if m == 0:
        return n+1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


if __name__ == "__main__":
    f1 = factorial(10)
    f2 = factorial_func(10)
    f3 = factorial_it(10)
    print(f"The factorial of 10 equals {f1}, {f2} and {f3}.")
    print("Solution for Towers of Hanoi with three disks:")
    hanoi(1, 3, 3)
    print("Here is one solution to subset sum with goal 81:")
    print(subset_sum([1, 4, 7, 10, 15, 22, 23, 35, 37], 81))
    print("Flattening the list produces the following:")
    print(flatten([1, (42, 99), [2, [3, [4, [5], 6], 7], 8], 9]))
    print("Here is a 6*6 knights tour:")
    print(knight_tour(6, 1, 1))
    print(f"Ackermann(3, 3) = {ackermann(3, 3)}.")
    print(f"Ackermann(3, 4) = {ackermann(3, 4)}.")
    # print(f"Ackermann(4, 4) = {ackermann(4, 4)}.")
    # would give error "recursion limit exceeded"
    print(f"Steps of computing binary_power(2, 100) are:")
    bp = binary_power(2, 100, True)
    print(f"The result is {bp}.")

    # Gold testing means testing a function against some existing
    # "golden" function already known to be correct.
    assert 2**10001 == binary_power(2, 10001)

    # Python functions are polymorphic in that they don't care about
    # the actual type of their argument, as long as the arguments have
    # the capabilities expected from them.
    b = Fraction(3, 7)
    print(f"{b} raised to 100th power equals {binary_power(b, 100)}.")
    v = 123456789
