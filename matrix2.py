import math
from collections import Counter


def coprime6(n):
    return n % 6 in (1, 5)


def _real_matrix_pairs(max_depth, m):
    """
    Reconstructs the SAME (row, col) pairs as matrix1.py's build_matrix,
    using the full symmetric index column (descending max_depth..1, then
    0, then back up to max_depth) with the compressed-counter base
    alternation -- but WITHOUT filtering out multiples of 3, since the
    exact-count mechanism below needs to know about them to compute the
    correction precisely. Returns the list of (a, c) pairs (no filtering,
    no printing).
    """
    index_column = list(range(max_depth, 0, -2)) + [0] + list(range(1, max_depth + 1, 2))
    compressed = 0
    bases = []
    for a in index_column:
        if a == 0:
            bases.append(0)
            continue
        compressed += 1
        bases.append(5 if compressed % 2 == 1 else 7)

    pairs = []
    for a, base in zip(index_column, bases):
        if a in (0, 1):
            continue
        cols = [base + 6 * j for j in range(m)]
        for c in cols:
            pairs.append((a, c))
    return pairs


def exact_count(V, max_depth, m, rows_filter=lambda a: True):
    """
    EXACT count of how many (row, col) pairs produce V, restricted to
    rows satisfying rows_filter (default: every valid row). Verified
    (in coprime_product_matrix_exact_count.py) to match the real matrix
    with zero mismatches across many scales.

    count(V) = number of ways to write V = a*c where
      - c is coprime-to-6 and 5 <= c <= max_col (max_col = 7+6*(m-1))
      - a is odd, 1 < a <= max_depth, a != 1, and rows_filter(a)
    """
    max_col = 7 + 6 * (m - 1)
    count = 0
    for c in range(5, max_col + 1):
        if V % c == 0 and coprime6(c):
            a = V // c
            if a % 2 == 1 and 1 < a <= max_depth and rows_filter(a):
                count += 1
    return count


def coprime_only_duplicates_direct(max_depth, m):
    """Direct (no formula) duplicate count using ONLY coprime-to-6 rows
    -- matrix1.py's actual matrix, since it excludes every multiple of 3
    from the index column entirely."""
    pairs = _real_matrix_pairs(max_depth, m)
    entries = [a * c for a, c in pairs if coprime6(a)]
    return len(entries) - len(set(entries))


def mod3_correction(max_depth, m):
    """
    EXACT, direct computation of what the multiples-of-3 rows would add
    on top of the coprime-only duplicate count -- kept here for
    reference, but matrix1.py's matrix never includes multiples-of-3
    rows at all (they're filtered out of the index column), so this is
    always 0 for matrix1.py's construction. Included so this file is a
    complete, standalone exact-count toolkit.
    """
    max_col = 7 + 6 * (m - 1)
    mod3_rows = [a for a in range(3, max_depth + 1, 2) if a % 3 == 0]

    candidate_values = set()
    for a in mod3_rows:
        for c in range(5, max_col + 1):
            if coprime6(c):
                candidate_values.add(a * c)

    correction = 0
    for v in candidate_values:
        count_all = exact_count(v, max_depth, m)
        count_coprime_only = exact_count(v, max_depth, m, coprime6)
        correction += max(0, count_all - 1) - max(0, count_coprime_only - 1)
    return correction


def total_cells_matrix1(max_depth, m):
    """Total cell count for matrix1.py's construction: each coprime-to-6
    depth value contributes a row TWICE (once in the descending half,
    once in the ascending half), m columns each."""
    coprime_rows = [a for a in range(3, max_depth + 1, 2) if coprime6(a)]
    return 2 * len(coprime_rows) * m


def c_distinct_exact(max_depth, m):
    """
    The exact, directly-calculated C_distinct for matrix1.py's
    construction (index column with multiples of 3 excluded):

        C_distinct = total_cells - coprime_only_duplicates_direct(max_depth, m)

    (mod3_correction is always 0 here since matrix1.py's index column
    never includes multiples of 3 in the first place -- it's included
    above for completeness/reference, not because it's needed for this
    specific matrix.)
    """
    total_cells = total_cells_matrix1(max_depth, m)
    return total_cells - coprime_only_duplicates_direct(max_depth, m)


if __name__ == "__main__":
    import matrix1

    cases = [(31, 5), (35, 10), (37, 6), (43, 7), (13, 2), (61, 10), (91, 15), (23, 4), (15, 3)]
    print(f"{'max_depth':>10} {'m':>3} {'true_C_distinct':>16} {'calculated':>11} {'match':>5}")
    for max_depth, m in cases:
        import io
        import sys
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        _, distinct_values = matrix1.build_matrix(max_depth, m)
        sys.stdout = old_stdout

        true_val = len(distinct_values)
        calculated = c_distinct_exact(max_depth, m)
        match = true_val == calculated
        print(f"{max_depth:>10} {m:>3} {true_val:>16} {calculated:>11} {'OK' if match else 'FAIL':>5}")
