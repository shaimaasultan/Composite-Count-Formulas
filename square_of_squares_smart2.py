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


def search(want=7, verbose=True, E=1500):
    """POINT-SYMMETRIC search: choose the FOUR free cells A, B, C, D as perfect
    squares; cells_from forces the opposite three (F,G,H,I = 2E - each).  Grids are
    point-symmetric (all 4 center-lines = 3E) but generally NOT magic.  This can
    reach more square cells than the magic search -- up to 8 or 9 -- at the cost of
    two unequal outer rows.

    To land squares on the FORCED cells too, we draw the free cells from the pool
    of squares v whose partner (2E - v) is also a square.  With >=4 such pairs the
    grid can be all-9-squares (point-symmetric)."""
    from itertools import product
    S = 3 * E
    lim = isqrt(2 * E)
    sset = {k * k for k in range(1, lim + 1)}          # squares below 2E
    e_sq = is_sq(E)
    # 'doubles': squares whose opposite 2E - v is ALSO a square (each fills a pair)
    pool = sorted(v for v in sset if (2 * E - v) in sset)
    if len(pool) < 4:                                   # not rich enough -> all squares
        pool = sorted(sset)
    best, best_sq = 0, None
    seen = set()
    for A, B, C, D in product(pool, repeat=4):
        cc = cells_from(A, B, C, D, E)                 # F,G,H,I forced; point-symmetric
        vals = [cc[k] for k in "ABCDEFGHI"]
        if min(vals) <= 0 or len(set(vals)) < 9:
            continue                                   # need 9 distinct positive cells
        cnt = sum(is_sq(v) for v in vals)              # count squares honestly
        if cnt > best:
            best, best_sq = cnt, dict(cc)
        if cnt >= want and verbose:
            key = tuple(sorted(vals))
            if key in seen:
                continue
            seen.add(key)
            print(f"squares={cnt}  center={E}  sum={S}  MAGIC={ismagic(cc)}")
            for row in ("ABC", "DEF", "GHI"):
                print("   ", [f"{cc[k]}{'*' if is_sq(cc[k]) else ''}" for k in row])
    if best >= want and best_sq:
        print(f"\nbest for center={E}: {best} of 9 cells are squares, "
              f"sum={S}, MAGIC={ismagic(best_sq)}")
        for row in ("ABC", "DEF", "GHI"):
            print("   ", [f"{best_sq[k]}{'*' if is_sq(best_sq[k]) else ''}" for k in row])
    return best

def ismagic(L):
    return (L["A"]+L["B"]+L["C"] == L["D"]+L["E"]+L["F"] == L["G"]+L["H"]+L["I"]   
           == L["A"]+L["E"]+L["I"] == L["C"]+L["E"]+L["G"] == L["B"]+L["E"]+L["H"] 
           == L["A"]+L["D"]+L["G"] == L["C"]+L["F"]+L["I"])
if __name__ == "__main__":
    for i in (195364 , 195365):# range(425364, 425365):#(195364 , 195365):
        if len(partners(i)) > 31 and len(square_pairs(2*i*i)) >=12:
            print(len(partners(i)))
            print(square_pairs(2*i*i))
            print(f"richness of {i} = {len(square_pairs(2*i*i))}  partners={len(partners(i))}")
            print(partners(i))
            search(want=6 ,verbose=False, E = i)
       