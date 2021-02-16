#Python 3
#Find perfect numbers
import math
import isPrime
n = 1
while 1:
    n = n + 1
    if isPrime.isPrime(n):
        if isPrime.isPrime(2**n - 1):
            print(n)
