from math import isqrt

def sq(m):
    """Return the root if m is a positive perfect square, else None."""
    if m <= 0:
        return None
    r = isqrt(m)
    return r if r * r == m else None

def near_misses(n, want=7):
    """Magic squares with center n^2, sum 3n^2, counting square entries."""
    S, D2 = 3*n*n, 2*n*n
    out = []
    for a in range(1, isqrt(S) + n):
        A = a*a
        for b in range(1, isqrt(S - A) + n):
            B = b*b
            C = S - A - B
            if sq(C) is None:
                continue
            G = D2 - C                    # anti-diagonal
            H = D2 - B                    # middle column
            I = D2 - A                    # main diagonal
            E = n*n
            Dc = S - A - G                # left column
            F = D2 - Dc                   # middle row
            cells = [A, B, C, Dc, E, F, G, H, I]
            if min(cells) <= 0 or len(set(cells)) != 9:
                continue
            count = sum(1 for c in cells if sq(c) is not None)
            if count >= want:
                out.append((count, cells))
    return out

for n in range(1, 600):
    for count, c in near_misses(n):
        print(f"n={n}  squares={count}")
        for i in range(0, 9, 3):
            print("   ", c[i:i+3])