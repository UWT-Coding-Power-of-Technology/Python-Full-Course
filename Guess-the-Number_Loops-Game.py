import random

print("🎯 Welcome to the Guess the Number Game! 🎯")
print("I'm thinking of a number between 1 and 100...")

# Computer chooses a random number
secret_number = random.randint(1, 100)
attempts = 0

while True:
    guess = input("Enter your guess: ")

    if not guess.isdigit():
        print("❌ Please enter a valid number!")
        continue

    guess = int(guess)
    attempts += 1

    if guess < secret_number:
        print("📉 Too low! Try again.")
    elif guess > secret_number:
        print("📈 Too high! Try again.")
    else:
        print(f"🎉 Correct! You guessed it in {attempts} attempts!")
        break
