import numpy as np
import random
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.csgraph import dijkstra

# Demonstrate the scipy.sparse.csgraph graph algorithms package
# to solve some word problems that we have seen earlier. Adapted
# from the official scipy documentation.

# The length of words that we care about, and the start word.

n, start_word = 5, 'cares'

# First, read in the wordlist and extract all 5-letter words.

with open('words_sorted.txt', encoding="utf-8") as f:
    wordlist = [x.strip() for x in f if x.islower()]
print(f"Read in a word list of {len(wordlist)} words.")
wordlist = sorted([x for x in wordlist if len(x) == n])
print(f"There remain {len(wordlist)} words of length {n}.")

# Convert list of words to numpy array.

words = np.asarray(wordlist)
print(f"The numpy array has the shape {words.shape}.")

# Convert that numpy array to matrix of Unicode characters.

word_bytes = np.ndarray((words.size, words.itemsize),
                        dtype='int8',
                        buffer=words.data)
print(f"Unicode matrix has the shape {word_bytes.shape}.")

# Compute the distance between each pair of words. You can also
# try the Euclidean distance instead of Hamming distance.

hamming_dist = pdist(word_bytes, metric="hamming")

# Convert the words numpy array into a sparse graph.

graph_h = csr_matrix(squareform(hamming_dist < 1.5 / words.itemsize))

# This graph will be broken into separate components.

N_h, components_h = connected_components(graph_h, directed=False)

print(f"The word graph is in {N_h} separate components.")

comps = [words[components_h == i] for i in range(N_h)]

singletons = [comp for comp in comps if len(comp) == 1]

print(f"Of those, {len(singletons)} are singleton components.")

sing_sample = random.sample(singletons, 50)
sing_sample = sorted([str(w[0]) for w in sing_sample])

print(f"Some of them are {', '.join(sing_sample)}.")


# Let's compute the shortest distances from the given start word to
# our chosen goal words. Dijkstra's algorithm will do that for us.

def word_ladder(graph, start, goals):
    d, p = dijkstra(graph, indices=start, return_predecessors=True)
    # d[i] is the distance from start to word i.
    # p[i] is the parent waypoint from word i to start.
    print(f"Shortest paths from {words[start]!r} are:", flush=True)
    for goal in goals:
        if d[goal] < np.inf:  # Reachable words are at finite distance.
            result, i = [], goal
            while i != start:  # Track the shortest path backwards.
                result.append(words[i])
                i = p[i]
            result.append(words[start])  # All roads lead to Rome.
            result.reverse()
            print(f"To {words[goal]}: {' -> '.join(result)}")
        else:
            print(f"To {words[goal]}: NO PATH FOUND.")


# First, find the position indices of these words in wordlist.

start = words.searchsorted(start_word)
ends = [words.searchsorted(w) for w in random.sample(wordlist, 10)]

# Then print out the word ladders.

word_ladder(graph_h, start, ends)