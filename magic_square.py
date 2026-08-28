"""
3x3 magic square builder, labelled A..I (row-major), driven by the SUM.

    A B C
    D E F
    G H I

Give the magic SUM; the center is forced to sum/3, and a, b are the two free
parameters. Everything else is derived so all 3 rows, 3 columns and both
diagonals equal the sum.

    A = a                 B = b                 C = sum - a - b
    D = 4*sum/3 - 2a - b  E = sum/3             F = 2a + b - 2*sum/3
    G = a + b - sum/3     H = 2*sum/3 - b       I = 2*sum/3 - a

Usage:
    magic_cells(3*n)          -> {'A': a, 'B': b, ...}  symbolic in a, b, n
    magic_cells(15, 8, 1)     -> concrete Lo Shu cells
    magic_square(15, 8, 1)    -> the 3x3 grid
"""

import sympy as sp

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


def magic_cells(total, a=None, b=None):
    """Return {A..I} for a 3x3 magic square with magic sum `total`.
    Center = total/3; a, b are free (symbolic if left as None)."""
    A = sp.Symbol('a') if a is None else sp.sympify(a)
    B = sp.Symbol('b') if b is None else sp.sympify(b)
    S = sp.sympify(total)
    n = S / 3                                   # the center is always sum / 3
    C = S - A - B
    D = 4 * n - 2 * A - B
    E = n
    F = 2 * A + B - 2 * n
    G = A + B - n
    H = 2 * n - B                               # (was the bug: 2*n - n)
    I = 2 * n - A
    vals = [sp.simplify(v) for v in (A, B, C, D, E, F, G, H, I)]
    return dict(zip(LETTERS, vals))


def magic_cells_num(total, a, b):
    """Fast plain-int cells for search loops.
    A 3x3 magic square ALWAYS has center = sum/3, so `total` must be divisible
    by 3. Returns None otherwise (no integer magic square exists for that sum)."""
    if not isinstance(total, int):
        return magic_cells(total, a, b)      # symbolic/fractional -> exact builder
    if total % 3 != 0:
        return None
    c = total // 3
    return {"A": a,           "B": b,           "C": total - a - b,
            "D": 4 * c - 2 * a - b, "E": c,       "F": 2 * a + b - 2 * c,
            "G": a + b - c,   "H": 2 * c - b,   "I": 2 * c - a}


def magic_square(total, a=None, b=None):
    """Return the 3x3 grid (list of rows) for magic sum `total`."""
    c = magic_cells(total, a, b)
    return [[c["A"], c["B"], c["C"]],
            [c["D"], c["E"], c["F"]],
            [c["G"], c["H"], c["I"]]]


def semi_magic_cells(total, a, b, d, e):
    """SEMI-magic square: every ROW and COLUMN sums to `total`, but the two
    DIAGONALS are NOT constrained.  That relaxation gives 4 free parameters
    (a, b, d, e) instead of 2 -- and repeated cells are allowed.

        A B C       a           b           total-a-b
        D E F   =   d           e           total-d-e
        G H I       total-a-d   total-b-e   a+b+d+e-total
    """
    S = sp.sympify(total)
    A, B, D, E = (sp.sympify(x) for x in (a, b, d, e))
    return {"A": A,          "B": B,          "C": S - A - B,
            "D": D,          "E": E,          "F": S - D - E,
            "G": S - A - D,  "H": S - B - E,  "I": A + B + D + E - S}


def semi_magic_square(total, a, b, d, e):
    """Return the 3x3 grid for a semi-magic square (rows+cols = total)."""
    c = semi_magic_cells(total, a, b, d, e)
    return [[c["A"], c["B"], c["C"]],
            [c["D"], c["E"], c["F"]],
            [c["G"], c["H"], c["I"]]]


def show(sq):
    w = max(len(str(x)) for row in sq for x in row)
    for row in sq:
        print("  ".join(str(x).rjust(w) for x in row))


def check(sq, diagonals=True):
    """True if all rows and columns share one sum.
    diagonals=True (default) also requires both diagonals  -> full magic square.
    diagonals=False checks rows+columns only              -> semi-magic square."""
    S = sum(sq[0])
    lines = sq + [[sq[i][j] for i in range(3)] for j in range(3)]
    if diagonals:
        lines += [[sq[i][i] for i in range(3)], [sq[i][2 - i] for i in range(3)]]
    return all(sp.simplify(sum(L) - S) == 0 for L in lines)


def build(total, a=None, b=None):
    """Convenience: print the full square for ANY total and return the grid.
    Just give the total; a, b are optional (left symbolic if omitted)."""
    sq = magic_square(total, a, b)
    print(f"total = {total}   center = {sp.simplify(sp.sympify(total) / 3)}"
          + ("" if a is None else f"   a={a}, b={b}"))
    show(sq)
    print("all lines equal?", check(sq))
    return sq


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        # e.g.  python magic_square.py 15 8 1     or     python magic_square.py 21
        total = sp.sympify(sys.argv[1])
        a = sp.sympify(sys.argv[2]) if len(sys.argv) > 2 else None
        b = sp.sympify(sys.argv[3]) if len(sys.argv) > 3 else None
        build(total, a, b)
    else:
        print("Usage: python magic_square.py TOTAL [a b]   (TOTAL may be a number or 'n')\n")
        n = sp.Symbol('n')
        print("magic_square(1*n):   (total = n, center = n/3)")
        show(magic_square(1 * n))
        print("all lines equal?", check(magic_square(1 * n)))
        print("\nmagic_square(15, 8, 1)  ->  Lo Shu (full magic):")
        show(magic_square(15, 8, 1))

        print("\nsemi_magic_square(30, a=5, b=9, d=9, e=5)  (rows+cols only, repeats OK):")
        sm = semi_magic_square(30, 5, 9, 9, 5)
        show(sm)
        print("rows+cols equal?", check(sm, diagonals=False),
              " | also a full magic square?", check(sm, diagonals=True))
        print(magic_cells_num(n ,1,1))