import time
i = int(input('please enter an integer:'))
start = time.clock()
#创建一个空list
r = list()
#添加元素2
r.append(2)
#从3开始挨个筛选
for a in range(3, i):
    b = False
    #用a除以小于a的质数b
    for b in r:
        if a % b == 0:
            b = False
            break
        else:
            b = True
    if b == True:
        r.append(a)
print(r)
t = (time.clock() - start)
print(t)
