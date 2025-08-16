lower = input("Enter lower range: ")
upper = input("Enter upper range: ")

print("Prime numbers between", lower, "and", upper, "are:")


for num in range(int(lower), int(upper) + 1):
   if num > 1: 
       for i in range(2, num):
            if (num % i) == 0:
                break

       else:
           print(num)

