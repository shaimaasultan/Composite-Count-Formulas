from math import isqrt

def is_sq(n):
    return n >= 0 and isqrt(n)**2 == n

def reps(e):
    """All (u, v) with u <= v and u^2 + v^2 = 2e^2."""
    t, out, u = 2*e*e, [], 1
    while 2*u*u <= t:
        v2 = t - u*u
        if is_sq(v2):
            out.append((u, isqrt(v2)))
        u += 1
    return out

def search(e, min_squares=7):
    """Yield (count, cells) for squares with >= min_squares square entries.

    A is drawn from reps(e), so the A/I pair is square.
    C is swept over all squares below 2e^2, so the C/X pair may be
    non-square -- which is what the Bremner configuration requires.
    """
    e2 = e*e
    seen = set()
    for pa in reps(e):
        for a2 in {pa[0]**2, pa[1]**2}:
            i2 = 2*e2 - a2
            c = 1
            while c*c < 2*e2:
                c2 = c*c
                x  = 2*e2 - c2
                b2 = 3*e2 - a2 - c2
                h2 = 2*e2 - b2
                d2 = 3*e2 - a2 - x
                f2 = a2 + x - e2
                cells = (a2, b2, c2, d2, e2, f2, x, h2, i2)
                c += 1
                if min(cells) <= 0 or len(set(cells)) < 9:
                    continue
                n = sum(is_sq(v) for v in cells)
                if n >= min_squares:
                    key = tuple(sorted(cells))
                    if key not in seen:
                        seen.add(key)
                        yield n, cells

if __name__ == "__main__":
    for e in range(5, 1000):
        for n, cells in search(e):
            print(e, n, cells)