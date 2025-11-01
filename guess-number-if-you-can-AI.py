print("Think of a number between 1 and 100.")
input("Press Enter when ready...")

low = 1
high = 100

while True:
    guess = (low + high) // 2
    print("My guess is:", guess)
    reply = input("Is it (H)igh, (L)ow, or (C)orrect? ").lower()

    if reply == "c":
        print("Yay! I guessed it! 🎉")
        break
    elif reply == "h":
        high = guess - 1
    elif reply == "l":
        low = guess + 1
    else:
        print("Please type H, L, or C only.")
