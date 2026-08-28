"""
Search a magic square of squares by hunting from the ABOVE odd-square list.

Every 3x3 magic square with centre e = N**2 is fixed by two gap parameters
(p, q); the eight border cells are e +/- p, e +/- q, e +/- (p+q), e +/- (2p+q),
and EVERY such (p, q) already makes a full 8/8 magic square. So the only thing
to maximise is how many of those cells are perfect squares (record: 7 of 9).

Strategy (mirrors the "look from above" idea):
  * list odd squares ABOVE N**2; each t**2 gives a gap g = t**2 - e, and the
    cell e + g is guaranteed square.
  * use two of those above-square gaps to seed the p-spoke and the (2p+q)-spoke.
  * solve for (p, q). The opposite (below) cells and the other two spokes fall
    out automatically -- their complements sum to 2*e but need NOT be squares.
  * count the perfect squares among the 9 cells and keep the best.
Nothing is imported from the other files.
"""
import math


def above_odd_squares(N, limit):
    """[(root, square, gap)] for odd roots just above N, nearest first."""
    e = N * N
    r = N + 1 if (N + 1) % 2 else N + 2      # first odd root above N
    out = []
    while len(out) < limit:
        out.append((r, r * r, r * r - e))
        r += 2
    return out


def is_square(v):
    if v < 0:
        return False
    r = math.isqrt(v)
    return r * r == v


def grid_from_pq(e, p, q):
    """The canonical 3x3 magic square with centre e and parameters (p, q)."""
    return [e + p,       e + q,       e - p - q,
            e - 2*p - q, e,           e + 2*p + q,
            e + p + q,   e - q,       e - p]


def search_from_above(N, limit, want=7):
    """
    Return arrangements (square_count, p, q, grid) with >= `want` square cells,
    seeding the two free spokes from the above odd-square gaps. Best first.
    """
    e = N * N
    gaps = [g for (_, _, g) in above_odd_squares(N, limit)]
    results, seen = [], set()
    for g1 in gaps:                       # p-spoke gap (an above square)
        for g2 in gaps:                   # (2p+q)-spoke gap (an above square)
            if g2 == g1:
                continue
            for p in (g1, -g1):
                for t2 in (g2, -g2):
                    q = t2 - 2 * p
                    spokes = [p, q, p + q, 2 * p + q]
                    if any(x == 0 for x in spokes):
                        continue
                    if len({abs(x) for x in spokes}) != 4:   # 4 distinct gaps
                        continue
                    grid = grid_from_pq(e, p, q)
                    if any(c <= 0 for c in grid):
                        continue
                    nsq = sum(is_square(c) for c in grid)
                    if nsq >= want:
                        key = tuple(sorted(grid))
                        if key in seen:
                            continue
                        seen.add(key)
                        results.append((nsq, p, q, grid))
    results.sort(key=lambda t: -t[0])
    return results


def print_table(grid, centre):
    S = 3 * centre

    def label(v):
        r = math.isqrt(v)
        return f"{r}^2" if r * r == v else f"{v}*"

    bar = "+" + "+".join(["-" * 22] * 3) + "+"
    print(bar)
    for r in range(0, 9, 3):
        print("|" + "|".join(f"{label(grid[r+j]):^22}" for j in range(3)) + "|")
        print("|" + "|".join(f"{grid[r+j]:^22}" for j in range(3)) + "|")
        print(bar)
    print(f"magic constant = {S}   (* = non-square cell)")


if __name__ == "__main__":
    N, limit = 5**2*129, 1000
    e = N * N
    hits = search_from_above(N, limit, want=6)
    print(f"N={N}, scanning {limit} above odd squares "
          f"(roots {N+2}..{N+2*limit}) for >=7 square cells")
    print(f"arrangements found: {len(hits)}\n")
    if hits:
        nsq, p, q, grid = hits[0]
        # show which above squares seeded it
        seeds = sorted({math.isqrt(c) for c in grid
                        if c > e and is_square(c)})
        print(f"best: {nsq} of 9 cells are squares  (p={p}, q={q})")
        print(f"above squares used as seeds: {[f'{r}^2' for r in seeds]}")
        print_table(grid, e)
