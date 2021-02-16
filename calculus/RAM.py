from decimal import Decimal

func = lambda x : Decimal('6') / x
func = lambda x : Decimal('36') - x ** 2
begin = Decimal('0')
end = Decimal('6')
num = 4

i = Decimal(str(num))
left_area = Decimal('0')
mid_area = Decimal('0')
right_area = Decimal('0')
count = 0

x = begin
step = Decimal(str(( end - begin ) / i ))

while count < num:
    left_area = left_area + step * func(x)
    mid_area = mid_area + step * func(x + step / 2)
    x = x + step
    right_area = right_area + step * func(x)
    count = count + 1

print('Riemann Sum')
print('Left: ' + str(left_area))
print('Right: ' + str(right_area))
print('Mid-point: ' + str(mid_area))
