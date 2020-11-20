def func(Dnum, binary):
    if Dnum == 0:
        return Dnum, binary
    else:
        binary.append(str(Dnum % 2))
        return func(Dnum // 2, binary)


if __name__ == '__main__':
    Dnum = int(input('Decimal: '))
    b = []
    b = func(Dnum, b)[1]
    b.reverse()
    ans = ''
    for i in b:
        ans = ans + i
    print(ans)
