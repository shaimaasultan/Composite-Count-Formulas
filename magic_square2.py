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
    """Fast plain-int version of magic_cells (total must be divisible by 3).
    Center = total // 3; returns a dict of ordinary ints for search loops."""
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


def show(sq):
    w = max(len(str(x)) for row in sq for x in row)
    for row in sq:
        print("  ".join(str(x).rjust(w) for x in row))


def check(sq):
    """True if all 3 rows, 3 columns and 2 diagonals share one sum."""
    S = sum(sq[0])
    lines = sq + [[sq[i][j] for i in range(3)] for j in range(3)]
    lines += [[sq[i][i] for i in range(3)], [sq[i][2 - i] for i in range(3)]]
    return all(sp.simplify(sum(L) - S) == 0 for L in lines)


if __name__ == "__main__":
    n = sp.Symbol('n')

    print("magic_cells(3*n):")
    for k, v in magic_cells(1 * n).items():
        print(f"   {k} = {v}")

    print("\nmagic_square(3*n):")
    sqn = magic_square(1 * n)
    show(sqn)
    print("all lines equal?", check(sqn))

    print("\nmagic_square(15, 8, 1)  ->  Lo Shu:")
    lo = magic_square(15, 8, 1)
    show(lo)
    print("all lines equal?", check(lo))
