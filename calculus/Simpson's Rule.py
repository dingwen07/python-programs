import math

func = lambda x: 3 * math.sqrt(x)
begin = 0
end = 1
n = 8

h = (end - begin) / n
i = begin
mult = True  # True ==> 4
count = 1

sum = func(i)
i = i + h

while count <= n - 1:
    if mult:
        sum = sum + 4 * func(i)
    else:
        sum = sum + 2 * func(i)
    mult = not mult
    i = i + h
    count = count + 1

sum = sum + func(end)
result = h / 3 * sum
print(result)
