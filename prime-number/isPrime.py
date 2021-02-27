#Python 3
#Verify if a number is a prime number

#from isPrime.py import isPrime
from itertools import count
import math


def isPrime(n):
    if n > 1:
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(n) + 1), 2):
            if n % current == 0:
                return False
        return True
    return False


"""
def isPrime(n):
    if n <= 1:
        return False
    i = 2
    while i < n:
        if n % i == 0:
            return False
        i = i + 1
    return True
"""
"""
def isPrime(n):
    if n < 2:  return []
    if n == 2: return [2]
    s = range(3, n, 2)
    mroot = n ** 0.5
    half = len(s)
    i = 0
    m = 3
    while m <= mroot:
        if s[i]:
            j = (m * m - 3)//2
            s[j] = 0
            while j < half:
                s[j] = 0
                j += m
    i = i + 1
    m = 2 * i + 3
    return [2]+[x for x in s if x]
"""

if __name__ == "__main__":
    print(isPrime(input('Input a number')))
