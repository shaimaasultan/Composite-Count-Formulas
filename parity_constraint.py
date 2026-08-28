"""
Section 40 - the mod-8 parity constraint, as a search-pruning layer.

Facts (verified in `verify_lemmas`):
  * n^2 mod 8 in {0, 1, 4};  odd^2 == 1 (mod 8),  even^2 in {0, 4}.
  * Theorem 21: if the centre root k is ODD, every one of the 9 cells is an
    odd square == 1 (mod 8). (Opposite pairs give a^2+b^2 = 2k^2 == 2 (mod 8);
    the only way to write 2 as a sum of two values in {0,1,4} is 1+1, so both
    cells are odd squares == 1.)
  * Corollary 18: if k is EVEN then 2k^2 == 0 (mod 8), every pair is {0,0} or
    {4,4} mod 8, so all cells are divisible by 4; dividing the whole square by
    4 gives a smaller magic square. Hence every magic square of squares reduces
    to a PRIMITIVE one with k odd, in which all nine cells == 1 (mod 8).

Consequences used for pruning:
  1. Only ODD centres k need to be searched (even k -> divide square by 4).
  2. A cell == 1 (mod 8) is necessarily an ODD square, so every border
     candidate must have an odd root. Even-root squares are rejected outright.
  3. mod-10: an odd square ends in 1, 5, or 9, a second cheap sieve.
"""
import math
from squares_around import squares_around


# ---- lemma checks -----------------------------------------------------------

def verify_lemmas(bound=2000):
    sq = {(n * n) % 8 for n in range(bound)}
    odd = {(n * n) % 8 for n in range(1, bound, 2)}
    even = {(n * n) % 8 for n in range(0, bound, 2)}
    assert sq == {0, 1, 4}
    assert odd == {1}
    assert even == {0, 4}
    return {"squares mod 8": sorted(sq), "odd^2 mod 8": sorted(odd),
            "even^2 mod 8": sorted(even)}


# ---- Corollary 18: reduction to a primitive odd centre ----------------------

def reduce_to_primitive(k):
    """Return (k_odd, divisions) where the square has been divided by 4 for
    each halving of k (Corollary 18). k_odd is the primitive centre root."""
    d = 0
    while k % 2 == 0:
        k //= 2          # halving root == dividing the square (k^2) by 4
        d += 1
    return k, d


# ---- Theorem 21: cell sieves ------------------------------------------------

def cell_mod8_ok(v):
    """A primitive-square cell must be == 1 (mod 8)."""
    return v % 8 == 1


def cell_mod10_ok(v):
    """An odd square ends in 1, 5 or 9."""
    return v % 10 in (1, 5, 9)


def odd_square(v):
    r = math.isqrt(v)
    return r * r == v and r % 2 == 1


# ---- pruned border-candidate generator --------------------------------------

def pruned_candidates(N, limit):
    """
    Border-cell candidates for a PRIMITIVE magic square of squares centred on
    N^2 (N odd). Returns (below, above, stats) where each list keeps only the
    odd-root squares that pass the mod-8 (hence mod-10) sieve.
    """
    if N % 2 == 0:
        raise ValueError(f"centre root {N} is even; reduce_to_primitive first "
                         f"-> {reduce_to_primitive(N)}")
    below, above, _, _ = squares_around(N, limit)
    raw = len(below) + len(above)

    def keep(entry):
        v = entry[1]
        return cell_mod8_ok(v) and cell_mod10_ok(v)   # == odd-root square

    b = [e for e in below if keep(e)]
    a = [e for e in above if keep(e)]
    stats = {"raw_candidates": raw, "kept": len(b) + len(a),
             "pruned": raw - (len(b) + len(a))}
    return b, a, stats


def pruned_octet_search(N, limit, k=4):
    """
    The border search of find_octets, restricted by Theorem 21: only odd-root
    squares are eligible. Returns (solutions, combos_full, combos_pruned) so
    the search-space reduction is visible. The pruned solution set is the
    mod-8-ADMISSIBLE subset of the unpruned one: every octet that is dropped
    contains an even-root square, which Theorem 21 forbids in a primitive
    magic square, so no genuine primitive-magic candidate is lost.
    """
    from itertools import combinations
    from math import comb
    target = (2 * k) * N * N
    b, a, _ = pruned_candidates(N, limit)
    b_vals = [x[1] for x in b]
    a_vals = [x[1] for x in a]

    above_by_sum = {}
    for combo in combinations(a_vals, k):
        above_by_sum.setdefault(sum(combo), []).append(combo)

    sols = []
    for lo in combinations(b_vals, k):
        for hi in above_by_sum.get(target - sum(lo), ()):
            sols.append(list(lo) + list(hi))

    # unpruned pool size for comparison
    below, above, _, _ = squares_around(N, limit)
    full = comb(len(below), k) * comb(len(above), k)
    pruned = comb(len(b_vals), k) * comb(len(a_vals), k)
    return sols, full, pruned


def find_below_roots(N):
    """
    Discover the four below-square roots that build a magic square of squares
    centred on N**2 -- no hard-coded list.

    Every 3x3 magic square with centre e is determined by two gap parameters
    (p, q); its four opposite-cell spokes have gaps |p|, |q|, |p+q|, |2p+q|,
    and cell = e +/- gap. We take two spokes to be both-square complementary
    pairs (s, 2e-s) [from `complementary_pairs`], solve for (p, q), then keep
    the cases whose remaining two spokes also have a perfect-square below cell.
    Returns a sorted list of distinct 4-root solutions.
    """
    from magic_search import complementary_pairs
    e = N * N
    gaps = [e - s for (s, _) in complementary_pairs(N)]   # both-square gaps

    def below_root(g):
        v = e - g
        r = math.isqrt(v)
        return r if (0 < v and r * r == v) else None

    found = set()
    for gp in gaps:                      # gap for parameter p
        for g2 in gaps:                  # gap for 2p+q
            if g2 == gp:
                continue
            for p in (gp, -gp):
                for t2 in (g2, -g2):     # 2p+q = +/- g2
                    q = t2 - 2 * p
                    gq, gpq = abs(q), abs(p + q)
                    if gq == 0 or gpq == 0 or gq >= e or gpq >= e:
                        continue
                    rq, rpq = below_root(gq), below_root(gpq)
                    if rq is None or rpq is None:
                        continue
                    roots = {below_root(gp), below_root(g2), rq, rpq}
                    if None not in roots and len(roots) == 4:
                        found.add(tuple(sorted(roots)))
    return sorted(found)


def build_cells(N, below_roots):
    """
    Build the 9 cells of a candidate square from four below-square roots,
    without hard-coding any values. Each below square s = r**2 (< N**2) is
    paired with its opposite cell 2*N**2 - s (so every pair sums to 2*centre).
    Returns (border_cells, centre).
    """
    e = N * N
    border = []
    for r in below_roots:
        s = r * r
        if s >= e:
            raise ValueError(f"root {r} is not below N={N}")
        border.append(s)                 # the below square
        border.append(2 * e - s)         # its above complement (2N^2 - s)
    return border, e


def arrange_magic(border, centre):
    """Search border permutations for the best magic arrangement.
    Returns (lines_correct, grid) with grid[4] == centre."""
    from itertools import permutations
    S = 3 * centre
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
             (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    slots = [0, 1, 2, 3, 5, 6, 7, 8]
    grid = [0] * 9
    grid[4] = centre
    best = (-1, None)
    for p in permutations(border):
        for pos, v in zip(slots, p):
            grid[pos] = v
        c = sum(1 for a, b, d in lines if grid[a] + grid[b] + grid[d] == S)
        if c > best[0]:
            best = (c, grid[:])
            if c == 8:
                break
    return best


def print_table(grid, centre):
    """Pretty-print the 3x3 square as a table (root^2 form, value below)."""
    S = 3 * centre

    def label(v):
        r = math.isqrt(v)
        return f"{r}^2" if r * r == v else f"{v}*"   # * = not a perfect square

    bar = "+" + "+".join(["-" * 22] * 3) + "+"
    print(bar)
    for r in range(0, 9, 3):
        top = "|" + "|".join(f"{label(grid[r+j]):^22}" for j in range(3)) + "|"
        val = "|" + "|".join(f"{grid[r+j]:^22}" for j in range(3)) + "|"
        print(top)
        print(val)
        print(bar)
    print(f"magic constant = {S}   (* = non-square cell)")


if __name__ == "__main__":
    print("lemmas:", verify_lemmas())
    # print("reduce_to_primitive(850) =", reduce_to_primitive(850),
    #       " reduce_to_primitive(425) =", reduce_to_primitive(425))

    N, limit = 425, 60
    b, a, stats = pruned_candidates(N, limit)
    print(f"\nN={N}, limit={limit}: {stats}")
    print("kept below roots:", [math.isqrt(x[1]) for x in b][:12], "...")
    print("kept above roots:", [math.isqrt(x[1]) for x in a][:12], "...")

    # the classic k=425 near-square: the four below-square roots are now
    # DISCOVERED, not hard-coded. Each below square r^2 pairs with 2N^2 - r^2.
    solutions = find_below_roots(N)
    print("\ndiscovered below-root solutions:", solutions)
    if len(solutions) > 0:
        below_roots = list(solutions[0])
        print("using below_roots =", below_roots)
        border, centre = build_cells(N, below_roots)
        cells = border + [centre]
        print("\nderived cells:", cells)
        print(f"classic k={N} cells == 1 (mod 8):", all(cell_mod8_ok(c) for c in cells))
        print("... mod 10 endings:", [c % 10 for c in cells])

        lines, grid = arrange_magic(border, centre)
        print(f"\nmagic square of squares (centre 425^2): {lines} of 8 lines correct")
        print_table(grid, centre)

    # sieve applied to the octet search: same solutions, far smaller space
    from squares_around import find_octets
    sols, full, pruned = pruned_octet_search(N, limit)
    unpruned = len(find_octets(N, limit))
    print(f"\noctet search @ N={N}, limit={limit}:")
    print(f"  sum-valid octets unpruned={unpruned}  mod-8 admissible={len(sols)} "
          f"({unpruned/len(sols):.1f}x fewer to test)")
    print(f"  4+4 combo pool: full={full:,}  pruned={pruned:,} "
          f"(x{full/pruned:.1f} smaller)")
    # confirm every pruned solution is genuinely all-odd-square and == 1 mod 8
    assert all(odd_square(v) and cell_mod8_ok(v) for s in sols for v in s)
    print("  all pruned octet cells are odd squares == 1 (mod 8): verified")
