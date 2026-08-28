def factorize(n):
    fs, d = [], 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d); n //= d
        d += 1
    if n > 1: fs.append(n)
    return fs

def atom(p):
    """A single prime, written with 1,2,3."""
    if p <= 3:
        return str(p)
    if p % 6 == 1:
        k, sign = (p - 1) // 6, "+"
    else:
        k, sign = (p + 1) // 6, "-"
    if k == 1:
        return f"(2*3{sign}1)"
    return f"(2*3*{rep(k)}{sign}1)"

def rep(n):
    """Any n >= 1, written with 1,2,3."""
    if n == 1:
        return "1"
    return "*".join(atom(p) for p in factorize(n))

def is_prime_form(s):
    depth = 0
    for i, c in enumerate(s):
        if c == '(': depth += 1
        elif c == ')': depth -= 1
        elif c == '*' and depth == 0:
            return False
    return True

def factorize2(n):
    fs = []
    for d in (2, 3):
        while n % d == 0:
            fs.append(d); n //= d
    k = 1
    while True:
        for d in (6*k - 1, 6*k + 1):
            if d * d > n:
                if n > 1: fs.append(n)
                return fs
            while n % d == 0:
                fs.append(d); n //= d
        k += 1

def build(limit):
    spf = [0] * (limit + 1)          # smallest prime factor
    for d in range(2, int(limit**0.5) + 1):
        if spf[d] == 0:
            for m in range(d*d, limit + 1, d):
                if spf[m] == 0:
                    spf[m] = d

    def rep(n):
        if n <= 3:
            return str(n)
        p = spf[n]
        if p:                                    # composite
            return rep(p) + "*" + rep(n // p)
        k, s = ((n-1)//6, "+") if n % 6 == 1 else ((n+1)//6, "-")
        return f"(2*3*{rep(k)}{s}1)" if k > 1 else f"(2*3{s}1)"

    return rep

def rep2(n):
    if n <= 3:
        return str(n)
    for d in (2, 3):                      # x wasn't coprime to 6
        if n % d == 0:
            return f"{d}*{rep(n // d)}"
    x, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    core = "2*3" if x == 1 else f"2*3*{rep(x)}"
    return f"({core}{s}1)"


print(rep2(25))

