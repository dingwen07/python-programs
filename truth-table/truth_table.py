import itertools
from logical_gates import *

# TEST
# ELEMENT_LIST = ['p', 'q']
# EXPRESSION = lambda p, q: NOT_GATE(p)
# EXPRESSION = lambda p, q: AND_GATE(p, q)
# EXPRESSION = lambda p, q: OR_GATE(p, q)
# EXPRESSION = lambda p, q: XOR_GATE(p, q)
# EXPRESSION = lambda p, q: IMPLY_GATE(p, q)
# EXPRESSION = lambda p, q: NOR_GATE(p, q)
# EXPRESSION = lambda p, q: XNOR_GATE(p, q)
# EXPRESSION = lambda p, q: NAND_GATE(p, q)

ELEMENT_LIST = ['p', 'q', 'r']
# EXPRESSION = lambda p, q, r: OR_GATE(p, q) # 1.1.1
# EXPRESSION = lambda p, q, r: NOT_GATE(p) # 1.1.2
# EXPRESSION = lambda p, q, r: OR_GATE(r, NOT_GATE(p)) # 1.1.3
EXPRESSION = lambda p, q, r: AND_GATE(OR_GATE(p, q), OR_GATE(r, NOT_GATE(p))) # 1.1.4
# EXPRESSION = lambda p, q, r: NOT_GATE(p) # 1.2.1
# EXPRESSION = lambda p, q, r: OR_GATE(p, NOT_GATE(p))  # 1.2.2
# EXPRESSION = lambda p, q, r: AND_GATE(q, r)  # 1.2.3
# EXPRESSION = lambda p, q, r: IMPLY_GATE(OR_GATE(p, NOT_GATE(p)), AND_GATE(q, r))  # 1.2.4

product_list = list(itertools.product((False, True), repeat=len(ELEMENT_LIST)))
permutation_list = []
for truth_list in product_list:
    i_list = []
    for i in range(0, len(ELEMENT_LIST)):
        i_list.append((ELEMENT_LIST[i], truth_list[i]))
    permutation_list.append(i_list)
# print(permutation_list)

for element in ELEMENT_LIST:
    print(element, end='\t')
print('RESULT')

for i in permutation_list:
    truth_list = []
    for element in ELEMENT_LIST:
        for e in i:
            if e[0] == element:
                truth_list.append(e[1])
                print_str = 'T' if e[1] else 'F'
                print(print_str, end='\t')
    print_str = 'T' if EXPRESSION(*truth_list) else 'F'
    print(print_str)
