import platform

if platform.machine().endswith('64'):
    size = 2**(8*4)
else:
    size = 2**(8*2)

size = 2**(8*2)

f = open('is_odd.c', 'w')
f.write('int is_odd(unsigned int i);\n\n')
f.write('int is_odd(unsigned int i) {\n')
for i in range(size):
    f.write('    if (i == {}u) return {};\n'.format(str(i), str(i%2)))
f.write('    return i % 2;\n')

f.write('}\n')
