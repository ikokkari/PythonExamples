from random import Random

# Randomly choose k elements from given sequence. This algorithm
# proceeds in "online" fashion in that it looks each element of
# the sequence only once, and never again after that. The memory
# use is proportional only to the sample size k, and independent
# of the length of the sequence. It seems impossible to choose
# a fair random sample of some lazy sequence that has billions
# of elements in such small memory space, and yet here we are.

# Sequence can be either eager or lazy: since we only access it
# with for-loop, either way works, and we don't need anything else.


def reservoir(seq, k, rng=None, shuffle=True):
    # When using random numbers, hardcode the seed to make results reproducible.
    rng = Random(12345) if not rng else rng
    lounge = []
    for (count, v) in enumerate(seq):
        if count < k:  # First k elements build up the reservoir.
            lounge.append(v)
        else:
            idx = rng.randint(0, count)  # Others take a random shot.
            if idx < k:  # The new element hits the reservoir.
                lounge[idx] = v  # Displace a previous element.
    # Shuffle the buffer in place in the end.
    if shuffle:
        rng.shuffle(lounge)
    yield from lounge  # All done, so emit the reservoir.


# The shuffling step in the end can be removed if we don't care
# about the order of elements inside the sample, but only care about
# the subset of elements that were chosen to the sample.

def __demo():
    print("Here are 20 random non-short lines from 'War and Peace':")
    with open('warandpeace.txt', encoding='utf-8') as wap:
        for (idx, line) in enumerate(reservoir((line for line in wap if len(line) > 60), 20)):
            print(f"{idx:2}: {line}", end='')


if __name__ == "__main__":
    __demo()
