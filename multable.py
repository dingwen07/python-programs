#Python 3
#Print a multiplication table

for row in range(1, 10):
    out = ""
    for column in range(1, 10):
        if column >= row + 1 and row != 1:
            break
        if row * column >= 10:
            sp = ""
        else:
            sp = " "
        out = out + sp + repr(row * column) + " "
    print(out)
