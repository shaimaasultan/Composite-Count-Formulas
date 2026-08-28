"""
Search for 3x3 (near) magic squares of squares centered on N**2.

A 3x3 magic square with center e forces every pair of opposite border cells
to sum to 2e, and the magic constant to be 3e. So each usable border pair is
(s, 2e - s) where BOTH s and 2e - s are perfect squares, i.e. a representation
    x**2 + y**2 = 2e = 2*N**2.
Placing 4 such pairs on the 4 axes through the center makes 4 of the 8 lines
(both diagonals, middle row, middle col) automatically magic. The remaining 4
outer lines are the hard part -- a fully magic 3x3 square of 9 distinct
squares is a famous open problem, so the best we expect is 7 of 8 lines.
"""
from itertools import combinations, permutations, product
import math

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]
AXES = [(0, 8), (2, 6), (1, 7), (3, 5)]   # opposite-cell axes through center


def complementary_pairs(N):
    """All (s, 2e-s) with both perfect squares, s < e, e = N**2 (center excluded)."""
    e = N * N
    two_e = 2 * e
    pairs = []
    for x in range(1, N):                 # s = x**2 < e
        rem = two_e - x * x
        y = math.isqrt(rem)
        if y * y == rem and x < y:        # x<y keeps s<e and avoids dupes/center
            pairs.append((x * x, rem))
    return pairs


def search(N, max_pairs=None):
    """Return best (lines_correct, grid) over all placements of 4 pairs."""
    e = N * N
    magic = 3 * e
    pairs = complementary_pairs(N)
    if max_pairs:
        pairs = pairs[:max_pairs]
    best_count, best_grid, best_full = -1, None, []
    grid = [0] * 9
    grid[4] = e
    for four in combinations(pairs, 4):
        for order in permutations(four):
            for orient in product((0, 1), repeat=4):
                for (u, v), pr, o in zip(AXES, order, orient):
                    grid[u], grid[v] = (pr[o], pr[1 - o])
                c = sum(1 for a, b, d in LINES
                        if grid[a] + grid[b] + grid[d] == magic)
                if c > best_count:
                    best_count, best_grid = c, grid[:]
                    best_full = [best_grid]
                elif c == best_count and c >= 7 and grid[:] not in best_full:
                    best_full.append(grid[:])
    return best_count, best_grid, pairs, best_full


def show(grid):
    for r in range(0, 9, 3):
        print("  ", grid[r], grid[r + 1], grid[r + 2])


if __name__ == "__main__":
    N = 425
    e = N * N
    pairs = complementary_pairs(N)
    print(f"N={N}, center e=N^2={e}, magic constant 3e={3*e}")
    print(f"complementary square-pairs (s, 2e-s): {len(pairs)}")
    for p in pairs:
        print("   ", p, "= sqrt", (math.isqrt(p[0]), math.isqrt(p[1])))
    best, grid, _, fulls = search(N)
    print(f"\nBest arrangement: {best} of 8 lines magic")
    show(grid)
    if best >= 7:
        print(f"\n{len(fulls)} distinct arrangement(s) reaching {best}/8:")
        for g in fulls[:3]:
            show(g); print()
