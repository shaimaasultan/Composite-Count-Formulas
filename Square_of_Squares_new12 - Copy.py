from math import isqrt

def sq(m):
    """Return the root if m is a positive perfect square, else None."""
    if m <= 0:
        return None
    r = isqrt(m)
    return r if r * r == m else None

def near_misses(n, want=7):
    """Magic squares with center n^2, sum 3n^2, counting square entries."""
    out = []
    for a in range(1, n):
        A = a*a
        for b in range(1,  n):
            B = b*b
            C = 3*n - A - B #3n
            if sq(C) is None:
                continue
            G = A + B -n                   # anti-diagonal
            H = 2*n - n                    # middle column
            I = 2*n - A                    # main diagonal
            E = n
            D = 4*n - 2 * A - B                # left column
            F = 2*A + B - 2*n                   # middle row
            cells = [A, B, C, D, E, F, G, H, I]
            if min(cells) <= 0 or len(set(cells)) < 8:
                continue
            count = sum(1 for c in cells if sq(c) is not None)
            if count >= want:
                out.append((count, cells))
    return out

for n in range(1, 1000):
    for count, c in near_misses(n,7):
        print(f"n={n}  squares={count}")
        for i in range(0, 9, 3):
            print("   ", c[i:i+3])