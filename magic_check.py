"""
Check whether an octet of 8 squares (4 below + 4 above N**2) can be arranged,
with N**2 in the center, into a 3x3 magic square of squares.

Grid positions:
    p0 p1 p2
    p3 p4 p5      (p4 = center = N**2)
    p6 p7 p8

The 8 "lines": 3 rows, 3 cols, 2 diagonals. A true magic square has all 8
lines equal to the magic constant 3*center. "Near magic" = as many lines as
possible are correct.
"""
from itertools import permutations

# (indices into the 9-cell grid) for each of the 8 lines
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]
BORDER = [0, 1, 2, 3, 5, 6, 7, 8]      # positions to fill (center is p4)


def best_arrangement(octet, center):
    """Return (max_lines_correct, grid) over all border arrangements."""
    magic = 3 * center
    mn = min(octet)
    best_count, best_grid = -1, None
    grid = [0] * 9
    grid[4] = center
    for perm in permutations(octet):
        if perm[0] != mn:            # fix one corner = min: kills 8x symmetry
            continue
        for pos, v in zip(BORDER, perm):
            grid[pos] = v
        c = sum(1 for a, b, d in LINES if grid[a] + grid[b] + grid[d] == magic)
        if c > best_count:
            best_count, best_grid = c, grid[:]
            if c == 8:
                return best_count, best_grid
    return best_count, best_grid


def pair_structure(octet, center):
    """How many opposite-cell pairs summing to 2*center exist (max 4)."""
    need = 2 * center
    vals = sorted(octet)
    used = [False] * len(vals)
    pairs = 0
    for i in range(len(vals)):
        if used[i]:
            continue
        for j in range(i + 1, len(vals)):
            if not used[j] and vals[i] + vals[j] == need:
                used[i] = used[j] = True
                pairs += 1
                break
    return pairs


if __name__ == "__main__":
    N = 425
    center = N * N

    given = [
        [179776, 170569, 164836, 164025, 183184, 189225, 196249, 197136],
        [179776, 169744, 165649, 164025, 181476, 193600, 194481, 196249],
        [179776, 169744, 164836, 164025, 186624, 187489, 194481, 198025],
        [179776, 168921, 166464, 164025, 181476, 192721, 194481, 197136],
        [179776, 168921, 166464, 164025, 182329, 190096, 195364, 198025],
        [179776, 168921, 166464, 164025, 183184, 188356, 196249, 198025],
        [179776, 168921, 165649, 164025, 183184, 193600, 194481, 195364],
        [179776, 168921, 164836, 164025, 186624, 190969, 193600, 196249],
        [179776, 168921, 164836, 164025, 187489, 190096, 192721, 197136],
        [179776, 168100, 166464, 164025, 183184, 192721, 194481, 196249],
    ]

    print(f"center N^2 = {center}, magic constant 3*N^2 = {3*center}")
    print(f"{'#':>2} {'pairs(=2N^2)':>12} {'max_lines/8':>12}")
    for i, oc in enumerate(given, 1):
        pairs = pair_structure(oc, center)
        lines, grid = best_arrangement(oc, center)
        print(f"{i:>2} {pairs:>12} {lines:>12}")
