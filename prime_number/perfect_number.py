#Python 3
#Find perfect numbers
import math
import is_prime
n = 1
while 1:
    n = n + 1
    if is_prime.is_prime(n):
        if is_prime.is_prime(2**n - 1):
            print(n)
