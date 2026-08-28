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

def search(n, want=7):
    """Magic squares with center n^2 and sum 3n^2; report those with >= want squares."""
    pairs = center_pairs(n)
    if len(pairs) < 2:
        return []
    S = 3 * n * n
    D = 2 * n * n
    results = []

    for a, i in pairs:                       # main diagonal: A .. I
        for c, g in pairs:                   # anti-diagonal: C .. G
            if (a, i) == (c, g):
                continue
            A, I, C, G = a*a, i*i, c*c, g*g
            B = S - A - C                    # top row
            if B <= 0:
                continue
            H = D - B                        # middle column
            Dc = S - A - G                   # left column
            F = D - Dc                       # middle row
            E = n * n
            cells = [A, B, C, Dc, E, F, G, H, I]

            if min(cells) <= 0 or len(set(cells)) != 9:
                continue
            # verify all eight lines
            ok = all(sum(cells[k] for k in line) == S for line in
                     ((0,1,2), (3,4,5), (6,7,8),
                      (0,3,6), (1,4,7), (2,5,8),
                      (0,4,8), (2,4,6)))
            if not ok:
                continue

            count = sum(1 for x in cells if sq(x) is not None)
            if count >= want:
                results.append((count, cells))
    return results

print(center_pairs(425))
for n in range(1, 3000):
    for count, c in search(n):
        print(f"n={n}  center={n*n}  squares={count}  sum={3*n*n}")
        for k in range(0, 9, 3):
            print("   ", c[k:k+3])