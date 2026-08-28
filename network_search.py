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


def scan(kmax):
    """
    Sweep centres k and square inputs A=a^2 and free knobs D=d^2 up to kmax; return the
    best border-square count found and the centres that reach the 7-of-9 record (6 border
    squares). This is an empirical bound --- 'none better found below kmax', not a proof.
    """
    best = (-1, None)
    record_centres = set()
    for k in range(3, kmax + 1):
        two = 2 * k * k
        dmax = isqrt(two)
        for a in range(1, k):
            A = a * a
            for d in range(1, dmax + 1):
                D = d * d
                if D >= two:
                    break
                s = score(k, A, D)
                if s > best[0]:
                    best = (s, (k, a, d))
                if s >= 6:
                    record_centres.add(k)
    return best, sorted(record_centres)


def complementary_members(k):
    """
    Values c that are perfect squares AND whose companion 2k^2 - c is also a perfect square
    (the both-square pairs, 2k^2 = x^2 + y^2). One O(k) pass per centre. Restricting the
    inputs A, D to these guarantees the companions I, F are square, which is where every
    high-scoring settlement lives.
    """
    two = 2 * k * k
    mem = []
    x = 1
    while x * x < two:
        s = x * x
        rem = two - s
        y = isqrt(rem)
        if y * y == rem and s <= rem:          # both square, no duplicates
            mem.append(s)
            if rem != s:
                mem.append(rem)
        x += 1
    return mem


def scan_fast(kmax):
    """
    Structure-based scan: O(n^2) instead of O(n^3). For each centre find the both-square
    members in one O(k) pass, then combine them as (A, D) -- a small set -- rather than
    sweeping every (a, d). Catches every settlement whose companions I, F are square,
    including the record.
    """
    best = (-1, None)
    record_centres = set()
    for k in range(3, kmax + 1):
        mem = complementary_members(k)
        for A in mem:
            for D in mem:
                s = score(k, A, D)
                if s > best[0]:
                    best = (s, (k, A, D))
                if s >= 6:
                    record_centres.add(k)
    return best, sorted(record_centres)


if __name__ == "__main__":
    max = [0,{}]
    for j in range(12325, 12326,2):
        for i in range(1,1000):
            k, a = j, i                           # centre 425^2, one square input 205^2
            s, D = search(k, a)
            if D == None: continue
            A = a * a
            cells = border(k, A, D)
            print(f"centre k^2 = {k*k}; input A = {a}^2 = {A}; free knob settled at D = {D} "
                f"= {isqrt(D)}^2")
            print(f"best score: {s} of 8 border cells square  (+ centre = {s+1} of 9)")
            if s+1 > max[0]:
                max = [s+1, {j: [i]} ]        # new record: start a fresh list
            elif s+1 == max[0]:
                if j not in max[1].keys():
                    max[1][j] = [i]
                else:
                    max[1][j].append(i)        # tie: append
            print()
            for n, v in cells.items():
                r = isqrt(v)
                tag = f"{r}^2" if r*r == v else f"{v}  (not square)"
                print(f"   {n} = {v:>8}   {tag}")
            w = weights(k, A, D)
            print("\nnormalised weights w_i = cell/k^2 sum to:", sum(w.values()))
    
    print(max)

    # print("\n--- bounded scan (empirical ceiling, not a proof) ---")
    # best_s, centres = scan(790)
    # bs, (bk, ba, bd) = best_s
    # print(f"scan k<=150: best {bs} of 8 border squares at k={bk}, A={ba}^2, D={bd}^2")
    # print(f"centres reaching 7 of 9 (6 border squares) with k<=150: {centres}")
    # print("425 is the smallest 7-of-9 centre; no centre anywhere is known to exceed 7 of 9.")
