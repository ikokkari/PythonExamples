import random

def hangman(wordlist, sep = '*'):
    misses, guesses = 0, []    
    word = random.choice(wordlist)
    letters = [ sep ] * len(word)
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

if __name__ == "__main__":
    with open('words_alpha.txt', encoding="utf-8") as f:
        wordlist = [word.strip() for word in f]
    print(f"Read a word list of {len(wordlist)} words." )
    while True:
        if hangman(wordlist) == -1:
            print("See you around!")
            break