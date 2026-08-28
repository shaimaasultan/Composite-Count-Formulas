"""
Self-contained builder: ONE pool of below odd squares -> pick 4 -> print square.

Lemma (Section 40): squares mod 8 in {0,1,4}; odd^2 == 1 (mod 8); even^2 in {0,4}.
So for an odd centre k = N every cell is an odd square == 1 (mod 8). We build a
single pool of odd squares strictly BELOW N**2. The matching ABOVE cell of any
pool member falls out automatically as its complement 2*N**2 - s (no second
list to maintain). Choosing 4 squares from the below pool fixes their 4 above
complements; those 8 values are the border and N**2 is the centre.

Everything needed (pool, complement, discovery of the working 4, arrange, print)
lives in this file -- nothing is imported from the other modules.
"""
import math
from itertools import permutations


# --------------------------------------------------------------------------
# the single pool: odd squares below N**2  (above complements are implicit)
# --------------------------------------------------------------------------
def below_pool(N, limit=None):
    """[ [root, square], ... ] for odd roots N-1, N-3, ... (squares < N**2)."""
    r = N - 1 if (N - 1) % 2 else N - 2
    pool = []
    while r >= 1 and (limit is None or len(pool) < limit):
        pool.append([r, r * r])
        r -= 2
    return pool


def complement(value, N):
    """The opposite (above) cell of a below value: pair sums to 2*N**2."""
    return 2 * N * N - value


def is_square(v):
    r = math.isqrt(v)
    return r * r == v


def _factor(n):
    """Simple prime factorization, for the 'why no square' explanation."""
    f, d = [], 2
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f


# --------------------------------------------------------------------------
# which 4 pool members build the magic square (self-contained discovery)
# --------------------------------------------------------------------------
def _complementary_pairs(N):
    """(s, 2e-s) with both perfect squares, s < e = N**2."""
    e = N * N
    out = []
    for x in range(1, N):
        s = x * x
        if s >= e:
            break
        rem = 2 * e - s
        y = math.isqrt(rem)
        if y * y == rem:
            out.append((s, rem))
    return out


def find_below_roots(N):
    """Discover four below-square roots that build a magic square centred N**2.
    A 3x3 magic square is fixed by two gap parameters (p, q); its spokes have
    gaps |p|,|q|,|p+q|,|2p+q|. Two spokes take both-square complementary pairs;
    solve for (p,q) and keep cases whose other two spokes also hit below-squares."""
    e = N * N
    gaps = [e - s for (s, _) in _complementary_pairs(N)]

    def broot(g):
        v = e - g
        r = math.isqrt(v)
        return r if (0 < v and r * r == v) else None

    found = set()
    for gp in gaps:
        for g2 in gaps:
            if g2 == gp:
                continue
            for p in (gp, -gp):
                for t2 in (g2, -g2):
                    q = t2 - 2 * p
                    gq, gpq = abs(q), abs(p + q)
                    if gq == 0 or gpq == 0 or gq >= e or gpq >= e:
                        continue
                    rq, rpq = broot(gq), broot(gpq)
                    if rq is None or rpq is None:
                        continue
                    roots = {broot(gp), broot(g2), rq, rpq}
                    if None not in roots and len(roots) == 4:
                        found.add(tuple(sorted(roots)))
    return sorted(found)


# --------------------------------------------------------------------------
# build + print
# --------------------------------------------------------------------------
def build_from_below(N, chosen_squares):
    """Given 4 below squares, complement to the above side, arrange the square.
    Returns (lines_correct, grid)."""
    if len(chosen_squares) != 4:
        raise ValueError("pick exactly 4 below squares from the pool")
    border = list(chosen_squares) + [complement(s, N) for s in chosen_squares]
    centre = N * N
    S = 3 * centre
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
             (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    slots = [0, 1, 2, 3, 5, 6, 7, 8]
    grid = [0] * 9
    grid[4] = centre
    best = (-1, None)
    for perm in permutations(border):
        for pos, v in zip(slots, perm):
            grid[pos] = v
        c = sum(1 for a, b, d in lines if grid[a] + grid[b] + grid[d] == S)
        if c > best[0]:
            best = (c, grid[:])
            if c == 8:
                break
    return best


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
    N = 195364#  5**3*29*37
    e = N * N

    # 1) the single below pool (above complements are implicit)
    pool = below_pool(N)
    pool_squares = {s for _, s in pool}
    print(f"N = {N} , N**2 = {e} , below pool: {len(pool)} odd squares < {e}  "
          f"(nearest roots {[r for r, _ in pool[:6]]} ...)")

    # 2) choose 4 from THIS pool (discovered; you could also pick by hand)
    solutions = find_below_roots(N)
    if not solutions:
        pairs = _complementary_pairs(N)
        fac = " * ".join(map(str, _factor(N)))
        print(f"\nNo magic square of squares exists for centre {N}^2  (= {N} = {fac}).")
        print(f"The below pool is fine ({len(pool)} squares). Two things are needed:")
        if len(pairs) < 2:
            print(f"  NECESSARY (fails): need >= 2 complementary both-square pairs")
            print(f"  (s, 2N^2 - s), but N has only {len(pairs)}. Such pairs are ways")
            print(f"  to write 2*N^2 as a sum of two squares, governed by the primes")
            print(f"  == 1 (mod 4) in N. Add more of them (5, 13, 17, 29, 37, ...).")
        else:
            print(f"  NECESSARY (ok): N has {len(pairs)} complementary both-square pairs.")
            print(f"  SUFFICIENT (fails): no two pairs align into the magic (p, q)")
            print(f"  structure -- i.e. supply gaps p and 2p+q while the induced gaps")
            print(f"  q and p+q ALSO land on perfect squares. That simultaneous")
            print(f"  4-square coincidence is rare; 425 hits it, this centre does not.")
        raise SystemExit(0)

    roots = list(solutions[0])
    chosen = [r * r for r in roots]
    assert all(s in pool_squares for s in chosen), "chosen squares must be in the pool"
    print(f"chosen 4 below roots (from pool): {roots}")
    print(f"below squares : {chosen}")
    print(f"above (auto)  : {[complement(s, N) for s in chosen]} "
          f"-> squares? {[is_square(complement(s, N)) for s in chosen]}")

    # 3) build & print
    lines, grid = build_from_below(N, chosen)
    print(f"\nmagic square of squares (centre {N}^2): {lines} of 8 lines correct")
    print_table(grid, e)
