"""
The coupled-network search for a magic square of squares.

Model (Prime_Certificate, coupling section): the eight border cells are one fully
connected network with two degrees of freedom (A, D) and centre k**2. We inject
ONE square input A (and the centre k), leave the single remaining knob D free, and
let the network settle every other cell through the row/column/diagonal sums:

    I = 2k^2 - A      F = 2k^2 - D
    C = A + D - k^2   G = 3k^2 - A - D
    B = 4k^2 - 2A - D  H = 2A + D - 2k^2

The network never needs the raw values --- only the normalised weights
    w_i = cell_i / k^2 ,   which satisfy   sum_i w_i = 8   (the mean is the centre).
Scoring function: how many of the eight weights are squares of rationals, i.e. how
many border cells are perfect squares (centre k^2 is always one). We fix A and k,
sweep the free knob D over square values d^2, and keep the best score.
"""
from math import isqrt
from fractions import Fraction as Fr


def is_square(v):
    if v < 0:
        return False
    r = isqrt(v)
    return r * r == v


def border(k, A, D):
    """The eight border cells settled by the network from inputs (A, D) and centre k^2."""
    e = k * k
    return {
        "A": A, "B": 4*e - 2*A - D, "C": A + D - e, "D": D,
        "F": 2*e - D, "G": 3*e - A - D, "H": 2*A + D - 2*e, "I": 2*e - A,
    }


def weights(k, A, D):
    """Normalised weights w_i = cell_i / k^2 (they sum to 8)."""
    e = k * k
    return {n: Fr(v, e) for n, v in border(k, A, D).items()}


def score(k, A, D):
    """Number of border cells that are perfect squares (0..8); centre adds 1 more.
    Requires the nine cells to be DISTINCT (a magic square of squares needs distinct
    entries; the degenerate solution with repeated cells is excluded)."""
    cells = border(k, A, D)
    if any(v <= 0 for v in cells.values()):
        return -1
    nine = list(cells.values()) + [k * k]
    if len(set(nine)) != 9:                     # reject repeated entries
        return -1
    return sum(is_square(v) for v in cells.values())


def search(k, a, droot_max=None):
    """
    Fix the centre k and ONE square input A = a^2; sweep the free knob over squares
    D = d^2 and return the best-scoring settlement.
    """
    A = a * a
    if droot_max is None:
        droot_max = isqrt(2 * k * k)          # D < 2k^2 keeps cells positive
    best = (-1, None)
    for d in range(1, droot_max + 1):
        D = d * d
        if D >= 2 * k * k:
            break
        s = score(k, A, D)
        if s > best[0]:
            best = (s, D)
    return best                                # (squares_in_border, D)


if __name__ == "__main__":
    k, a = 425, 205                            # centre 425^2, one square input 205^2
    s, D = search(k, a)
    A = a * a
    cells = border(k, A, D)
    print(f"centre k^2 = {k*k}; input A = {a}^2 = {A}; free knob settled at D = {D} "
          f"= {isqrt(D)}^2")
    print(f"best score: {s} of 8 border cells square  (+ centre = {s+1} of 9)")
    print()
    for n, v in cells.items():
        r = isqrt(v)
        tag = f"{r}^2" if r*r == v else f"{v}  (not square)"
        print(f"   {n} = {v:>8}   {tag}")
    w = weights(k, A, D)
    print("\nnormalised weights w_i = cell/k^2 sum to:", sum(w.values()))
