def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_palindrome(n):
    return str(n) == str(n)[::-1]


print("Prime Palindrome numbers between 1 and 3000:")

for num in range(1, 3001):
    if is_prime(num) and is_palindrome(num):
        print(num)
