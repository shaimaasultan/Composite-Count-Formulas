from collections import defaultdict
from math import isqrt

ALLOWED = {0,0, 5}

def sq(m):
    if m <= 0: return None
    r = isqrt(m)
    return r if r*r == m else None

def digit_ok(cells):
    return all(c % 10 in ALLOWED for c in cells)

def partners(A):
    out, n, d = [], A*A, 1
    while d*d < n:
        if n % d == 0:
            e = n // d
            if (d + e) % 2 == 0:
                B, C = (d + e)//2, (e - d)//2
                if C > 0: out.append((B, C))
        d += 1
    return out

def candidates(limit, min_pairs=2):
    idx = defaultdict(set)
    for leg in range(3 , isqrt(limit)):
        for B, C in partners(leg):
            if B <= limit:
                idx[B].add((abs(leg - C), leg + C))
    return {n: sorted(P) for n, P in idx.items() if len(P) >= min_pairs}

def run(limit, want=9, use_digits=True):
    for n, P in sorted(candidates(limit).items()):
        if use_digits and (n*n) % 10 not in ALLOWED:
            continue
        S, T, E = 3*n*n, 2*n*n, n*n
        orient = [p for q in P for p in (q, q[::-1])]
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

run(10000000000, 7,False)