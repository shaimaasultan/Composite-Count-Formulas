def split_by_form(n, R=None):
    if R is None:
        R = []
    for d in (2, 3):
        if n % d == 0:
            R.append(d)
            return split_by_form(n // d, R)
    k = 1
    while True:
        for d in (6*k - 1, 6*k + 1):
            if d * d > n:
                R.append(n)          # n is prime
                return R
            if n % d == 0:
                R.append(d)
                return split_by_form(n // d, R)
        k += 1

def rep(n):
    if n <= 3:
        return str(n)
    parts = split_by_form(n)
    if len(parts) > 1:
        return "*".join(rep_prime(p) for p in parts)
    return rep_prime(n)

def rep_prime(p):
    """p is prime — no factoring here."""
    if p <= 3:
        return "("+str(p)+")"
    k, s = ((p+1)//6, "-") if (p+1) % 6 == 0 else ((p-1)//6, "+")
    core = "2*3" if k == 1 else f"2*3*{rep(k)}"
    return f"({core}{s}1)"

def is_Prime(N):
    if N < 2:
        return f"{N} is neither"
    forms   = rep(N) 
    if ")*(" in forms:
        return f"Not prime = {forms} = {N}"
  
    return f"prime = {forms} = {N}"

N= 91
print(rep(N))
print(split_by_form(N))
print(is_Prime(N))