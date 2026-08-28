"""
shift_magic.py
--------------
A 3x3 magic square of squares in the SHIFT parametrization (k, g1, g2).

An apex is fixed by a center k and a shift g (= offset delta):
    area = g/4,   cells = k^2 - g  and  k^2 + g.

A whole square is three integers (k, g1, g2): one center and two shifts.
The other two shifts are FORCED (definitional, only additions):
    g3 = g1 + g2   (middle column)
    g4 = g1 - g2   (middle row)

Grid (center c = k^2):

    c+g1        c-g1-g2     c+g2
    c-g1+g2     c           c+g1-g2
    c-g2        c+g1+g2     c-g1

Every row, column and diagonal sums to 3*k^2 automatically.
It is a magic square of NINE squares iff all eight outer cells
    k^2 -/+ g1,  k^2 -/+ g2,  k^2 -/+ (g1+g2),  k^2 -/+ (g1-g2)
are perfect squares (the center k^2 always is).
"""

from math import isqrt


def is_square(n):
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def shifts(g1, g2):
    """The four shifts of the square: two chosen, two forced (only additions)."""
    return (g1, g2, g1 + g2, g1 - g2)


def cells(k, g1, g2):
    """The eight outer cells k^2 -/+ g for the four shifts (center k^2 omitted)."""
    c = k * k
    out = []
    for g in shifts(g1, g2):
        out.append(c - g)
        out.append(c + g)
    return out


def count_squares(k, g1, g2):
    """How many of the 8 outer cells are perfect squares (0..8); +1 for the center."""
    return sum(1 for v in cells(k, g1, g2) if is_square(v))


def build_grid(k, g1, g2):
    """The 3x3 grid from (k, g1, g2); every line sums to 3*k^2."""
    c = k * k
    return [
        [c + g1,      c - g1 - g2, c + g2],
        [c - g1 + g2, c,           c + g1 - g2],
        [c - g2,      c + g1 + g2, c - g1],
    ]


def is_nine_squares(k, g1, g2):
    """True iff all nine cells are perfect squares (a full magic square of squares)."""
    if g1 - g2 <= 0 or g1 + g2 > k * k:      # keep shifts positive and under the ceiling
        return False
    return count_squares(k, g1, g2) == 8      # center is automatically a square


def apex_shifts(k):
    """The genuine apex shifts of center k: offsets g with BOTH k^2-/+g square."""
    c = k * k
    out = []
    a = 1
    while a < k:
        hi = 2 * c - a * a
        b = isqrt(hi)
        if b * b == hi and b > k:             # a^2, b^2 with a^2+b^2 = 2k^2
            out.append(c - a * a)             # g = k^2 - a^2  (a full apex offset)
        a += 1
    return sorted(out)


def best_on_center(k):
    """Best magic square on center k^2 over all square corners: (max squares, grid)."""
    c = k * k
    R = isqrt(2 * c)
    best, grid = -1, None
    for ra in range(1, R + 1):
        A = ra * ra                            # corner c+g1  -> g1 = A - c  (may be signed)
        for rc in range(ra, R + 1):
            C = rc * rc
            g1 = A - c                          # main-diagonal shift (signed)
            g2 = C - c                          # anti-diagonal shift (signed)
            cs = cells_signed(c, g1, g2)
            if cs is None:
                continue
            n = sum(1 for v in cs if is_square(v))
            if n > best:
                best, grid = n, reshape(c, cs)
    return best, grid


def cells_signed(c, g1, g2):
    """All 9 cells for signed shifts; returns None if any negative or not distinct."""
    vals = [c + g1, c - g1 - g2, c + g2,
            c - g1 + g2, c, c + g1 - g2,
            c - g2, c + g1 + g2, c - g1]
    if any(v < 0 for v in vals) or len(set(vals)) < 9:
        return None
    return vals


def reshape(c, vals):
    return [vals[0:3], vals[3:6], vals[6:9]]


def search_full(kmax):
    """Scan centers for a FULL nine-square magic square via apex shifts."""
    for k in range(2, kmax):
        gs = set(apex_shifts(k))
        if len(gs) < 3:
            continue
        gl = sorted(gs)
        for g1 in gl:
            for g2 in gl:
                if g2 >= g1:
                    break
                if (g1 + g2) in gs and (g1 - g2) in gs and g1 + g2 <= k * k:
                    return (k, g1, g2)          # all four shifts are genuine apexes
    return None


if __name__ == "__main__":
    # the classic 7-square on center 425^2, in shift form
    k, g1, g2 = 425, 138600, 41496
    print(f"(k, g1, g2) = ({k}, {g1}, {g2})   center = {k*k},  magic sum = {3*k*k}")
    grid = build_grid(k, g1, g2)
    for row in grid:
        print("   ", [f"{isqrt(v)}^2" if is_square(v) else "NS" for v in row])
    print("   squares:", 1 + count_squares(k, g1, g2), "of 9")
    print()
    # search for a full nine-square
    print("search_full(6000):", search_full(6000) or "None  (no nine-square in range)")


# ---- parity / mod-8 pruning (primitive: k odd -> every cell must be 1 mod 8) ----

def mod8_ok(k, g1, g2):
    """Fast reject: a primitive magic square of squares has k odd and every cell
    congruent to 1 mod 8. Returns False if the configuration cannot be primitive."""
    if k % 2 == 0:
        return False                          # even k reduces to an odd-k square
    c = k * k
    for g in shifts(g1, g2):
        if (c - g) % 8 != 1 or (c + g) % 8 != 1:
            return False
    return True


def search_full_pruned(kmax):
    """Same as search_full but restricted to odd k and mod-8-valid shifts."""
    for k in range(3, kmax, 2):               # odd centers only
        gs = set(apex_shifts(k))
        if len(gs) < 3:
            continue
        gl = sorted(gs)
        for g1 in gl:
            for g2 in gl:
                if g2 >= g1:
                    break
                if (g1 + g2) in gs and (g1 - g2) in gs and g1 + g2 <= k * k \
                        and mod8_ok(k, g1, g2):
                    return (k, g1, g2)
    return None
