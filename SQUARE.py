from itertools import permutations

def reps(e):
    """All (u,v), u<=v, with u^2+v^2 = 2e^2."""
    t, out, u = 2*e*e, [], 1
    while 2*u*u <= t:
        v2 = t - u*u
        v = int(v2**0.5)
        if v*v == v2:
            out.append((u, v))
        u += 1
    return out

def is_sq(n):
    if n < 0: return False
    r = int(n**0.5)
    while r*r > n: r -= 1
    while (r+1)*(r+1) <= n: r += 1
    return r*r == n

def search(e, min_squares=7):
    e2, r = e*e, reps(e)
    for pa in r:
        for pc in r:
            if pa == pc: continue
            for a2 in (pa[0]**2, pa[1]**2):
                for c2 in (pc[0]**2, pc[1]**2):
                    i2, x = 2*e2 - a2, 2*e2 - c2
                    b2 = 3*e2 - a2 - c2
                    h2, d2, f2 = 2*e2 - b2, 3*e2 - a2 - x, a2 + x - e2
                    cells = [a2, b2, c2, d2, e2, f2, x, h2, i2]
                    if min(cells) <= 0 or len(set(cells)) < 9: continue
                    n = sum(is_sq(v) for v in cells)
                    if n >= min_squares:
                        yield n, cells

for e in range(5, 600):
    for n, cells in search(e,min_squares=5):
        print(e, n, cells)