"""
Search for 3x3 semi-magic squares of squares centered on e = N**2.

Layout        a b c
              d e f     e = N**2, magic constant S = 3e
              g h i

Semi-magic = all 3 rows and 3 columns equal S (6 lines). That forces the
middle row and middle column to be complementary square-pairs:
    d + f = 2e ,  b + h = 2e   (both terms perfect squares)
Given those, the four corners are determined by a single free corner a = t:
    c = 3e - b - t
    g = 3e - d - t
    i = t - 2e + b + d
We sweep t over all perfect squares and keep cases where c, g, i are also
squares. Then we count how many of the 8 lines (incl. 2 diagonals) are magic.
A fully magic 3x3 of 9 distinct squares is unsolved; 7 of 8 is the record.
"""
import math

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def square_pairs(e):
    """(s, 2e-s) with both perfect squares, s < e."""
    out = []
    two_e = 2 * e
    for x in range(1, math.isqrt(e) + 1):
        s = x * x
        if s >= e:
            break
        rem = two_e - s
        y = math.isqrt(rem)
        if y * y == rem:
            out.append((s, rem))
    return out


def search(N):
    e = N * N
    S = 3 * e
    pairs = square_pairs(e)                      # candidate middle row/col pairs
    is_sq = lambda v: v > 0 and math.isqrt(v) ** 2 == v
    kmax = math.isqrt(2 * e)
    corner_squares = [t * t for t in range(1, kmax + 1) if t * t < 2 * e]

    best = -1
    best_grids = []
    seen = set()
    for (d, f) in pairs:                          # middle row (both orders)
        for (b, h) in pairs:                      # middle col
            for t in corner_squares:              # a = t
                a = t
                c = S - b - a
                g = S - d - a
                i = a - 2 * e + b + d
                if not (is_sq(c) and is_sq(g) and is_sq(i)):
                    continue
                grid = [a, b, c, d, e, f, g, h, i]
                if len(set(grid)) != 9:           # need 9 distinct entries
                    continue
                if min(grid) <= 0:
                    continue
                cnt = sum(1 for x, y, z in LINES
                          if grid[x] + grid[y] + grid[z] == S)
                key = tuple(grid)
                if cnt > best:
                    best = cnt
                    best_grids = [grid]
                    seen = {key}
                elif cnt == best and key not in seen:
                    seen.add(key)
                    best_grids.append(grid)
    return best, best_grids, e, S


def show(grid):
    roots = [math.isqrt(v) for v in grid]
    for r in range(0, 9, 3):
        print("   " + "  ".join(f"{grid[r+j]:>7} ({roots[r+j]}^2)" for j in range(3)))


if __name__ == "__main__":
    for N in (425,):
        cnt, grids, e, S = search(N)
        print(f"N={N}, center={e}, magic S=3N^2={S}")
        print(f"best lines magic: {cnt} of 8 ; {len(grids)} distinct square(s)\n")
        for g in grids[:4]:
            show(g)
            good = [nm for nm, (x, y, z) in zip(
                ["r1", "r2", "r3", "c1", "c2", "c3", "d\\", "d/"], LINES)
                if g[x] + g[y] + g[z] == S]
            print("   magic lines:", ", ".join(good), "\n")
