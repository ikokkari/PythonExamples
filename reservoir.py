from random import randint


# Randomly choose k elements from given iterable.

def reservoir(items, k):
    buffer = []
    for (count, v) in enumerate(items):
        if count < k:  # First k elements build up the reservoir.
            buffer.append(v)
        else:
            idx = randint(0, count)
            if idx < k:  # The new element hits the reservoir.
                buffer[idx] = v  # displace some previous element
        count += 1
    yield from buffer  # Emit the reservoir elements.


if __name__ == "__main__":
    print("Here are 20 random non-short lines from 'War and Peace':")
    with open('warandpeace.txt', encoding='utf-8') as wap:
        source = enumerate(reservoir((x.strip() for x in wap
                                      if len(x) > 60), 20))
        for (idx, line) in source:
            print(f"{idx:2}: {line}")
