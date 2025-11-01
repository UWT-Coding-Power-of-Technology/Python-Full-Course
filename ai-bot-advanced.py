print("🤖 Hello! I'm your friendly AI Chatbot!")

while True:
    print("\nChoose a topic:")
    print("1. Mood")
    print("2. Hobby")
    print("3. Favorite Food")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        mood = input("How are you feeling today? ").lower()
        if mood == "happy":
            print("That’s awesome! Keep smiling 😄")
        elif mood == "sad":
            print("Don’t worry, better days are coming 💙")
        else:
            print("I hope your day gets even better 🌟")

    elif choice == "2":
        hobby = input("What’s your favorite hobby? ").lower()
        print(f"Nice! {hobby.title()} sounds really fun! 🎨")

    elif choice == "3":
        food = input("What’s your favorite food? ").lower()
        print(f"Mmm, {food.title()} sounds delicious 😋")

    elif choice == "4":
        print("Goodbye! 👋 See you soon!")
        break

    else:
        print("Please choose a valid option (1-4).")
