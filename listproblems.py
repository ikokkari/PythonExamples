from fractions import Fraction
import heapq


# Given a sorted list of items, determine whether it contains two
# elements that exactly add up to goal. If parameters i and j are
# given, search only within the sublist from i up to j, inclusive.

# This is an example of technique known as "two pointers". Two
# position indices start from the beginning and end of sequence.
# Each round, one of these indices moves towards the other one,
# maintaining the assumption that if the sequence contained the
# solution in the first place, a solution still remains between
# these indices. Eventually, either a solution will be found, or
# the indices meet in the middle and reduce the problem to its
# trivial base case.

def two_summers(items, goal, i=0, j=None):
    j = len(items) - 1 if j is None else j
    while i < j:
        x = items[i] + items[j]
        if x == goal:
            return True  # Okay, that's a solution.
        elif x < goal:
            i += 1  # Smallest element can't be part of solution.
        else:
            j -= 1  # Largest element can't be part of solution.
    return False


# In the graded labs, solve the classic problem of three_summers
# where you need to find three elements that add up to the goal.
# This function can use two_summers as a helper function.

# Modify the list s in place so that all elements for which the
# given predicate is true are in the front in some order, followed
# by the elements for which the predicate is false, in some order.

def partition_in_place(s, predicate):
    # Elements from position i to j, inclusive, can be anything.
    # Anything to left of i is acceptable, anything to the right
    # of j is unacceptable. When i == j, all is well.
    i, j = 0, len(s) - 1
    # Each round, one of the indices takes a step towards the other.
    while i < j:
        # If s[i1] satisfies the predicate, leave it be...
        if predicate(s[i]):
            i += 1
        else:
            # Otherwise, swap it to the end
            s[i], s[j] = s[j], s[i]
            j -= 1
    # Note that for list of n elements, the predicate is called exactly
    # n - 1 times. This can be valuable if the predicate is expensive.
    return s


# List comprehensions make this easier and stable, but at the cost
# of calling the predicate twice for each element in the list. This
# version maintains the mutual ordering of elements inside the left
# and right partitions, though, thanks to list comprehensions.

def stable_partition(s, predicate):
    return [x for x in s if predicate(x)] + [x for x in s if not predicate(x)]


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
            return (n10 + n01) / (2 * n11 + n10 + n01)
        elif kind == 'sokal-sneath':
            return (2 * (n10 + n01)) / (n11 + 2 * (n10 + n01))
        elif kind == 'jaccard':
            return (n10 + n01) / (n11 + n10 + n01)
        elif kind == 'matching':
            return (n10 + n01) / len(first)
        elif kind == 'rogers-tanimoto':
            return (2 * (n10 + n01)) / (n11 + 2 * (n10 + n01) + n00)
        else:
            raise ValueError(f"Unknown dissimilarity metric {kind}")
    except ZeroDivisionError:
        return 0


# Let us calculate how the congressional seats are divided over states
# whose populations (in millions) are given in the parameter list pop.
# The classic Huntington-Hill algorithm creates the fairest possible
# allocation under the constraint that every state gets some integer
# number of seats.

# Instead of the usual priority formula pop / sqrt(s*(s+1)) that needs
# floating point functions and square roots, we square the priority to
# the form (pop * pop) / (s * (s+1)) that we can handle exactly as an
# integer Fraction.

def apportion_congress_seats(seats, pop):
    # List of seats assigned to each state, initially one per state.
    result = [1 for _ in pop]
    # List of states and their current priorities.
    pq = [(Fraction(-p * p, 2), i) for (i, p) in enumerate(pop)]
    # Organize the list into a priority queue.
    heapq.heapify(pq)
    seats -= len(pop)
    # Give out the remaining seats one at the time.
    while seats > 0:
        # Pop from priority queue the state with the highest priority.
        (priority, state) = heapq.heappop(pq)
        # That state receives one more seat.
        result[state] += 1
        # Update the priority of that state and put it back to queue.
        new_pq = Fraction(-pop[state] * pop[state], result[state] * (result[state] + 1))
        heapq.heappush(pq, (new_pq, state))
        seats -= 1
    return result


def __demo():
    print("Partitioning integers from 1 to 10, unstable:")
    print(partition_in_place(list(range(1, 11)), lambda x: x % 2 == 0))
    print("Partitioning integers from 1 to 10, stable:")
    print(stable_partition(list(range(1, 11)), lambda x: x % 2 == 0))

    from random import randint
    kinds = ['yule', 'dice', 'sokal-sneath', 'jaccard',
             'matching', 'rogers-tanimoto']
    print("\nSome dissimilarity metrics for random vectors.")
    print("v1       v2       yule   dice   s-s    jac    match  r-t")
    for i in range(10):
        v1 = [randint(0, 1) for _ in range(8)]
        v2 = [randint(0, 1) for _ in range(8)]
        # No vector can ever be dissimilar from itself.
        if any([dissimilarity(v1, v1, kind) != 0 for kind in kinds]):
            print("Something is hinky with dissimilarities!")
        res = [f"{dissimilarity(v1, v2, kind):.4f}" for kind in kinds]
        res = " ".join(res)
        o1 = "".join([str(x) for x in v1])
        o2 = "".join([str(x) for x in v2])
        print(f"{o1} {o2} {res}")

    # https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population
    # April 2020 census data, 50 states + DC
    us_states = [
        ('AL', 5024279), ('AK', 733391), ('AZ', 7151502), ('AR', 3011524),
        ('CA', 39538223), ('CO', 5773714), ('CT', 3605944), ('DC', 689545),
        ('DE', 989948), ('FL', 21538187), ('GA', 10711908), ('HI', 1455271),
        ('ID', 1839106), ('IL', 12812508), ('IN', 6785528), ('IA', 3190369),
        ('KS', 2937880), ('KY', 4505836), ('LA', 4657757), ('ME', 1362359),
        ('MD', 6177224), ('MA', 7029917), ('MI', 10077331), ('MN', 5706494),
        ('MS', 2961279), ('MT', 1084225), ('MO', 6154913), ('NE', 1961504),
        ('NV', 3104614), ('NH', 1377529), ('NJ', 9288994), ('NM', 2117522),
        ('NY', 20201249), ('NC', 10439388), ('ND', 779094), ('OH', 11799448),
        ('OK', 3959353), ('OR', 4237256), ('PA', 13002700), ('RI', 1097379),
        ('SC', 5118425), ('SD', 886667), ('TN', 6910840), ('TX', 29145505),
        ('UT', 3271616), ('VT', 643077), ('VA', 8631393), ('WA', 7705281),
        ('WV', 1793716), ('WI', 5893718), ('WY', 576851)
    ]

    us_congress = apportion_congress_seats(435, [pop for (_, pop) in us_states])
    us_congress = [(abbr, seats) for ((abbr, _), seats) in zip(us_states, us_congress)]
    print("\nU.S. House of Representatives, seats according to April 2020 census:")
    for (i, (abbr, seats)) in enumerate(us_congress):
        print(f"{abbr}:{seats:-3d}", end=('\n' if i % 8 == 7 else '   '))

    # The Huntington-Hill algorithm can also be used to compute optimal
    # rounded percentages so that the percentages add up to exactly 100.
    # Demonstrate this with some made-up data values:
    pops = [42, 33, 17, 11, 8, 7, 2]
    print(f"\n\nFor comparison, rounded percentages of {pops}:")
    pct = apportion_congress_seats(1000, pops)
    # Rounded percentages are guaranteed to add up to exactly 100.
    print(", ".join([f"{p / 10:.1f}" for p in pct]))


if __name__ == "__main__":
    __demo()
