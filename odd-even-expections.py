valid = False
while not valid:
    try:
        n = int(input("Enter a number: "))
        if n % 2 != 0:
            print("bye")
            valid = True
        else:
            print("Number must be odd.")
    except ValueError:
        print("Invalid input. Please enter a number.")
