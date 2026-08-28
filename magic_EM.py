"""
Build a 3x3 magic square in the factored form  square = E * M.

Two shape matrices are provided:

  M_dev(A,B,C,D)   -- your matrix: center 1, opposite cells negated.
                      This is the DEVIATION shape; E*M_dev is NOT magic
                      (rows sum to E(A+B+C), E, -E(A+B+C)).

  M_mag(A,C[,B,D])  -- the center-1 NORMALIZED magic square (1 +/- offsets).
                      E*M_mag IS a genuine magic square (center E, sum 3E).
                      With B=-A-C and D=C-A forced, it is FULLY magic.

Here A,B,C,D are offset RATIOS (cell/E - 1); using Fractions makes E*M exact.
"""

from fractions import Fraction as Fr
from math import isqrt

def is_sq(m):
    if m < 0:
        return False
    r = isqrt(m)
    return r * r == m

def _rt(v):
    """Integer square root if v is a perfect square, else None.
    A Fraction is a perfect square ONLY if it is an integer whose value is square
    (a non-integer like 2561/40 is NOT a square -- do not int()-truncate it)."""
    if isinstance(v, Fr):
        if v.denominator != 1:
            return None            # genuine fraction -> not a perfect square
        v = v.numerator
    v = int(v)
    if v < 0:
        return None
    r = isqrt(v)
    return r if r * r == v else None


def is_sq(v):
    """True if v is a (nonnegative) perfect square."""
    return _rt(v) is not None


def M_dev(A,  C, B = None,D=None):
    """Your matrix: center 1, opposite cells negated (the deviation shape)."""
    if B is None:
        B = -A - C
    if D is None:
        D = C - A
    return {"A": A, "B": B, "C": C,
            "D": D, "E": Fr(1), "F": -D,
            "G": -C, "H": -B, "I": -A}


def M_mag(A, C, B=None, D=None):
    """Center-1 normalized MAGIC square: E*M_mag is a real magic square.
    A, C are the two free offset ratios; B, D are forced for full magic:
        B = -A - C   (top row = 3)      D = C - A   (left column = 3)."""
    A, C = Fr(A), Fr(C)
    if B is None:
        B = -A - C
    if D is None:
        D = C - A
    return {"A": 1 + A, "B": 1 + B, "C": 1 + C,
            "D": 1 + D, "E": Fr(1), "F": 1 - D,
            "G": 1 - C, "H": 1 - B, "I": 1 - A}


def from_cells(E, A_cell, C_cell):
    """Choose A, C by naming the two free CELLS (e.g. two perfect squares).
    A = (A_cell - E)/E,  C = (C_cell - E)/E ;  the rest of the square is forced.
    Returns the offset ratios (A, C) and the finished square E*M_mag."""
    A = Fr(A_cell - E, E)
    C = Fr(C_cell - E, E)
    return A, C, times_E(M_mag(A=A, C=C), E)


def times_E(M, E):
    """The actual square:  E * M  (exact; integer when E clears denominators)."""
    return {k: E * v for k, v in M.items()}


def line_sums(g):
    S = [g["A"] + g["B"] + g["C"], g["D"] + g["E"] + g["F"], g["G"] + g["H"] + g["I"],
         g["A"] + g["D"] + g["G"], g["B"] + g["E"] + g["H"], g["C"] + g["F"] + g["I"],
         g["A"] + g["E"] + g["I"], g["C"] + g["E"] + g["G"]]
    return S


def is_magic(g):
    return len(set(line_sums(g))) == 1


def all_AC(E, want=6, verbose=True):
    """For a FIXED center E, scan every pair of perfect-square free cells
    (A_cell, C_cell) and keep those giving a VALID magic square (9 distinct
    positive cells) with at least `want` perfect-square cells.

    Because the two free cells are chosen as squares and the rest are forced, this
    enumerates all magic-square-of-squares configurations at this center.  Returns a
    list of (A, C, grid, square_count); A, C are the offset ratios ((cell-E)/E).

    Cost O((sqrt 2E)^2): a free cell lies in (0, 2E), so its root is < sqrt(2E)."""
    lim = isqrt(2 * E)
    squares = [k * k for k in range(1, lim + 1)]
    sset = set(squares)
    e_is_sq = _rt(E) is not None
    out, seen = [], set()
    for Ac in squares:
        for Cc in squares:
            A, C, g = from_cells(E, Ac, Cc)
            vals = [int(g[k]) for k in "ABCDEFGHI"]
            if min(vals) <= 0 or len(set(vals)) < 9:
                continue
            # Ac, Cc are squares by choice; count the rest honestly
            cnt = 2 + e_is_sq + sum(v in sset or _rt(v) is not None
                                    for v in (int(g[k]) for k in "BDFGHI"))
            if cnt < want:
                continue
            key = tuple(sorted(vals))
            if key in seen:                       # skip symmetric duplicates
                continue
            seen.add(key)
            out.append((A, C, dict(g), cnt))
            if verbose:
                print(f"squares={cnt}  A_cell={Ac}({isqrt(Ac)}^2)  C_cell={Cc}({isqrt(Cc)}^2)"
                      f"   A={A}  C={C}")
                for row in ("ABC", "DEF", "GHI"):
                    print("   ", [f"{g[k]}{'*' if _rt(g[k]) is not None else ''}" for k in row])
    if verbose and len(out) > 0:
        print(f"\n{len(out)} distinct configurations with >= {want} squares "
              f"at center E={E}; best = {max((c for *_ , c in out), default=0)}.")
    return out


def scan_primitive(centers, want=6, verbose=True):
    """Scan a list of centers but report each distinct SHAPE exactly once.

    Scale-copies (the same square at k^2 * E) have IDENTICAL offset ratios (A, C),
    because A = (A_cell - E)/E is scale-invariant.  So we key on (A, C) and skip any
    shape already seen at a smaller center -- e.g. E=580 is dropped once E=145 is in,
    since 580 = 4*145 gives the same (A, C).  Nothing is lost: a center that also
    hosts a NEW shape (one primitive to it) still contributes that shape.

    Returns a list of (E, A, C, grid, square_count), one per distinct shape."""
    centers = list(centers)
    seen, results = {}, []
    for E in centers:
        for A, C, g, cnt in all_AC(E, want, verbose=False):
            key = (A, C)                        # scale-invariant shape
            if key in seen:
                continue                        # scale-copy of an earlier center
            seen[key] = E
            results.append((E, A, C, g, cnt))
            if verbose:
                print(f"NEW  E={E}  squares={cnt}  A={A}  C={C}")
                for row in ("ABC", "DEF", "GHI"):
                    print("   ", [f"{g[k]}{'*' if is_sq(g[k]) else ''}" for k in row])
                print()
    if verbose:
        print(f"{len(results)} distinct shapes across {len(centers)} centers "
              f"(scale-copies skipped).")
    return results


def show(g, title=""):
    if title:
        print(title)
    for row in ("ABC", "DEF", "GHI"):
        print("   ", [f"{g[k]}{'*' if is_sq(g[k]) else ''}" for k in row])
    print("    line sums:", set(str(s) for s in line_sums(g)), " magic:", is_magic(g))
    print()

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

if __name__ == "__main__":
    E = 180625                     # = 425^2, the record center
    # # 425 family offsets (cell - E), as ratios of E:
    # Ao, Co = -41496, 138600        # A and C offsets; B, D are forced
    # A, C = Fr(Ao, E), Fr(Co, E)

    # print(f"center E = {E}\n")
    # show(times_E(M_mag(A, C), E), "E * M_mag  (genuine MAGIC square = the 425 family):")
    # show(times_E(M_dev(A, -A - C, C, C - A), E),
    #      "E * M_dev  (your matrix: scaled DEVIATION -- NOT magic):")
    for i in range(180625,180650):
        print(len(square_pairs(i)))
        if len(square_pairs(i)) >=7:
            print(i)
            print(len(square_pairs(i)))
            scan_primitive(range(i, i+1), want=7 , verbose=True)   # each distinct shape once, no scale-twins

    