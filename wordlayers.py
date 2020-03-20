# Inspired by the work of Donald Knuth in "Stanford Graphbase".

# Compute the Hamming distance between two words of same length.
# That is, the number of positions in which the words have a
# different character. In the word graph, we consider two words
# to be neighbours if their Hamming distance equals one.

def hamming_distance(w1, w2):
    return sum(int(c1 != c2) for (c1, c2) in zip(w1, w2))

# Compute the word layers from the given starting word using the
# breadth first search algorithm.

def word_layers(start, neighbours):
    # The zeroth layer contains only the starting word.
    result = [[start]]
    # All words that have been discovered so far.
    discovered = set()
    # The words of the previous layer.
    frontier = [start]
    discovered.add(start)
    # Generate all word layers up to maxd level, or as long
    # as the current layer has even one word in it.
    while len(frontier) > 0:
        # The next layer that we build up this round.
        nextl = []
        # The next layer contains all undiscovered neighbours
        # of all the words of the current layer.
        for w in frontier:
            for w2 in neighbours[w]:
                if w2 not in discovered:
                    nextl.append(w2)
                    discovered.add(w2)
        # Add the completed word layer to the result list.
        result.append(nextl)
        # This layer becomes the frontier for the next round.
        frontier = nextl
    return result

if __name__ == "__main__":
    from random import sample
    from itertools import combinations
    # The length of the words that we consider.
    n = 4
    with open('words_alpha.txt', encoding="utf-8") as f:
        wordlist = [x.strip() for x in f]
    print(f"Read in a word list of {len(wordlist)} lowercase words.")
    wordlist = [x for x in wordlist if len(x) == n]
    print(f"There remain {len(wordlist)} words of length {n}.")
    
    print("Building the neighbourhood graph, please wait...", flush = True)
    # Dictionary that maps each word to list of its neighbours.
    neighbours = { w:[] for w in wordlist }
    # Loop through all pairs of words, looking for neighbours.
    # This will take a while.
    for (w1, w2) in combinations(wordlist, 2):
        if hamming_distance(w1, w2) == 1:                
            neighbours[w1] = neighbours[w1] + [w2]
            neighbours[w2] = neighbours[w2] + [w1]
    print("Thank you for waiting. Graph is now fully constructed.")
    
    singletons = [x for x in wordlist if neighbours[x] == []]
    print(f"There are {len(singletons)} singleton words in the dictionary:")
    print("Here is a random sample of 50 such singletons.")
    print(sample(singletons, 50))
    
    # Compute the total number of neighbours, and find the word
    # that has the largest number of neighbours.
    mw, total = 0, 0
    for word in wordlist:
        total += len(neighbours[word])
        if len(neighbours[word]) > mw:
            mw, mword = len(neighbours[word]), word            
    print(f"Average number of neighbours is {total / len(wordlist):.2f}.")
    print(f"The word with largest number of neighbours is {mword!r}.")
    print(f"It is directly connected to {', '.join(neighbours[mword])}.")
    print(f"Constructing the word layers starting from {mword!r}.")
    wl = word_layers(mword, neighbours)
    total = 0
    print(f"Word layers starting from {mword!r} have sizes:")
    for i in range(1, len(wl) - 1):
        print(f"Level {i} contains {len(wl[i])} words.", end = " ")
        print(f"Some are: {', '.join(sample(wl[i], min(5, len(wl[i]))))}.")
        total += len(wl[i])
    print(f"A total of {total} words are reachable from {mword!r}.")