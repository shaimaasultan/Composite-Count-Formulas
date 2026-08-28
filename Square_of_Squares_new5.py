from math import isqrt

def sq(m):
    if m <= 0: return None
    r = isqrt(m)
    return r if r*r == m else None

def reps(D):
    """All (u, v) with u^2 + v^2 = D, u < v."""
    out = []
    for u in range(1, isqrt(D // 2) + 1):
        v = sq(D - u*u)
        if v is not None and u < v:
            out.append((u, v))
    return out

def build(n, rep1, rep2):
    """Center n^2; rep1 on the main diagonal, rep2 on the anti-diagonal."""
    S, E = 3*n*n, n*n
    (u1, v1), (u2, v2) = rep1, rep2
    A, I = u1*u1, v1*v1
    C, G = u2*u2, v2*v2
    B  = S - A - C          # top middle
    H  = S - G - I          # bottom middle
    Dc = S - A - G          # left middle
    F  = S - C - I          # right middle
    return [A, B, C, Dc, E, F, G, H, I]

def report(n):
    R = reps(2*n*n)
    for i, r1 in enumerate(R):
        for r2 in R[i+1:]:
            cells = build(n, r1, r2)
            k = sum(1 for c in cells if c > 0)
            s = sum(1 for c in cells if sq(c) is not None)
            if k == 9:
                print(n, s, cells)

report(425)
