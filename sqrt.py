import time

from decimal import Decimal, localcontext
num = Decimal('1')
add = Decimal('0.5')
temp = Decimal('0')
with localcontext() as ctx:
    ctx.prec = 256
    while True:
        temp = num + add
        if temp**2 >= 2:
            add = add / 2
        else:
            if add <= Decimal('1E-' + str(ctx.prec - 1)):
                break
            num = num + add
print(num)
print()
print(time.process_time())
