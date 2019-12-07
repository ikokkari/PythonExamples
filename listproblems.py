# Given a sorted list of items, determine whether it contains two
# elements that exactly add up to goal. If parameters i and j are
# given, search only within the subarray from i up to j, inclusive.

def two_summers(items, goal, i = None, j = None):
    i = i if i else 0
    j = j if j else 0
    while i < j:
        x = items[i] + items[j]
        if x == goal:
            return True
        elif x < goal:
            i += 1
        else:
            j -= 1
    return False

# Given two lists s1 and s2, zip them together into one list.
# (Python function zip produces pairs of elements.)

def zip_together(s1, s2):
    i, result = 0, []
    while i < len(s1) and i < len(s2):
        result.append(s1[i])
        result.append(s2[i])
        i += 1
    while i < len(s1):
        result.append(s1[i])
        i += 1
    while i < len(s2):
        result.append(s2[i])
        i += 1
    return result

# Given two sorted lists, create a new list that contains the elements
# of both lists sorted, constructing the new list in one pass.

def merge_sorted(s1, s2):
    i1, i2, result = 0, 0, []
    while i1 < len(s1) and i2 < len(s2):
        if s1[i1] <= s2[i2]:
            result.append(s1[i1])
            i1 += 1
        else:
            result.append(s2[i2])
            i2 += 1
    while i1 < len(s1):
        result.append(s1[i1])
        i1 += 1
    while i2 < len(s2):
        result.append(s2[i2])
        i2 += 1
    return result

# Given two sorted lists, create and return a new list that contains
# the elements that are in both lists. If the lists are sorted, this
# operation can be done in linear time in one pass through both lists.

def intersection_sorted(s1, s2):
    i1, i2, result = 0, 0, []
    while i1 < len(s1) and i2 < len(s2):
        if s1[i1] < s2[i2]:
            i1 += 1
        elif s1[i1] > s2[i2]:
            i2 += 1
        else:
            result.append(s1[i1])
            i1 += 1
            i2 += 1
    return result

# Modify the list s in place so that all elements for which the
# given predicate pred is true are in the front in some order,
# followed by the elements for which pred is false, in some order.    

def partition(s, pred):
    i1, i2 = 0, len(s) - 1
    # Each round, one of the indices takes a step towards the other.
    while i1 < i2:
        # If s[i1] satisfies the predicate, leave it be...
        if pred(s[i1]):
            i1 += 1
        else:
            # Otherwise, swap it to the end
            (s[i1], s[i2]) = (s[i2], s[i1])          
            i2 -= 1
    return s

# List comprehensions make this easier and stable, but at the cost
# of calling pred twice for each element in the list. This version
# maintains the mutual ordering of elements inside the left and
# right partitions, though.

def stable_partition(s, pred):
    return [x for x in s if pred(x)] + [x for x in s if not(pred(x))]

# There exist a multitude of dissimilarity metrics of how different
# two given lists of truth values of same length are from each other.
# If these lists are equal, their dissimilarity is zero, otherwise
# this dissimilarity measure gets larger the more different the lists.

def dissimilarity(first, second, kind='yule'):
    n, n00, n01, n10, n11 = len(first), 0, 0, 0, 0
    for i in range(n):
        if first[i] and second[i]:
            n11 += 1
        elif first[i] and not second[i]:
            n10 += 1
        elif not first[i] and second[i]:
            n01 += 1
        else: # first[i] and second[i] are both false
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

from math import sqrt
import heapq

def apportion_congress_seats(seats, pop, verbose = False):
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
        (priority, i) = heapq.heappop(pq)
        # That state receives one more seat.
        result[i] += 1
        # Update the priority of that state and put it back to queue.
        newpq = -pop[i] / sqrt(result[i] * (result[i] + 1))
        heapq.heappush(pq, (newpq, i))        
        seats -= 1
    return result

if __name__ == "__main__":    
    print("Partitioning numbers from 1 to 10:")
    print(partition(list(range(1, 11)), lambda x: x % 2 == 0))
    print("\nZipping together:")
    print(zip_together([1, 2, 3, 4, 5], [99, 44, -55]))
    print("\nMerging two sorted lists:")
    print(merge_sorted([-4, 2, 5, 9, 10], [-2, -1, 0, 6]))
    print("\nComputing the intersection:")
    print(intersection_sorted([-4, -2, 10, 12], [-2, 0, 6, 10, 11]))

    from random import randint    
    kinds = ['yule', 'dice', 'sokal-sneath', 'jaccard', 'matching', 'rogers-tanimoto']
    print("\nHere are some dissimilarity metrics for random bit vectors.\n")
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
        
    # Let's make up a small pretend nation with five states and 16 seats.
    print("\nApportioning congressional seats:")
    pops = [32, 22, 14, 8, 5]
    print(f"Seats are given as {apportion_congress_seats(16, pops, True)}.")
    # The Huntington-Hill algorithm can also be used to compute
    # rounded percentages without any rounding error.
    print(f"\nHere are the rounded percentages of {pops}:")
    pct = apportion_congress_seats(1000, pops, False)
    # These rounded percentages will add up to exactly 100.
    print([f"{p/10:.1f}" for p in pct])