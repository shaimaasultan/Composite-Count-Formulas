"""
Build a magic square of squares from complementary pairs around the centre N**2.

Idea (Theorem 21 world, k = N odd so all cells are odd squares == 1 mod 8):
  * `above` = odd squares strictly ABOVE N**2.
  * every cell has an opposite cell across the centre: complement(v) = 2*N**2 - v,
    so an above square's partner sits BELOW N**2 (and vice versa).
  * pick 4 cells from one side; their 4 complements fill the other side.
    Those 8 values are the border; N**2 is the centre. Arrange and print.

For a given centre only one side is guaranteed to be all perfect squares
(for N=425 that's the BELOW side: roots 23,205,289,373 -- two of their above
complements, 360721 and 222121, are not squares). So we pick from whichever
side is all-squares; `below_roots`/`above_roots` are just the roots of the
squares on whichever side we took them from.
"""
import math
from parity_constraint import (find_below_roots, build_cells,
                               arrange_magic, print_table)


def odd_squares_above(N, limit):
    """Odd squares strictly above N**2, nearest first, up to `limit` of them."""
    r = N + 1 if (N + 1) % 2 else N + 2      # first odd root above N
    out = []
    while len(out) < limit:
        out.append([r, r * r])               # [root, square]
        r += 2
    return out


def odd_squares_below(N, limit):
    """Odd squares strictly below N**2, nearest first, up to `limit` of them."""
    r = N - 1 if (N - 1) % 2 else N - 2      # first odd root below N
    out = []
    while len(out) < limit and r >= 1:
        out.append([r, r * r])
        r -= 2
    return out


def complement(value, N):
    """The opposite cell across the centre: below <-> above (pair sums to 2N**2)."""
    return 2 * N * N - value


def complete_from(N, chosen_values):
    """
    Given 4 chosen cell values on one side, compute the 4 complements on the
    other side, then build and arrange the square. Returns (lines, grid).
    """
    if len(chosen_values) != 4:
        raise ValueError("need exactly 4 chosen values")
    others = [complement(v, N) for v in chosen_values]
    border = list(chosen_values) + others
    return arrange_magic(border, N * N)


def is_square(v):
    r = math.isqrt(v)
    return r * r == v


if __name__ == "__main__":
    N = 425
    e = N * N

    # 1) the two complementary pools around the centre
    print(f"centre N^2 = {e}")
    print("odd squares ABOVE (nearest 4):", [s for _, s in odd_squares_above(N, 4)])
    print("their BELOW complements     :", [complement(s, N)
                                            for _, s in odd_squares_above(N, 4)])

    # 2) discover the 4 all-square roots (here they land on the BELOW side)
    below_roots = list(find_below_roots(N)[0])
    below_squares = [r * r for r in below_roots]
    above_complements = [complement(s, N) for s in below_squares]
    print(f"\nchosen below_roots (all squares): {below_roots}")
    print(f"below squares (< N^2): {below_squares}")
    print(f"above complements (2N^2 - s): {above_complements}"
          f"  <- squares? {[is_square(v) for v in above_complements]}")

    # 3) build the square from the 4 below squares + their above complements
    lines, grid = complete_from(N, below_squares)
    print(f"\nmagic square of squares (centre {N}^2): {lines} of 8 lines correct")
    print_table(grid, e)
