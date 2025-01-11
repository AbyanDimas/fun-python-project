import random

def hangman():
    words = ["python", "programming", "hangman", "developer", "github"]
    word = random.choice(words)
    guessed = ["_"] * len(word)
    attempts = 6

    print("Welcome to Hangman!")
    while attempts > 0 and "_" in guessed:
        print("Word:", " ".join(guessed))
        guess = input("Guess a letter: ").lower()

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed[i] = guess
        else:
            attempts -= 1
            print(f"Wrong! Attempts left: {attempts}")

    if "_" not in guessed:
        print(f"Congratulations! You guessed the word: {word}")
    else:
        print(f"Game Over! The word was: {word}")

hangman()

