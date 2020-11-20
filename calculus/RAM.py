from decimal import Decimal

func = lambda x : Decimal('6') / x
begin = Decimal('4')
end = Decimal('6')
nn = 100
n = Decimal(str(nn))
area = Decimal('0')
count = 0

x = begin
step = Decimal(str(( end - begin ) / n ))

while count < nn:
    x = x + step
    area = area + step * func(x)
    count = count + 1

print(area)
