decimal = int(input("Enter a decimal number: "))
binary = ""
num = decimal
while num > 0:
    remainder = num % 2
    binary = str(remainder) + binary
    num = num // 2
print("Binary of", decimal, "is:", binary)
