from math import isqrt

def partners(D):
    """{a: b} for every a^2 + b^2 = D."""
    out = {}
    for a in range(1, isqrt(D) + 1):
        b2 = D - a*a
        b = isqrt(b2)
        if b and b*b == b2:
            out[a] = b
    return out

def search(n):
    D, S = 2*n*n, 3*n*n
    part = partners(D)
    found = []
    for p, w in part.items():
        for q, v in part.items():
            r2 = S - p*p - q*q                  # top row
            if r2 <= 0: continue
            r = isqrt(r2)
            if r*r != r2 or r not in part: continue
            u = part[r]
            s2 = S - p*p - u*u                  # left column
            if s2 <= 0: continue
            s = isqrt(s2)
            if s*s != s2 or s not in part: continue
            t = part[s]
            cells = [p, q, r, s, n, t, u, v, w]
            if len(set(cells)) ==9:
                found.append(cells)
    return found

for n in range(1, 200):
    for c in search(n):
        print(n, [x*x for x in c])