try:
    input_str = input("Enter two numbers, separated by a comma : ")
    num1, num2 = map(float, input_str.split(','))
    result = num1 / num2
    print("Result is", result)
    # using multiple except block for different type of error
except ZeroDivisionError:
    print("Division by zero is error !")
except ValueError:
    print("Invalid input. Please enter numbers separated by a comma like this: 1, 2")
except Exception as e:
    print("An error occurred:", e)

else:
    print("No exceptions")


finally:
    print("This will execute no matter what")
