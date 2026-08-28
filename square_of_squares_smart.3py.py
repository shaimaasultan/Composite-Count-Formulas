"""
Smart search for a 3x3 magic-square-of-squares, using the 3:2 structure.

A line through the center sums to 3*center; the two cells flanking the center
sum to 2*center.  So a pair of square cells opposite the center means
2*center = square + square -- which is plentiful only when the center n^2 is
built from primes = 1 (mod 4).  We therefore scan only "rich" centers n^2 whose
odd prime factors are all = 1 (mod 4)  (e.g. 425 = 5^2 * 17), and for each we
pick the two free cells A, C as perfect squares; the rest is forced:

    A                B = 3c - A - C     C
    D = c - A + C    E = c              F = c + A - C          (c = n^2)
    G = 2c - C       H = A + C - c      I = 2c - A             (sum = 3c)

This is always a valid magic square by construction, so a hit can never be a
fake -- we only count how many of the 9 cells are perfect squares.
"""

from math import isqrt


def is_sq(m):
    if m < 0:
        return False
    r = isqrt(m)
    return r * r == m


def odd_primes_all_1mod4(n):
    """True if every ODD prime factor of n is = 1 (mod 4).  These n give the
    richest 2*n^2 (many sum-of-two-squares representations)."""
    m = n
    while m % 2 == 0:
        m //= 2
    d = 3
    while d * d <= m:
        if m % d == 0:
            if d % 4 == 3:
                return False
            while m % d == 0:
                m //= d
        d += 2
    return not (m > 1 and m % 4 == 3)


def two_squares(N):
    """All ways N = a^2 + b^2 with 0 <= a <= b."""
    out = []
    for a in range(0, isqrt(N) + 1):
        b2 = N - a * a
        b = isqrt(b2)
        if b >= a and b * b == b2:
            out.append((a, b))
    return out


def partners(A):
    """All (m, k) with m^2 - k^2 = A^2  (Pythagorean triples having A as a leg).
    Count grows with the number of equal-parity divisor pairs of A^2 -- i.e. with
    how rich A is in primes = 1 (mod 4).  A good 'richness' proxy."""
    out, N = [], A * A
    for d in range(1, isqrt(N) + 1):
        if N % d == 0:
            e = N // d
            if d < e and (d + e) % 2 == 0:
                out.append(((d + e) // 2, (e - d) // 2))
    return out


def square_pairs(two_c):
    """Ways to write 2*center = u^2 + v^2 with 0 < u < v.  THIS is the number of
    flanking square-pairs a center allows -- the true richness measure.
    (partners() equals this only when the number has no prime = 3 mod 4.)"""
    out = []
    for u in range(1, isqrt(two_c) + 1):
        v2 = two_c - u * u
        v = isqrt(v2)
        if v > u and v * v == v2:
            out.append((u, v))
    return out


def rich_centers(root_max):
    """Candidate centers c = n^2 with n built only from 2 and primes = 1 (mod 4),
    ranked by how many flanking square-pairs (square_pairs(2c)) they offer.
    Those are the centers worth searching for many square cells."""
    out = []
    for n in range(2, root_max + 1):
        if not odd_primes_all_1mod4(n):
            continue
        out.append((len(square_pairs(2 * n * n)), n))
    out.sort(reverse=True)
    return out

def cells_from(A, B, C ,D , E):
    """3x3 magic square (center E, magic sum 3E) fixed by the two free cells A, C.

    D, F, G default to the values the magic law FORCES:
        D = E - A + C,   F = E + A - C,   G = 2E - C
    Pass any of them explicitly to override / experiment (this generally breaks
    magic, since with E fixed there are only 2 degrees of freedom -- A and C
    """
    return {"A": A,          "B": B, "C": C,
            "D": D,          "E": E,         "F":2*E -D,
            "G": 2*E -C,          "H": 2*E -B, "I": 2 * E - A}
    # return {"A": A,          "B": B, "C": C,
    #         "D": E-A+C,          "E": E,         "F":E +A-C,
    #         "G": 2*E -C,          "H": 2*E -B, "I": 2 * E - A}

def cells_from2(E, A, C, D=None, F=None, G=None):
    """3x3 magic square (center E, magic sum 3E) fixed by the two free cells A, C.

    D, F, G default to the values the magic law FORCES:
        D = E - A + C,   F = E + A - C,   G = 2E - C
    Pass any of them explicitly to override / experiment (this generally breaks
    magic, since with E fixed there are only 2 degrees of freedom -- A and C)."""
    S = 3 * E
    if D is None:
        D = E - A + C
    if F is None:
        F = E + A - C
    if G is None:
        G = 2 * E - C
    return {"A": A,          "B": S - A - C, "C": C,
            "D": D,          "E": E,         "F": F,
            "G": G,          "H": A + C - E, "I": 2 * E - A}

    # return {"A": A,          "B": E+S - A - C, "C": C,
    #         "D": E - A + C,  "E": E,         "F":  E+A - C,
    #         "G": S - C,  "H": A + C-E , "I": S - A}


def magic_from(a, b, c):
    """A full MAGIC square (center c, sum 3c) fixed by two free cells:
    a = corner A, b = edge B.  Everything else is forced.

        A = a            B = b            C = 3c - a - b
        D = 4c - 2a - b  E = c            F = 2a + b - 2c
        G = a + b - c    H = 2c - b       I = 2c - a
    """
    return {"A": a,             "B": b,           "C": 3 * c - a - b,
            "D": 4 * c - 2 * a - b, "E": c,        "F": 2 * a + b - 2 * c,
            "G": a + b - c,     "H": 2 * c - b,   "I": 2 * c - a}


def search(want=7, verbose=True, E=442, mode="pairs"):
    """MAGIC square-of-squares search.  E is the ROOT, so the center is the perfect
    square  c = E*E  and magic sum = 3c.  Every candidate is magic by construction
    (magic_from); we count how many of the 9 cells are perfect squares.

    The two FREE cells are a CORNER (A) and an EDGE (B) -- not two corners.  That
    matters: a 7-square family like 425 has its two full opposite-pairs on the
    corner-diagonal AND the edge-pair, so you need one corner-pair value and one
    edge-pair value.  square_pairs(2c) supplies both.

    mode="pairs"  : magic_from(a, b) with a=corner, b=edge, both from pair values.
                    Fast O(pairs^2); every hit is MAGIC and it reaches 425 (7 squares).
    mode="hybrid" : cells_from(a, b, C, D) -- a POINT-SYMMETRIC grid with four free
                    cells all drawn from pair values.  O(pairs^4) (pool is tiny), so
                    it can reach 9 squares, but those are generally NOT magic.
    """
    from itertools import product
    c = E *E
    S = 3 * c
    pairs = square_pairs(2 * c)
    pool = sorted({u * u for u, v in pairs} | {v * v for u, v in pairs})
    if not pool:
        return 0
    best, best_sq = 0, None
    seen = set()
    # hybrid: 4 free cells -> point-symmetric; pairs: 2 free cells -> magic
    combos = (product(pool, repeat=4) if mode == "hybrid"
              else ((a, b, None, None) for a in pool for b in pool))
    for a, b, C, D in combos:
        if mode == "hybrid":
            cc = cells_from(a, b, C, D, c)             # point-symmetric (maybe not magic)
        else:
            cc = magic_from(a, b, c)                   # always magic
        vals = [cc[k] for k in "ABCDEFGHI"]
        if min(vals) <= 0 or len(set(vals)) < 9:
            continue
        cnt = sum(is_sq(v) for v in vals)
        if cnt > best:
            best, best_sq = cnt, dict(cc)
        if cnt >= want and verbose:
            key = tuple(sorted(vals))
            if key in seen:
                continue
            seen.add(key)
            print(f"squares={cnt}  root={E}  center={c}  sum={S}  MAGIC={ismagic(cc)}")
            for row in ("ABC", "DEF", "GHI"):
                print("   ", [f"{cc[k]}{'*' if is_sq(cc[k]) else ''}" for k in row])
    if best >= want and best_sq:
        print(f"\nbest for root={E} (center={c}, mode={mode}): {best} of 9 squares, "
              f"sum={S}, MAGIC={ismagic(best_sq)}")
        for row in ("ABC", "DEF", "GHI"):
            print("   ", [f"{best_sq[k]}{'*' if is_sq(best_sq[k]) else ''}" for k in row])
    return best

def ismagic(L):
    return (L["A"]+L["B"]+L["C"] == L["D"]+L["E"]+L["F"] == L["G"]+L["H"]+L["I"]   
           == L["A"]+L["E"]+L["I"] == L["C"]+L["E"]+L["G"] == L["B"]+L["E"]+L["H"] 
           == L["A"]+L["D"]+L["G"] == L["C"]+L["F"]+L["I"])
if __name__ == "__main__":
    # Rank centers by the RIGHT richness measure: square_pairs(2*c) with c = i*i
    # (sum-of-two-squares reps -> flanking square-pairs).  partners() is the WRONG
    # proxy (difference of squares) and is dropped.
    MIN_RICH = 7            # only look at roots whose center has >= this many pairs
    for i in range(1105, 1106):
        rich = len(square_pairs(2 * i * i))
        if rich >= MIN_RICH:
            print(f"root {i}: richness (square_pairs of 2*center) = {rich}")
            search(want=7, verbose=False, E=i,mode="hybrid")  # point-symmetric, maybe not magic