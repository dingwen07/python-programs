#Python 3
#Find all prime numbers in a certain range

from math import sqrt
import time


def findPrime(n):
    result = list()
    result.append(2)
    result.append(3)
    for i in range(5, n + 1, 2):
        for j in range(2, int(sqrt(i)) + 2):
            #for j in range(2,(i>>4)+1):
            if i % j == 0:
                break
        else:
            result.append(i)

    return result


#start=time.clock()
print(findPrime(1000000))
#print(time.clock()-start)
