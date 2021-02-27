
def NOT_GATE(p:bool) -> bool:
    return not(p)

def AND_GATE(p:bool, q:bool) -> bool:
    return p and q

def OR_GATE(p:bool, q:bool) -> bool:
    return p or q

def XOR_GATE(p:bool, q:bool) -> bool:
    return (p != q)

def IMPLY_GATE(p:bool, q:bool) -> bool:
    return OR_GATE(NOT_GATE(p), q)

def NOR_GATE(p:bool, q:bool) -> bool:
    return NOT_GATE(OR_GATE(p, q))

def XNOR_GATE(p:bool, q:bool) -> bool:
    return (p == q)

def NAND_GATE(p:bool, q:bool) -> bool:
    return NOT_GATE(AND_GATE(p ,q))
