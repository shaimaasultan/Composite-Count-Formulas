"""
Search for 3x3 "magic square of squares" using the labelled square from
magic_square.py (all rows/cols/diagonals = the magic sum).

Setup:  magic sum = 3*n^2, so the CENTER E = n^2 is itself a perfect square.
The two free parameters a, b are taken as perfect squares, so A = a and B = b
are squares too -> A, B, E are square by construction (3 of the 9 cells).

The remaining cells come straight from magic_cells_num(), and we count how many
of all nine are perfect squares:

    A B C
    D E F
    G H I

7 square cells is the near-record; a full 9 (all distinct squares) is a famous
open problem.
"""

from math import isqrt
from magic_square import magic_cells_num, LETTERS


def is_sq(m):
    if m <= 0:
        return False
    r = isqrt(m)
    return r * r == m


def search(n_max=120, want=6):
    best = 0
    for n in range(1, n_max + 1):
        S = 3*n             # center E = n^2 (a perfect square); magic sum = 3*n^2
        im = isqrt(S)
        for i in range(1, im + 1):
            a = i * i                       # A = a is a perfect square
            for j in range(1, im + 1):
                b = j * j                   # B = b is a perfect square
                c = magic_cells_num(S, a, b)
                #c["D"] = n*n
                #c["H"] = b*b
                #print(c)
                if c is None:                # sum not divisible by 3 -> no integer square
                    continue
                vals = [c[k] for k in LETTERS]
                if min(vals) <= 0 or len(set(vals)) < 8:
                    continue                # need distinct, positive entries
                cnt = sum(1 for v in vals if is_sq(v))
                if cnt >= want:
                    print(f"squares={cnt}  n={n}  center={n*n}  sum={S}  a={a} b={b}")
                    for row in (("A", "B", "C"), ("D", "E", "F"), ("G", "H", "I")):
                        print("   ", [f"{c[k]}{'*' if is_sq(c[k]) else ''}" for k in row])
                    best = max(best, cnt)
    print(f"\nbest found: {best} of 9 cells are perfect squares  "
          f"(7 = near-record, 9 = open problem).  '*' marks a square cell.")


if __name__ == "__main__":
    # n up to 300 (center up to 300^2 = 90000) finds 6-square magic squares fast.
    # want=7 is the near-record and needs far larger / smarter search than brute force.
    search(n_max=100, want=7)


