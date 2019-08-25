num = int(input("enter a number:"))

num = abs(num)
if num > 1:
    isPrime = True
    for i in range(2, num):
         if num % i == 0:
             isPrime = False
             break
    if isPrime:
        print(num, "is a prime")
    else:
        print(num, " is a composite")
else:
    print(num, "is considered neither")
