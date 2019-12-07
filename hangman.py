import random

def hangman(wordlist, sep = '*'):
    misses = 0
    guesses = []    
    word = random.choice(wordlist)
    letters = [ sep for x in range(len(word)) ]
    print("Let us play a game of Hangman.")
    while sep in letters:
        print(f"Current word is {'-'.join(letters)}.")
        print(f"Letters guessed so far: {''.join(guesses)}")
        guess = input("Please enter a letter, or 'quit' to quit: ")
        if guess == 'quit':
            return -1
        if guess not in guesses:
            guesses.append(guess)
            guesses.sort()
        hit = 0
        for i in range(len(word)):
            if letters[i] == sep and word[i] == guess:
                letters[i] = guess
                hit += 1
        if hit > 0:
            print(f"That one hit {hit} times!")
        else:
            print("That one was a miss.")
            misses += 1            
    print(f"You guessed {word!r} with {misses} misses.\n")
    return misses

def only_letters(word):
    for x in word:
        if x not in "abcdefghijklmnopqrstuvwxyz":
            return False
    return True

if __name__ == "__main__":
    with open('words.txt', encoding="utf-8") as f:
        wordlist = [x.strip() for x in f]
    print(f"Read a word list of {len(wordlist)} words." )
    wordlist = [x for x in wordlist if only_letters(x)]
    print(f"After cleanup, the list has {len(wordlist)} words.")
    while True:
        if hangman(wordlist) == -1:
            print("See you around!")
            break