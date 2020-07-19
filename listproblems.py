from math import sqrt
import heapq

# Given a sorted list of items, determine whether it contains two
# elements that exactly add up to goal. If parameters i and j are
# given, search only within the subarray from i up to j, inclusive.


def two_summers(items, goal, i=0, j=None):
    j = j if j is not None else len(items)-1
    while i < j:
        x = items[i] + items[j]
        if x == goal:
            return True
        elif x < goal:
            i += 1
        else:
            j -= 1
    return False


# In the graded labs, solve the classic problem of three_summers
# in which you need to find three elements that add up to the goal.

# Modify the list s in place so that all elements for which the
# given predicate pred is true are in the front in some order,
# followed by the elements for which pred is false, in some order.

def partition(s, pred):
    i1, i2 = 0, len(s) - 1
    # Each round, one of the indices takes a step towards other.
    while i1 < i2:
        # If s[i1] satisfies the predicate, leave it be...
        if pred(s[i1]):
            i1 += 1
        else:
            # Otherwise, swap it to the end
            s[i1], s[i2] = s[i2], s[i1]
            i2 -= 1
    # Note that for list of n elements, pred is called exactly
    # n-1 times. This can be valuable if pred is expensive.
    return s


# List comprehensions make this easier and stable, but at the cost
# of calling pred twice for each element in the list. This version
# maintains the mutual ordering of elements inside the left and
# right partitions, though, thanks to list comprehensions.

def stable_partition(s, pred):
    return [x for x in s if pred(x)] + [x for x in s if not pred(x)]


# There exist a multitude of dissimilarity metrics of how different
# two given lists of truth values of same length are from each other.
# If these lists are equal, their dissimilarity is zero, otherwise
# this dissimilarity measure gets larger the more different the lists.

def dissimilarity(first, second, kind='yule'):
    n00, n01, n10, n11 = 0, 0, 0, 0
    for f, s in zip(first, second):
        if f and s:
            n11 += 1
        elif f and not s:
            n10 += 1
        elif not f and s:
            n01 += 1
        else:  # f and s are both false
            n00 += 1
    try:
        if kind == 'yule':
            return (2 * (n10 + n01)) / (n11 * n00 + n01 * n10)
        elif kind == 'dice':
            return (n10 + n01) / (2*n11 + n10 + n01)
        elif kind == 'sokal-sneath':
            return (2 * (n10 + n01)) / (n11 + 2*(n10 + n01))
        elif kind == 'jaccard':
            return (n10 + n01) / (n11 + n10 + n01)
        elif kind == 'matching':
            return (n10 + n01) / len(first)
        elif kind == 'rogers-tanimoto':
            return (2 * (n10 + n01)) / (n11 + 2*(n10 + n01) + n00)
        else:
            raise ValueError(f"Unknown dissimilarity metric {kind}")
    except ZeroDivisionError:
        return 0

# Let us calculate how the congressional seats are divided over states
# whose populations (in millions) are given in the parameter list pop.
# The classic Huntington-Hill algorithm creates the fairest possible
# allocation under the constraint that every state gets some integer
# number of seats.


def apportion_congress_seats(seats, pop):
    # List of seats assigned to each state, initially one per state.
    result = [1 for p in pop]
    # List of states and their current priorities.
    pq = [(-p / sqrt(2), i) for (i, p) in enumerate(pop)]
    # Organize the list into a priority queue.
    heapq.heapify(pq)
    seats -= len(pop)
    # Give out the remaining seats one at the time.
    while seats > 0:
        # Pop from priority queue the state with highest priority.
        (priority, state) = heapq.heappop(pq)
        # That state receives one more seat.
        result[state] += 1
        # Update the priority of that state and put it back to queue.
        newpq = -pop[state] / sqrt(result[state] * (result[state] + 1))
        heapq.heappush(pq, (newpq, state))
        seats -= 1
    return result


if __name__ == "__main__":
    print("Partitioning integers from 1 to 10, unstable:")
    print(partition(list(range(1, 11)), lambda x: x % 2 == 0))
    print("Partitioning integers from 1 to 10, stable:")
    print(stable_partition(list(range(1, 11)), lambda x: x % 2 == 0))

    from random import randint
    kinds = ['yule', 'dice', 'sokal-sneath', 'jaccard',
             'matching', 'rogers-tanimoto']
    print("\nSome dissimilarity metrics for random vectors.")
    print("v1       v2       yule   dice   s-s    jac    match  r-t")
    for i in range(10):
        v1 = [randint(0, 1) for i in range(8)]
        v2 = [randint(0, 1) for i in range(8)]
        # No vector can ever be dissimilar from itself.
        if any([dissimilarity(v1, v1, kind) != 0 for kind in kinds]):
            print("Something is hinky with dissimilarities!")
        res = [f"{dissimilarity(v1, v2, kind):.4f}" for kind in kinds]
        res = " ".join(res)
        o1 = "".join([str(x) for x in v1])
        o2 = "".join([str(x) for x in v2])
        print(f"{o1} {o2} {res}")

    # A small pretend nation with five states and 100 seats.
    pops = [32, 22, 14, 8, 5]
    seats = apportion_congress_seats(100, pops)
    print(f"\nCongressonal seats for {pops} are given as {seats}.")
    # The Huntington-Hill algorithm can also be used to compute optimal
    # rounded percentages so that the percentages add up to exactly 100.
    print(f"\nFor comparison, rounded percentages of {pops}:")
    pct = apportion_congress_seats(1000, pops)
    # These rounded percentages will add up to exactly 100.
    print(", ".join([f"{p/10:.1f}" for p in pct]))
