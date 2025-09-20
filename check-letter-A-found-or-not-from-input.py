a = input("Enter a word: ")
found = False 

for i in a:
    if i == 'A':  
        print("A is found")
        found = True
        break  
    
if not found:
    print("A not found")
