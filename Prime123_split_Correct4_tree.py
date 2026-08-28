from math import isqrt

class Node:
    def __init__(self, op, kids=(), val=None):
        self.op, self.kids, self.val = op, list(kids), val

    def eval(self):
        if self.op == 'atom':  return self.val
        if self.op == '*':     
            p = 1
            for k in self.kids: p *= k.eval()
            return p
        if self.op == '+1':    return 6 * self.kids[0].eval() + 1
        if self.op == '-1':    return 6 * self.kids[0].eval() - 1

    def __str__(self):
        if self.op == 'atom':  return f"({self.val})"
        if self.op == '*':     return "*".join(str(k) for k in self.kids)
        inner = "*".join(str(k) for k in self.kids[0].factors())
        core = "2*3" if inner == "(1)" else f"2*3*{inner}"
        return f"({core}{self.op[0]}1)"

    def factors(self):
        return self.kids if self.op == '*' else [self]

def smallest_factor(n):
    for d in (2, 3):
        if n % d == 0:
            return d
    k = 1
    while True:
        for d in (6*k - 1, 6*k + 1):
            if d * d > n:
                return n
            if n % d == 0:
                return d
        k += 1

def build(n, factor=True):
    """Tree for n. factor=False gives the blind descent."""
    if n <= 3:
        return Node('atom', val=n)
    if factor:
        p = smallest_factor(n)
        if p != n:
            return flatten(Node('*', [build(p, True), build(n // p, True)]))
    else:
        for d in (2, 3):
            if n % d == 0:
                return flatten(Node('*', [Node('atom', val=d),
                                          build(n // d, False)]))
    if (n + 1) % 6 == 0:
        return Node('-1', [build((n + 1) // 6, factor)])
    return Node('+1', [build((n - 1) // 6, factor)])

def flatten(node):
    """Collapse nested products into one n-ary * node."""
    if node.op != '*':
        return node
    kids = []
    for k in node.kids:
        k = flatten(k)
        kids.extend(k.kids if k.op == '*' else [k])
    kids.sort(key=lambda k: k.eval())
    return kids[0] if len(kids) == 1 else Node('*', kids)

def canonicalise_cheap(node, peel=(2,3,5,7,11,13,17,19,23,29,31,37,41,43)):
    n = node.eval()
    if n <= 3:
        return Node('atom', val=n)
    r = isqrt(n)
    if r * r == n:                                  # perfect square
        h = canonicalise_cheap(build(r, False), peel)
        return flatten(Node('*', [h, h]))
    s = isqrt(n + 1)
    if s * s == n + 1 and n % 6 == 5:               # (s-1)(s+1)
        return flatten(Node('*', [canonicalise_cheap(build(s-1, False), peel),
                                  canonicalise_cheap(build(s+1, False), peel)]))
    for d in peel:
        if n != d and n % d == 0:
            return flatten(Node('*', [canonicalise_cheap(build(d, False), peel),
                                      canonicalise_cheap(build(n//d, False), peel)]))
    if (n + 1) % 6 == 0:
        return Node('-1', [canonicalise_cheap(build((n+1)//6, False), peel)])
    return Node('+1', [canonicalise_cheap(build((n-1)//6, False), peel)])

def canonicalise(node):
    """Rewrite any tree into canonical form: * at the root when composite."""
    return build(node.eval(), factor=True)

t = build(77, factor=False)
print(t)                    # blind descent, +1 at the root
print(canonicalise(t))      # (2*3-1)*(2*3-1)*(2*3-1)*(2*3*(2)-1)*(...)
print(canonicalise_cheap(t))