import math

def split_by_form(n):
    if n % 6 == 1:
        r = math.isqrt(n)
        if r * r == n:
            return [r, r]                # 25, 49, 121, 169...
        else:
            A = int((n +1)/6)
            fact = 1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , int(n/i)]
           
    elif n % 6 == 5:
        s = math.isqrt(n + 1)
        if s * s == n + 1:
            print(s-1, s+1)
            return [s - 1, s + 1]        # 35, 143, 323, 899...
        else:
            A = int((n -1)/6)
            fact = 1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , int(n/i)]
    return None

def rep(n):
    if n <= 3:
        return str(n)
    for d in (2, 3):                     # peel 2s and 3s first
        if n % d == 0:
            return f"{d}*{rep(n // d)}"
    pair = split_by_form(n)
    if pair:
        a, b = pair
        return f"{rep(a)}*{rep(b)}"
    k, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    core = "2*3" if k == 1 else f"2*3*{rep(k)}"
    return f"({core}{s}1)"



def sign_counts(s):
    plus = minus = 0
    i = 0
    while i < len(s) - 1:
        if s[i] in '+-' and s[i+1] == '1' and (i+2 >= len(s) or not s[i+2].isdigit()):
            if s[i] == '+': plus += 1
            else: minus += 1
        i += 1
    return plus, minus
N = 412637
N= 155
def is_prime(N):
    is_prime = False
    if N % 2 == 0 or N%3 ==0: 
        print(f"NOT Prime = {rep(N)} = {N}")
        return

    pair = split_by_form(N)
    if pair:
        a, b = pair
        print(f"Not Prime = ({rep(a)}*{rep(b)}) = {a * b}")
        return

    plus , minus = sign_counts(rep(N))
    print((+1) * plus + (-1) *minus)
    if (+1) * plus + (-1) *minus == 0:
        print(f"Prime = {rep(N)} = {N}")
    else:
        print(f"NOT Prime  = {rep(N)} = {N}")


def inner_groups(s):
    """All parenthesized groups, as (depth, substring)."""
    out, stack = [], []
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            start = stack.pop()
            out.append((len(stack), s[start:i+1]))
    return out

def innermost(s):
    """The deepest group — no parens inside it."""
    groups = inner_groups(s)
    return max(groups, key=lambda g: g[0])[1]

def chain_values(s):
    return sorted({parse(g) for _, g in inner_groups(s)})

def parse(s):
    s = s.replace(' ', '').replace('×', '')
    pos = 0

    def expr():
        nonlocal pos
        v = term()
        while pos < len(s) and s[pos] in '+-':
            op = s[pos]; pos += 1
            t = term()
            v = v + t if op == '+' else v - t
        return v

    def term():
        nonlocal pos
        v = atom()
        while pos < len(s) and s[pos] == '*':
            pos += 1
            v *= atom()
        return v

    def atom():
        nonlocal pos
        if s[pos] == '(':
            pos += 1
            v = expr()
            pos += 1          # skip ')'
            return v
        d = ''
        while pos < len(s) and s[pos].isdigit():
            d += s[pos]; pos += 1
        return int(d)

    return expr()




is_prime(N)
split_by_form(N)


