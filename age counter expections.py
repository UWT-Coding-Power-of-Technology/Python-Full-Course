try:
    age = int(input("Enter your age: "))
    print(f"Your age is {age}")

    if age % 2 == 0:
        print("Your age is even.")
    else:
        print("Your age is odd.")

except ValueError:
    print("Error: Please enter a valid whole number for age.")
