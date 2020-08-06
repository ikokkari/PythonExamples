from random import randint, shuffle


# Randomly choose k elements from given sequence. This algorithm
# proceeds in "online" fashion in that it looks each element of
# the sequence only once, and never again after that. The memory
# use is proportional only to the sample size k, and independent
# of the length of the sequence. It seems impossible to choose
# a fair random sample of some lazy sequence that has billions
# of elements in such small memory space, and yet here we are.

def reservoir(items, k):
    buffer = []
    for (count, v) in enumerate(items):
        if count < k:  # First k elements build up the reservoir.
            buffer.append(v)
        else:
            idx = randint(0, count)
            if idx < k:  # The new element hits the reservoir.
                buffer[idx] = v  # Displace a previous element.
        count += 1
    shuffle(buffer)  # Shuffle the buffer in place.
    yield from buffer  # All done, so emit the reservoir.

# The shuffling step in the end can be removed if we don't care
# about the order of elements in the sample, but just the subset
# of elements chosen to the sample.


if __name__ == "__main__":
    print("Here are 20 random non-short lines from 'War and Peace':")
    with open('warandpeace.txt', encoding='utf-8') as wap:
        source = enumerate(reservoir((x.strip() for x in wap
                                      if len(x) > 60), 20))
        for (idx, line) in source:
            print(f"{idx:2}: {line}")
