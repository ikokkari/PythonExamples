import random


def hangman(wordlist, blank='*'):
    misses, guesses = 0, []
    word = random.choice(wordlist)
    letters = [blank] * len(word)
    print("Let us play a game of Hangman.")
    while blank in letters:
        print(f"Current word is {'-'.join(letters)}.")
        print(f"Letters guessed so far: {''.join(guesses)}")
        guess = input("Please enter a letter, or 'quit' to quit: ")
        if guess == 'quit':
            return None
        if guess not in guesses:
            guesses.append(guess)
            guesses.sort()
        hit = 0
        for (i, (let, w)) in enumerate(zip(letters, word)):
            if let == blank and w == guess:
                letters[i] = guess
                hit += 1
        if hit > 0:
            print(f"That one hit {hit} time{'s' if hit > 1 else ''}!")
        else:
            print("That one was a miss.")
            misses += 1
    print(f"You guessed {word!r} with {misses} misses.\n")
    return misses


if __name__ == "__main__":
    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [word.strip() for word in f]
    print(f"Read a word list of {len(wordlist)} words.")
    while True:
        if hangman(wordlist) is None:
            print("See you around!")
            break
