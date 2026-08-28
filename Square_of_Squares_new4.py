from math import isqrt

def sq(m):
    """Root of m if m is a positive perfect square, else None."""
    if m <= 0:
        return None
    r = isqrt(m)
    return r if r * r == m else None

def center_pairs(n):
    """All (a, b) with a^2 + b^2 = 2n^2, a < b. Excludes the trivial (n, n)."""
    out = []
    D = 2 * n * n
    for a in range(1, n):
        b = sq(D - a * a)
        if b is not None:
            out.append((a, b))
    return out

from math import gcd
from functools import reduce

# def primitive(cells):
#     g = reduce(gcd, cells)
#     r = isqrt(g)
#     return  g == 1

def search(n, want=7):
    pairs = center_pairs(n)
    if not pairs:
        return []
    S, D = 3*n*n, 2*n*n
    E = n*n
    seen, out = set(), []

    for a, i in pairs:                    # main diagonal squares
        A, I = a*a, i*i
        for b in range(1, isqrt(2*n*n)):  # B square, top row
            B = b*b
            C = S - A - B
            if C <= 0:
                continue
            H = D - B
            G = S - C - E - 0 if False else D - C   # anti-diagonal partner
            Dc = S - A - G
            F = D - Dc
            cells = (A, B, C, Dc, E, F, G, H, I)
            #if not primitive(cells): continue
            if min(cells) <= 0 or len(set(cells)) != 9:
                continue
            count = sum(1 for x in cells if sq(x) is not None)
            if count >= want and cells not in seen:
                seen.add(cells)
                out.append((count, cells))
    return out

def search_fix(n, free_pair=(3, 8)):
    """Require every cell square EXCEPT the two at free_pair."""
    S, D, E = 3*n*n, 2*n*n, n*n
    out = []
    for a in range(1, isqrt(S)):
        A = a*a
        I = D - A
        if sq(I) is None: continue          # main diagonal both square
        for b in range(1, isqrt(D)):
            B = b*b
            H = D - B
            if sq(H) is None: continue      # middle column both square
            C = S - A - B
            if sq(C) is None: continue
            G = D - C
            if sq(G) is None: continue      # anti-diagonal both square
            Dc = S - A - G
            F = D - Dc
            cells = [A, B, C, Dc, E, F, G, H, I]
            if min(cells) <= 0 or len(set(cells)) != 9: continue
            n_sq = sum(1 for x in cells if sq(x) is not None)
            if n_sq >= 7:
                out.append((n_sq, cells))
    return out

for n in range(1, 65000):
    for count, c in search(n):
        print(f"n={n}  center={n*n}  squares={count}  sum={3*n*n}")
        for k in range(0, 9, 3):
            print("   ", c[k:k+3])