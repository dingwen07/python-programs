import itertools
from typing import Callable, Iterable, NoReturn

def truth_table(prop_symbols: Iterable[str], expressions: Iterable[Callable[..., bool]]) -> int:
    err = 0
    for symbol in prop_symbols:
        print(symbol, end='\t')
    for i in range(1, len(expressions) + 1):
        print('EXP{}'.format(str(i)), end='\t')
    print()

    product_list = list(itertools.product((False, True), repeat=len(prop_symbols)))
    product_list.sort(reverse=False)
    truth_count = [0] * len(expressions)
    for truth_list in product_list:
        for i in truth_list:
            print_str = 'T' if i else 'F'
            print(print_str, end='\t')
        for j in range(0, len(expressions)):
            expression = expressions[j]
            try:
                if expression(*truth_list):
                    print_str = 'T'
                    truth_count[j] = truth_count[j] + 1
                else:
                    print_str = 'F'
            except TypeError:
                print_str = 'E'
                err = 1
            except Exception:
                print_str = 'E'
                err = 2
            print(print_str, end='\t')
        print()
    for symbol in prop_symbols:
        print('X', end='\t')
    for i in truth_count:
        print(str(i), end='\t')
    print()
    return err

if __name__ == '__main__':
    from logical_gates import *

    # TEST
    prop_symbols_t = ('p', 'q')
    EXPRESSION1 = lambda p, q: NOT_GATE(p) # MUST take len(prop_symbols) parameter(s)
    EXPRESSION2 = lambda p, q: AND_GATE(p, q)
    EXPRESSION3 = lambda p, q: OR_GATE(p, q)
    EXPRESSION4 = lambda p, q: XOR_GATE(p, q)
    EXPRESSION5 = lambda p, q: IMPLY_GATE(p, q)
    EXPRESSION6 = lambda p, q: NOR_GATE(p, q)
    EXPRESSION7 = lambda p, q: XNOR_GATE(p, q)
    EXPRESSION8 = lambda p, q: NAND_GATE(p, q)
    expressions = (EXPRESSION1, EXPRESSION2, EXPRESSION3, EXPRESSION4, EXPRESSION5, EXPRESSION6, EXPRESSION7, EXPRESSION8)
    print(truth_table(prop_symbols_t, expressions))

    prop_symbols_ab = ('p', 'q', 'r')
    EXPRESSION_a1 = lambda p, q, r: OR_GATE(p, q) # 1.a.1
    EXPRESSION_a2 = lambda p, q, r: NOT_GATE(p) # 1.a.2
    EXPRESSION_a3 = lambda p, q, r: OR_GATE(r, NOT_GATE(p)) # 1.a.3
    EXPRESSION_a4 = lambda p, q, r: AND_GATE(OR_GATE(p, q), OR_GATE(r, NOT_GATE(p))) # 1.a.4
    expressions_a = (EXPRESSION_a1, EXPRESSION_a2, EXPRESSION_a3, EXPRESSION_a4)
    EXPRESSION_b1 = lambda p, q, r: NOT_GATE(p) # 1.b.1
    EXPRESSION_b2 = lambda p, q, r: OR_GATE(p, NOT_GATE(p))  # 1.b.2
    EXPRESSION_b3 = lambda p, q, r: AND_GATE(q, r)  # 1.b.3
    EXPRESSION_b4 = lambda p, q, r: IMPLY_GATE(OR_GATE(p, NOT_GATE(p)), AND_GATE(q, r))  # 1.b.4
    expressions_b = (EXPRESSION_b1, EXPRESSION_b2, EXPRESSION_b3, EXPRESSION_b4)

    truth_table(prop_symbols_ab, expressions_a)
    print()
    truth_table(prop_symbols_ab, expressions_b)

