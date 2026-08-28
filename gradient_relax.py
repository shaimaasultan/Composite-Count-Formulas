"""
Continuous relaxation of the magic-square-of-squares search (the 'gradient to the mean'
idea). Treat the two knobs (A, D) as real numbers; the centre k**2 is fixed and every
antipodal pair is symmetric about it (sum 2k**2), so a pair's two cells are the mean plus
and minus an offset. Each cell 'wants' to be a perfect square; we descend the loss

    L(A,D) = sum_i ( cell_i - nearest_square(cell_i) )**2 ,

over the 2-parameter plane. Because the pair sum is pinned to 2k**2, pushing one member
toward a square pushes its partner off -- the coupling shows up as a tug-of-war, and the
flow settles at a local minimum, not necessarily zero.
"""
from math import isqrt, sqrt

# cell as linear form in (A, D); coeff = (dCell/dA, dCell/dD), const added with k**2
CELLS = {
    "A": (1, 0, 0), "D": (0, 1, 0),
    "I": (-1, 0, 2), "F": (0, -1, 2),          # 2k^2 - A , 2k^2 - D
    "C": (1, 1, -1), "G": (-1, -1, 3),         # A+D-k^2 , 3k^2-A-D
    "B": (-2, -1, 4), "H": (2, 1, -2),         # 4k^2-2A-D , 2A+D-2k^2
}


def cells(k, A, D):
    e = k * k
    return {n: cA * A + cD * D + ck * e for n, (cA, cD, ck) in CELLS.items()}


def nearest_square(v):
    if v <= 0:
        return 0.0
    r = round(sqrt(v))
    return float(r * r)


def relax(k, A0, D0, eta=0.02, steps=20000):
    """Gradient descent on the distance-to-nearest-square loss over (A, D)."""
    e = k * k
    A, D = float(A0), float(D0)
    for _ in range(steps):
        cur = cells(k, A, D)
        gA = gD = 0.0
        for n, (cA, cD, ck) in CELLS.items():
            v = cur[n]
            resid = v - nearest_square(v)        # target held locally constant
            gA += 2 * resid * cA
            gD += 2 * resid * cD
        A -= eta * gA / e                         # normalise step by k^2
        D -= eta * gD / e
    return A, D


def report(k, A, D):
    print(f"  settled (A,D) ~ ({A:.1f}, {D:.1f})  ~ ({sqrt(A):.2f}^2, {sqrt(D):.2f}^2)")
    exact = 0
    for n, v in cells(k, A, D).items():
        r = isqrt(int(round(v)))
        near = r * r if abs(r*r - v) <= abs((r+1)**2 - v) else (r+1)**2
        d = v - near
        sq = abs(d) < 0.5
        exact += sq
        print(f"    {n} = {v:12.1f}   nearest sq {int(round(sqrt(near)))}^2, off by {d:+.1f}"
              f"{'   <-- square' if sq else ''}")
    print(f"  cells landing on a square: {exact} of 8")


if __name__ == "__main__":
    k = 425
    print("start near the 425 record (A=205^2, D=527^2):")
    A, D = relax(k, 205**2 + 3000, 527**2 - 4000)
    report(k, A, D)
