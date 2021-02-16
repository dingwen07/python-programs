#Python 3
#Find the number of "0"s at the end of the factorial of a number
def fun(n):
    if n < 5:
        return 0
    else:
        return int(n / 5 + fun(n / 5))


n = int(input("Input n:"))
print(n, "! 后0的数目为:", fun(n))
