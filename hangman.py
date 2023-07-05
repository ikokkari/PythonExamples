from random import Random


def hangman(secret, blank='*'):
    misses, guessed = 0, []
    board = [blank for _ in secret]
    print("All righty, let us play a game of Hangman.")
    while blank in board:
        print(f"Current word is {'-'.join(board)}.")
        print(f"Letters guessed so far: {''.join(guessed)}")
        guess = input("Please enter a letter, or 'quit' to quit: ")
        if guess == 'quit':
            return None
        if guess not in guessed:
            guessed.append(guess)
            guessed.sort()
        hit = 0
        for (pos, (board_char, secret_char)) in enumerate(zip(board, secret)):
            if board_char == blank and secret_char == guess:
                board[pos] = guess
                hit += 1
        if hit > 0:
            print(f"That one hit {hit} {'times' if hit > 1 else 'time'}!")
        else:
            print("That one was a miss.")
            misses += 1
    print(f"You guessed {secret!r} with {misses} misses.\n")
    return misses


def __demo():
    # The text file words_sorted.txt contains one word per line.
    with open('words_sorted.txt', encoding="utf-8") as word_file:
        wordlist = [line.strip() for line in word_file if len(line) > 5]
    print(f"Finished reading a word list of {len(wordlist)} words.")
    rng = Random()  # RNG seed is taken from system clock, different each run
    while True:
        if hangman(rng.choice(wordlist)) is None:
            print("See you around!")
            break


if __name__ == "__main__":
    __demo()
