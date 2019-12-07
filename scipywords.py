import numpy as np
import random

# Demonstrate the scipy.sparse.csgraph graph algoritms package
# to solve some word problems that we have seen earlier. Adapted
# from the official scipy documentation.

# First, read in the wordlist and extract all 5-letter words.

n = 6
with open('words.txt', encoding="utf-8") as f:
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

from scipy.spatial.distance import pdist, squareform
hamming_dist = pdist(word_bytes, metric="hamming")

# Convert the words into sparse graphs.

from scipy.sparse import csr_matrix
graph_h = csr_matrix(squareform(hamming_dist < 1.5 / words.itemsize))

# This graph may be in separate components. Let's find out.

from scipy.sparse.csgraph import connected_components
N_h, components_h = connected_components(graph_h, directed=False)
print(f"The word graph is in {N_h} separate components.")
comps = [ words[components_h == i] for i in range(N_h) ]

# Compute the shortest distances between 'live' and 'dead'.
# Dijkstra's algorithm can do that for us.

from scipy.sparse.csgraph import dijkstra
def word_ladder(graph, start, ends):
    d, p = dijkstra(graph, indices=start, return_predecessors=True)
    print(f"Shortest paths from {words[start]!r} are:", flush=True)
    for end in ends:
        if d[end] != np.inf:            
            result = []
            i = end
            while i != start:
                result.append(words[i])
                i = p[i]
            result.append(words[start])
            print(f"To {words[end]}: {result[::-1]}")
        else:
            print(f"To {words[end]}: NO PATH FOUND.")        

# First, find the position indices of these words in wordlist.
start = words.searchsorted('hacker')
ends = [words.searchsorted(w) for w in random.sample(wordlist, 10)]

# Then print out the word ladders.
word_ladder(graph_h, start, ends)