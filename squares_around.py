import math
from itertools import combinations


def squares_around(N, limit):
    """
    Center the search on N**2 and return two lists of [index, square]:
      - below: squares strictly less than N**2, starting from the largest
               one below N**2 and moving down (index 1, 2, 3, ...)
      - above: squares strictly greater than N**2, starting from the least
               one above N**2 and moving up (index 1, 2, 3, ...)
    Each list contains up to `limit` entries. The center N**2 itself is
    excluded. Also returns the gap lists (N**2 - square) used to balance
    sums around N**2.
    """
    M = N * N                        # center of the search
    r = math.isqrt(M)                # floor(sqrt(M)) == N
    left_k = r if r * r < M else r - 1   # largest k with k*k < M
    right_k = r + 1                      # smallest k with k*k > M

    below = [[i + 1, (left_k - i) ** 2]
             for i in range(limit) if left_k - i >= 1]
    below_gaps = [[x[0], x[1], M - x[1]] for x in below]
    above = [[i + 1, (right_k + i) ** 2]
             for i in range(limit)]
    above_gaps = [[x[0], x[1], M - x[1]] for x in above]

    return below, above, below_gaps, above_gaps


def find_octets(N, limit, target=None, k=4):
    """
    Choose `k` values from the below list and `k` from the above list so all
    2*k chosen numbers sum to `target` (default 8*N for k=4).

    Returns a list of solutions; each solution is a dict with the chosen
    below values, above values, all values, and the confirmed sum.
    """
    if target is None:
        target = (2 * k) * N * N

    below, above, _, _ = squares_around(N, limit)
    b_vals = [x[1] for x in below]
    a_vals = [x[1] for x in above]

    # meet-in-the-middle: index all k-subset sums of the above list
    above_by_sum = {}
    for a in combinations(a_vals, k):
        above_by_sum.setdefault(sum(a), []).append(a)

    results = []
    for b in combinations(b_vals, k):
        need = target - sum(b)
        for a in above_by_sum.get(need, ()):
            results.append({
                "below": list(b),
                "above": list(a),
                "all": list(b) + list(a),
                "sum": target,
            })
    return results


def octet_roots(N, limit, target=None, k=4):
    """
    Same search as find_octets, but return each solution as the integer roots
    A,B,C,D,F,G,H,I of the 8 border squares (E = N is the center root, omitted).

    Guarantees the identity requested:
        (A^2 + B^2 + C^2 + D^2 + F^2 + G^2 + H^2 + I^2) / 8 == N^2
    i.e. the mean of the eight border squares equals the center N^2.
    """
    letters = ["A", "B", "C", "D", "F", "G", "H", "I"]  # E is the center
    out = []
    for s in find_octets(N, limit, target, k):
        vals = s["all"]
        roots = [math.isqrt(v) for v in vals]
        assert all(r * r == v for r, v in zip(roots, vals))     # all perfect squares
        assert sum(vals) == 8 * N * N                            # mean of squares == N^2
        out.append({
            "roots": dict(zip(letters, roots)),
            "squares": vals,
            "mean_of_squares": sum(vals) // 8,   # == N**2
        })
    return out


if __name__ == "__main__":
    N, limit = 425, 20
    target = 8 * N * N
    sols = find_octets(N, limit, target)
    print(f"N={N}, limit={limit}, target=8*N^2={target}")
    print(f"found {len(sols)} solution(s)")
    for s in sols[:10]:
        print(s["below"], "+", s["above"], "=", s["sum"])
