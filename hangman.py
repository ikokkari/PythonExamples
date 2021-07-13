import random


def hangman(wordlist, blank='*'):
    misses, guesses = 0, []
    secret = random.choice(wordlist)
    displayed = [blank for _ in secret]
    print("Let us play a game of Hangman.")
    while blank in displayed:
        print(f"Current word is {'-'.join(displayed)}.")
        print(f"Letters guessed so far: {''.join(guesses)}")
        guess = input("Please enter a letter, or 'quit' to quit: ")
        if guess == 'quit':
            return None
        if guess not in guesses:
            guesses.append(guess)
            guesses.sort()
        hit = 0
        for (i, (c1, c2)) in enumerate(zip(displayed, secret)):
            if c1 == blank and c2 == guess:
                displayed[i] = guess
                hit += 1
        if hit > 0:
            print(f"That one hit {hit} time{'s' if hit > 1 else ''}!")
        else:
            print("That one was a miss.")
            misses += 1
    print(f"You guessed {secret!r} with {misses} misses.\n")
    return misses


def __demo():
    with open('words_sorted.txt', encoding="utf-8") as f:
        wordlist = [word.strip() for word in f if len(word) > 5]
    print(f"Read a word list of {len(wordlist)} words.")
    while True:
        if hangman(wordlist) is None:
            print("See you around!")
            break


if __name__ == "__main__":
    __demo()
