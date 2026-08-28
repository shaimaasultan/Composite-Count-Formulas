from collections import defaultdict
from math import sqrt , pi
import math

ALLOWED = {1, 5,9}

def sq(m):
    if m <= 0: return None
    m = int(m/5)
    r = sqrt(m)
    return r if (r)*(r) == (m) else None

def digit_ok(cells):
    return all(c % 10 in ALLOWED for c in cells)

def partners(A):
    out, n = [], A*A
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            e = n // d
            if d < e and (d + e) % 2 == 0:
                out.append(((d + e)//2, (e - d)//2))
    return out

from math import gcd

def candidates(limit, min_pairs=3):
    idx = defaultdict(set)
    m = 2
    while m*m <= limit:
        for k in range(1, m):
            if (m - k) % 2 and gcd(m, k) == 1:
                p, q, h = m*m - k*k, 2*m*k, m*m + k*k
                s = 1
                while s*h <= limit:
                    idx[s*h].add((s*abs(p - q), s*(p + q)))
                    s += 1
        m += 1
    return {n: sorted(P) for n, P in idx.items() if len(P) >= min_pairs}

def run(limit, want=9, use_digits=True):
    for n, P in sorted(candidates(limit,4).items()):
        if use_digits and (n*n) % 10 not in ALLOWED:
            continue
        S, T, E = 3*n*n, 2*n*n, 1*n*n
        orient = [p for q in P for p in (q, q[::-1])]
        print(orient)
        for a, i in orient:
            A, I = a*a, i*i
            if use_digits and (A % 10 not in ALLOWED or I % 10 not in ALLOWED):
                continue
            for b, h in orient:
                B, H = b*b, h*h
                C  = S - A - B
                G  = T - C
                Dc = S - A - G
                F  = T - Dc
                cells = [A, B, C, Dc, E, F, G, H, I]
                if min(cells) <= 0 or len(set(cells)) != 9:
                    continue
                if use_digits and not digit_ok(cells):
                    continue
                k = sum(1 for x in cells if sq(x) is not None)
                if k >= want:
                    print(n, k, cells)

run(1000, 9,False)