from heapq import heappop, heappush

# A traditional version to compute and return the n:th Hamming number.

def nth_hamming(n):
    muls = (2, 3, 5)
    frontier_pq = [1]
    frontier_set = set()
    frontier_set.add(1)
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

# Merge the results of two sorted iterators into sorted sequence.
# For simplicity, this assumes that both iterators are infinite.
def iterator_merge(i1, i2):
    v1 = next(i1)
    v2 = next(i2)
    while True:
        if v1 <= v2:
            yield v1
            v1 = next(i1)
        else:
            yield v2
            v2 = next(i2)

# Let through only one element of each run of consecutive values.
def iterator_uniq(i):
    v = next(i)
    yield v
    while True:
        while True:
            v2 = next(i)
            if v != v2: break
        v = v2
        yield v

# Hamming numbers can be produced by merging three streams of
# Hamming numbers with their values multiplied by 2, 3 and 5.
def hamming_it():
    yield 1
    i = iterator_uniq(iterator_merge(
        (2*x for x in hamming_it()),
        iterator_merge(
            (3*x for x in hamming_it()),
            (5*x for x in hamming_it())
            )
        ))
    for x in i:
        yield x

if __name__ == "__main__":
    import itertools
    print(f"The millionth Hamming numbers is {nth_hamming(1000000)}.")
    print("Here are the first 100 Hamming numbers with iterators.")
    print(list(itertools.islice(hamming_it(), 100)))
