
def parse(s):
    """Evaluate an expression over {1,2,3}, *, +, -, ^, and parentheses."""
    s = s.replace(' ', '').replace('×', '')
    s = s.replace(')(', ')*(')
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
        v = power()
        while pos < len(s) and s[pos] == '*':
            pos += 1
            v *= power()
        return v

    def power():
        nonlocal pos
        v = atom()
        if pos < len(s) and s[pos] == '^':
            pos += 1
            v **= power()
        return v

    def atom():
        nonlocal pos
        if s[pos] == '-':
            pos += 1
            return -atom()
        if s[pos] == '(':
            pos += 1
            v = expr()
            pos += 1
            return v
        d = ''
        while pos < len(s) and s[pos].isdigit():
            d += s[pos]; pos += 1
        return int(d)

    return expr()


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

def rep(n):
    if n <= 3:
        return "(" + str(n) + ")"
    k, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    p = smallest_factor(n)
    if p != n:
        return rep(n//p) + "*" + rep(p)
    
    core = "2*3" if k == 1 else f"2*3*{rep(k)}"
    return f"({core}{s}1)"

def rep_fast(n):
    if n <= 3:
        return  str(n) 
    for d in (2 ,3):
        if n % d == 0:
            #return rep_fast(d)+"*" + rep_fast(n//d)
            #return f"{d}*" + rep_fast(n //d)
            return rep_fast(n//d)+"*" + rep_fast(d)
    k, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    core = "2*3" if k == 1 else f"2*3*{rep_fast(k)}"
    return f"({core}{s}1)"

def is_Prime(N):
    if N < 2:
        return f"{N} is neither"
    forms   = rep(N) 
    if ")*(" in forms:
        return f"Not prime = {forms} = {N}"
  
    return f"prime = {forms} = {N}"

N= 4126371
N=143
N= 41263751419195237937917
N = 341022739001613536677 
Canonical = rep(N) 
Non_Canonical = rep_fast(N)
print("canonical Form =" , Canonical , parse(Canonical))
print("non canonical form =" , Non_Canonical , parse(Non_Canonical))
print(is_Prime(N))
print(smallest_factor(N))
#print(rep(4126375))
# (2)... no — (2*3-1)*(2*3-1)*(2*3-1)*(2*3*2-1)*(2*3*2*2*(2*3-1)*(2*3-1)*(2*3-1)+1)


