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
from fractions import Fraction as Fr


# --- basis of the 3x3 magic-square space: mutually orthogonal J, P, Q -----------
_J = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]                 # carries the sum (magic 3)
_P = [[1, -1, 0], [-1, 0, 1], [0, 1, -1]]              # the 'a' generator (magic 0)
_Q = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]              # the 'c' generator (magic 0)


def _dot(A, B):
    return sum(A[i][j] * B[i][j] for i in range(3) for j in range(3))


def make_magic(M):
    """Nearest magic square to a 3x3 grid M -- the least-squares projection onto the
    magic-square space span{J, P, Q} (these three are mutually orthogonal, with
    <J,J>=9, <P,P>=<Q,Q>=6).  It redistributes each line's mismatch across the cells
    with the SMALLEST total change, and preserves the grand total, so the magic sum
    is (sum of M)/3.  Returns exact Fractions.

        a = <M,J>/9,  b = <M,P>/6,  c = <M,Q>/6      ->   a*J + b*P + c*Q

    If M is already magic it is returned unchanged.  If it is not, the correction
    generally BREAKS the perfect-square cells (and may go negative or fractional):
    forcing magic and keeping the squares pull against each other -- that is the
    whole obstruction.  e.g. the 9-square point-symmetric grid collapses to 1 square,
    the 8-square grid to 3, once made magic."""
    a = Fr(_dot(M, _J), 9)
    b = Fr(_dot(M, _P), 6)
    c = Fr(_dot(M, _Q), 6)
    return [[a * _J[i][j] + b * _P[i][j] + c * _Q[i][j] for j in range(3)]
            for i in range(3)]


def line_sums(M):
    """The 8 line sums (3 rows, 3 cols, 2 diagonals) of a 3x3 grid."""
    rows = [sum(M[i]) for i in range(3)]
    cols = [sum(M[i][j] for i in range(3)) for j in range(3)]
    diag = [M[0][0] + M[1][1] + M[2][2], M[0][2] + M[1][1] + M[2][0]]
    return rows + cols + diag


def is_magic_grid(M):
    return len(set(line_sums(M))) == 1


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
    return {"A": 1+A,          "B": 1+B, "C": 1+C,
            "D": 1+D,          "E": 1,         "F":1 -D,
            "G": 1 -C,          "H": 1 -B, "I":  1 - A}
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


def search(want=7, verbose=True, E=442 , rich=7, mode="pairs"):
    """MAGIC square-of-squares search.  E is the ROOT, so the center is the perfect
    square  c = E*E  and magic sum = 3c.  Every candidate is magic by construction
    (magic_from); we count how many of the 9 cells are perfect squares.

    The two FREE cells are a CORNER (A) and an EDGE (B) -- not two corners.  That
    matters: a 7-square family like 425 has its two full opposite-pairs on the
    corner-diagonal AND the edge-pair, so you need one corner-pair value and one
    edge-pair value.  square_pairs(2c) supplies both.

    mode="pairs"  : magic_from(a, b) with a=corner, b=edge, both from pair values.
                    Fast O(pairs^2); every hit is MAGIC and it reaches 425 (7 squares).
    mode="hybrid" : runs BOTH builders and reports BOTH bests --
                      * magic_from -> best MAGIC square (up to 7), and
                      * cells_from -> best POINT-SYMMETRIC grid (up to 9, non-magic).
    """
    from itertools import product
    c = E * E
    S = 3 * c
    pairs = square_pairs(2* c)
    pool = sorted({u * u for u, v in pairs} | {v * v for u, v in pairs})
    # offsets for the E +/- A form (cells_from): half-difference of each pair, so
    # that E-offset = u^2 and E+offset = v^2 are BOTH squares  (offset = c - u^2)
    offsets = sorted({c - u * u for u, v in pairs})
    if not pool:
        return 0
    best, best_sq = 0, None            # best overall (by square count)
    best_m, best_msq = 0, None         # best MAGIC square
    seen = set()

    def consider(cc):
        nonlocal best, best_sq, best_m, best_msq
        vals = [cc[k] for k in "ABCDEFGHI"]
        if min(vals) <= 0 or len(set(vals)) < 9:
            return
        cnt = sum(is_sq(v) for v in vals)
        mg = ismagic(cc)
        if cnt > best:
            best, best_sq = cnt, dict(cc)
        if mg and cnt > best_m:
            best_m, best_msq = cnt, dict(cc)
        if cnt >= want and verbose:
            key = (mg, tuple(sorted(vals)))
            if key in seen:
                return
            seen.add(key)
            print(f"squares={cnt}  root={E}  center={c}  sum={S}  MAGIC={mg}")
            for row in ("ABC", "DEF", "GHI"):
                print("   ", [f"{cc[k]}{'*' if is_sq(cc[k]) else ''}" for k in row])

    # (1) MAGIC search -- always: magic_from over pool x pool (corner + edge)
    for a in pool:
        for b in pool:
            consider(magic_from(a, b, c))
    # (2) POINT-SYMMETRIC search -- hybrid only: cells_from is the E +/- A form,
    #     so feed it OFFSETS (half-differences), not square values.  E-/+offset are
    #     both squares -> reaches the 9-square (non-magic) grid.
    if mode == "hybrid":
        for a, b, C, D in product(offsets, repeat=4):
            consider(cells_from(a, b, C, D, c))

    def show(tag, sq):
        print(f"\n{tag} for root={E} (center={c}): "
              f"{sum(is_sq(sq[k]) for k in sq)} of 9 squares, MAGIC={ismagic(sq)}")
        for row in ("ABC", "DEF", "GHI"):
            print("   ", [f"{sq[k]}{'*' if is_sq(sq[k]) else ''}" for k in row])

    rich = len(pairs)
    # report the MAGIC best and (in hybrid) the point-symmetric best, independently
    if best >= want and best_m >= want:
        print(f"root {E}: richness (square_pairs of 2*center) = {rich}")
        if best_msq:
            show("best MAGIC", best_msq)
        if mode == "hybrid" and best_sq and best_sq is not best_msq:
            show("best overall", best_sq)
    return best_m if mode == "pairs" else best

def ismagic(L):
    return (L["A"]+L["B"]+L["C"] == L["D"]+L["E"]+L["F"] == L["G"]+L["H"]+L["I"]
           == L["A"]+L["E"]+L["I"] == L["C"]+L["E"]+L["G"] == L["B"]+L["E"]+L["H"]
           == L["A"]+L["D"]+L["G"] == L["C"]+L["F"]+L["I"])


def search_mod3(root, want=7, verbose=True, off_lim=None):
    """Search the two integer offsets A, C directly (center E = root^2), using the
    mod-3 necessary condition.

    A perfect square is 0 or 1 (mod 3), never 2.  The nine cells are
        E+A, E-A-C, E+C, E-A+C, E, E+A-C, E-C, E+A+C, E-A .
    Working mod 3 shows: unless A == 0 AND C == 0 (mod 3), at least three cells land
    on residue 2 and can't be squares, capping the count at 6.  So *every* square
    square-of-squares with 7+ squares has A == C == 0 (mod 3).  We therefore step
    A and C by 3 -- a lossless 9x pruning for the 7/8/9-square hunt (it does skip
    some 6-square grids that sit off the grid; those aren't records).

    Cost is still O(E^2/9), so this is a demonstrator for small roots; for large
    rich centers use search(..., mode='pairs'/'hybrid')."""
    E = root * root
    if off_lim is None:
        off_lim = E - 1
    off_lim -= off_lim % 3                       # snap to a multiple of 3
    best, best_cells = 0, None
    for A in range(0, off_lim + 1, 3):           # A >= 0 by reflection symmetry
        for C in range(-off_lim, off_lim + 1, 3):
            cells = [E+A, E-A-C, E+C, E-A+C, E, E+A-C, E-C, E+A+C, E-A]
            if min(cells) <= 0 or len(set(cells)) < 9:
                continue
            cnt = sum(1 for v in cells if is_sq(v))
            if cnt > best:
                best, best_cells = cnt, cells
    if verbose and best >= want and best_cells:
        k = "ABCDEFGHI"
        d = dict(zip(k, best_cells))
        print(f"root {root}: {best} of 9 squares (mod-3 search), MAGIC={ismagic(d)}")
        for row in ("ABC", "DEF", "GHI"):
            print("   ", [f"{d[x]}{'*' if is_sq(d[x]) else ''}" for x in row])
    return best


def _sieve_residues(E, M):
    """The (A mod M, C mod M) residue pairs for which all 9 cells are square-
    ELIGIBLE (each cell a quadratic residue mod M).  A necessary condition, so any
    real square-of-squares offset pair reduces to one of these mod M."""
    Q = {(x * x) % M for x in range(M)}
    em = E % M
    out = []
    for ar in range(M):
        for cr in range(M):
            cells = [em+ar, em-ar-cr, em+cr, em-ar+cr, em, em+ar-cr, em-cr, em+ar+cr, em-ar]
            if all(v % M in Q for v in cells):
                out.append((ar, cr))
    return out


def search_sieve(root, want=7, verbose=True, mode="pairs"):
    """FAST square-of-squares search.  Instead of scanning offsets and sieving them
    (O(E^2)), we draw the two free CELLS straight from square_pairs -- a pair value
    IS a perfect square, so it passes every modular sieve (mod 3, 4, 8, 16, 5, ...)
    for free.  That's strictly stronger than the sieve and costs only O(pairs^2).

    mode="pairs"  : corner a and edge b both from pair values (magic_from). O(pairs^2),
                    reaches the 425 family (7 squares) instantly.
    mode="hybrid" : corner a from a pair, edge b swept over ALL squares below 2E but
                    pruned to sieve-eligible residues -- widest fast net for lone
                    squares.  O(pairs * sqrt(2E) / sieve-density)."""
    E = root * root
    pairs = square_pairs(2 * E)
    pool = sorted({u * u for u, v in pairs} | {v * v for u, v in pairs})
    if not pool:
        return 0
    if mode == "hybrid":
        # sieve-eligible edge values: squares b with b % M in the square residues
        M = 240
        Q = {(x * x) % M for x in range(M)}
        lim = isqrt(2 * E)
        edge = [k * k for k in range(1, lim + 1) if (k * k) % M in Q]
    else:
        edge = pool
    best, best_sq = 0, None
    for a in pool:
        for b in edge:
            cc = magic_from(a, b, E)
            vals = [cc[k] for k in "ABCDEFGHI"]
            if min(vals) <= 0 or len(set(vals)) < 9:
                continue
            cnt = sum(is_sq(v) for v in vals)
            if cnt > best:
                best, best_sq = cnt, dict(cc)
    if verbose and best_sq and best >= want:
        flag = "" if best >= want else "  (below want)"
        print(f"root {root}: {best} of 9 squares (pairs, mode={mode}), "
              f"MAGIC={ismagic(best_sq)}{flag}")
        for row in ("ABC", "DEF", "GHI"):
            print("   ", [f"{best_sq[k]}{'*' if is_sq(best_sq[k]) else ''}" for k in row])
    return best
if __name__ == "__main__":
    # Rank centers by the RIGHT richness measure: square_pairs(2*c) with c = i*i
    # (sum-of-two-squares reps -> flanking square-pairs).  partners() is the WRONG
    # proxy (difference of squares) and is dropped.
    MIN_RICH = 1           # only look at roots whose center has >= this many pairs
    for i in range(1, 50):
        rich = len(square_pairs(2 * i * i))
        if rich >= MIN_RICH :
            search(want=6, verbose=False, E=i , rich=rich,mode="hybrid") # point-symmetric, maybe not magic
            #search_sieve(want=7, verbose=True, root=i ,mode="pairs") # point-symmetric, maybe not magic
    
    #search(want=6, verbose=False, E=195364 , rich=rich,mode="hybrid") # point-symmetric, maybe not magic