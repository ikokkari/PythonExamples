import random
from math import sqrt, floor

# Given current generation of solution candidates sorted in the order
# of increasing fitness, compute the next generation of candidates.

def compute_next_gen(current, fitness, combine, newsize=None, elitism=0):
    n = len(current)
    if not newsize:
        newsize = n
    # Initialize the result list to be filled in.
    next_gen = []
    # Best solutions get to the next generation automatically.    
    for i in range(elitism):
        next_gen.append(current[-i])
    while len(next_gen) < newsize:
        # Choose the parents to create two new offspring so that higher
        # fitness solutions have a higher chance of being chosen.
        i1 = int(floor(sqrt(random.randint(0, n * n - 1))))
        i2 = int(floor(sqrt(random.randint(0, n * n - 1))))
        # Create the offspring and add them to the next generation.
        (o1, o2) = combine(current[i1], current[i2])
        next_gen.append(o1)
        next_gen.append(o2)
    # Sort the next generation in order of increasing fitness.
    next_gen.sort(key=fitness)
    return next_gen

# One point crossover function to combine two solutions.

def one_point_crossover(s1, s2):
    i = random.randint(1, len(s1) - 1)
    return (s1[:i] + s2[i:], s2[:i] + s1[i:])

# Burst crossover, a better combinator for two solutions.
def burst_crossover(s1, s2, prob=10):
    r1, r2 = "", ""
    for i in range(len(s1)):
        r1 += s1[i]
        r2 += s2[i]
        if random.randint(0, 99) < prob:
            (s1, s2) = (s2, s1)
    return (r1, r2)

if __name__ == "__main__":
    # Make the randomness repeatable between runs. Change
    # the seed value to get a different random pattern.
    random.seed(8765)
    # Read in the wordlist.
    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [x.strip() for x in f if x.islower()]
    
    # We shall look for words of five letters.
    wordlist = [x for x in wordlist if len(x) == 5]
    # How many times each letter occurs in wordlist.    
    cfreq = [0 for i in range(26)]
    # Extract the bigrams, trigrams, quadgrams, and words.
    wordsets = [set(), set(), set(), set()]
    for word in wordlist:
        for c in word:
            cfreq[ord(c) - ord('a')] += 1
        wordsets[3].add(word) # word itself
        for i in range(0, 3):
            wordsets[0].add(word[i:i+2]) # bigrams
            if i < 3:
                wordsets[1].add(word[i:i+3]) # trigrams
            if i < 2:
                wordsets[2].add(word[i:i+4]) # quadgrams
    
    print(f"Weights are {cfreq} {len(cfreq)}.")
    
    chars = ['a','b','c','d','e','f','g','h','i','j','k',
             'l','m','n','o','p','q','r','s','t','u','v',
             'w','x','y','z']
    
    # Fitness function for a text string. We give points for
    # bigrams and trigrams so that the fitness landscape does
    # not consist of flat plateaus that the genetic algorithm
    # will just aimlessly mosey around.
    def word_count(text):
        count = 0
        for i in range(0, len(text) - 2):
            if text[i:i+2] in wordsets[0]: # bigrams
                count += 1
            if text[i:i+3] in wordsets[1]: # trigrams
                count += 100
            if text[i:i+4] in wordsets[2]: # quadgrams
                count += 10000
            if text[i:i+5] in wordsets[3]: # words
                count += 1000000
        return count

    # Create a random pattern of n characters.
    def create_pattern(n, forced=None, prob=50):
        pat = ""
        for i in range(n):
            if forced and forced[i] != '*':
                pat += forced[i]
            elif not forced and random.randint(0, 99) < prob:
                pat += '*'
            else:
                pat += random.choices(chars, weights = cfreq, k=1)[0]
        return pat
    
    # Find the best way to fill in the asterisks of the given
    # character pattern to maximize the number of words in it.
    pattern = create_pattern(50)
    print(f"Pattern: {pattern}.")
    sols = [create_pattern(50, forced = pattern) for i in range(3000)]
    sols.sort(key=word_count)
    
    for g in range(50):
        sols = compute_next_gen(sols, word_count, burst_crossover,
                                newsize = len(sols)-10, elitism=30)
        # Uncomment this to receive a status report after each gen.
        print(f"Gen {g}: {sols[-1]}, fitness {word_count(sols[-1])}.")
    
    best = sols[-1]
    print(f"The best solution found was {best}.")
    words = [best[i:i+5] for i in range(0, len(best) - 5)
            if best[i:i+5] in wordsets[3]]
    print(f"The solution contains {len(words)} words. They are:")
    print(words)