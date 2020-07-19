# Regular numbers: https://en.wikipedia.org/wiki/Regular_number

from heapq import heappop, heappush, merge


# A traditional version to compute and return the n:th Hamming number.
# A priority queue is used to keep track of all the Hamming numbers
# we have discovered so far. The same numbers are also kept in a
# set to allow for a quick membership check that the priority queue
# cannot give us. Different data structures organize data in ways
# that make different operations fast.

def nth_hamming(n, muls=(2, 3, 5)):
    # A Python list can be used as a priority_queue by using only
    # the functions in heapq module to access it. These functions
    # maintain the priority queue "binary heap" order in the list.
    frontier_pq = [1]
    frontier_set = set(frontier_pq)
    while n > 0:
        curr = heappop(frontier_pq)
        frontier_set.remove(curr)
        for m in muls:
            if m * curr not in frontier_set:
                frontier_set.add(m * curr)
                heappush(frontier_pq, m * curr)
        n -= 1
    return curr

# Another (slow) version by combining lazy iterators recursively.

# Let through only one element of each run of consecutive values.
def iterator_uniq(it):
    prev = next(it)
    yield prev
    while True:
        curr = next(it)
        if curr != prev:
            yield curr
            prev = curr

# Hamming numbers can be produced by merging three streams of
# Hamming numbers with their values multiplied by 2, 3 and 5.
# However, this is not quite as efficient as the algorithm
# above implemented with a priority queue.

__iter_count = 0

def hamming_it():
    # To access a name outside the function, tell Python that
    # you mean to access the global name, not create a local.
    global __iter_count
    __iter_count += 1
    yield 1 # the "base case"
    yield from iterator_uniq(merge(
        (2*x for x in hamming_it()),
        (3*x for x in hamming_it()),
        (5*x for x in hamming_it())
    ))


if __name__ == "__main__":
    import itertools
    print(f"The millionth Hamming number is {nth_hamming(1000000)}.")
    n = 10
    print(f"Here are the first {n} Hamming numbers from iterators.")
    print(list(itertools.islice(hamming_it(), n)))
    print(f"That created {__iter_count} iterator objects. Whoa!")