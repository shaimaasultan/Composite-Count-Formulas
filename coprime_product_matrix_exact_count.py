import math
from collections import Counter, defaultdict


def coprime6(n):
    return n % 6 in (1, 5)


def build_matrix(max_depth, m):
    """
    Same construction as coprime_product_matrix.py:
      - index column: full symmetric list, descending max_depth..1, then 0,
        then back up to max_depth.
      - base column: alternates 5,7,5,7,... but the zero row doesn't
        consume a step -- it shows 0 and the alternation resumes on the
        next row exactly where it left off.
      - the three middle rows (1, 0, 1) contribute no matrix cells.
      - every other row's m columns are 5 consecutive branch values,
        stepping by 6, starting at that row's base.
      - each cell = row_value * column_value.

    Prints the index column, the per-row columns (0 for the zero row),
    the sorted list of all entries, the sorted distinct values, and every
    repeated value with its count -- same as coprime_product_matrix.py.

    Returns (all_entries, distinct_values).
    """
    if max_depth < 3 or max_depth % 2 == 0:
        raise ValueError("max_depth must be an odd integer >= 3")

    index_column = list(range(max_depth, 0, -2)) + [0] + list(range(1, max_depth + 1, 2))
    print(index_column)

    compressed = 0
    bases = []
    for a in index_column:
        if a == 0:
            bases.append(0)
            continue
        compressed += 1
        bases.append(5 if compressed % 2 == 1 else 7)

    all_entries = []
    for a, base in zip(index_column, bases):
        if a == 0:
            cols = 0  # the zero row: a single 0, not a 5-wide list
            print(cols)
            continue
        cols = [base + 6 * j for j in range(m)]
        print(cols)
        if a == 1:
            continue  # the two a=1 rows still show real cols, but
                       # contribute no matrix cells (same as the zero row)
        for c in cols:
            all_entries.append(a * c)

    distinct_values = set(all_entries)

    print(sorted(all_entries))
    print(sorted(distinct_values))

    counts = Counter(all_entries)
    repeated = {v: c for v, c in counts.items() if c > 1}
    print("repeated values (value: count):")
    for v in sorted(repeated):
        print(f"  {v}: {repeated[v]}")

    return all_entries, distinct_values


def exact_count(V, max_depth, m):
    """
    EXACT formula for how many times V appears in the matrix, verified
    with zero mismatches across many (max_depth, m) scales:

    count(V) = number of ways to write V = a*c where
      - c is coprime-to-6 and 5 <= c <= max_col (a valid column value,
        max_col = 7 + 6*(m-1), independent of max_depth)
      - a is odd, 1 < a <= max_depth, a != 1 (a valid row value -- rows
        can be ANY odd number, not just coprime-to-6, but the two a=1
        rows and the a=0 row never contribute)

    This works because columns are always coprime-to-6 (base is always
    5 or 7, and stepping by 6 preserves that residue class forever),
    while rows can be any odd number including multiples of 3 -- so a
    factor pair where one side is divisible by 3 can only ever appear in
    ONE direction (the multiple-of-3 side can never sit in the column
    position), while a factor pair where both sides are coprime-to-6 can
    appear in both directions.
    """
    max_col = 7 + 6 * (m - 1)
    count = 0
    for c in range(5, max_col + 1):
        if V % c == 0 and coprime6(c):
            a = V // c
            if a % 2 == 1 and 1 < a <= max_depth:
                count += 1
    return count


def verify_exact_count(max_depth, m, all_entries=None, distinct_values=None):
    """Checks exact_count() against the real matrix for every distinct
    value, printing any mismatches found. Returns the mismatch count."""
    if all_entries is None or distinct_values is None:
        all_entries, distinct_values = build_matrix(max_depth, m)

    counts = Counter(all_entries)
    mismatches = 0
    for V in distinct_values:
        actual = counts[V]
        predicted = exact_count(V, max_depth, m)
        if actual != predicted:
            mismatches += 1
            print(f"  MISMATCH V={V}: actual={actual} predicted={predicted}")

    print(f"checked {len(distinct_values)} distinct values, mismatches={mismatches}")
    return mismatches


def base_formula(m):
    """The LaTeX document's original correction term: sum_{i=1}^{2m-1} i.

    NOTE -- verified NOT to equal the true coprime-only duplicate count in
    general (only matches by coincidence at a couple of small cases, see
    coprime_only_duplicates_direct() below). Kept here for reference /
    comparison against the earlier LaTeX formula, not as a trusted term.
    """
    return (2 * m - 1) * (2 * m) // 2


def exact_count_filtered(V, max_depth, m, rows_filter):
    """Same as exact_count(), but only counting rows a that satisfy
    rows_filter(a) -- e.g. rows_filter=coprime6 restricts to coprime-to-6
    rows only (excludes every multiple of 3)."""
    max_col = 7 + 6 * (m - 1)
    count = 0
    for c in range(5, max_col + 1):
        if V % c == 0 and coprime6(c):
            a = V // c
            if a % 2 == 1 and 1 < a <= max_depth and rows_filter(a):
                count += 1
    return count


def _real_matrix_entries(max_depth, m):
    """Same construction as build_matrix(), but silent (no printing) and
    returns the (a, c) pairs, not just the products -- used internally so
    other functions can reuse the EXACT real row/base assignment
    (the compressed-counter logic) instead of a simplified approximation."""
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


def coprime_only_duplicates_direct(max_depth, m):
    """Direct computation (no formula) of the duplicate count using ONLY
    coprime-to-6 rows -- the true baseline, since base_formula(m) does not
    reliably equal this. Uses the REAL row/base assignment (via
    _real_matrix_entries), just excluding multiples-of-3 rows'
    contributions -- not a simplified/approximate row-column pairing."""
    pairs = _real_matrix_entries(max_depth, m)
    entries = [a * c for a, c in pairs if coprime6(a)]
    return len(entries) - len(set(entries))


def mod3_correction(max_depth, m):
    """
    EXACT, direct computation (not a curve fit, not an approximation) of
    what the multiples-of-3 rows (3, 9, 15, 21, ...) add on top of the
    coprime-only duplicate count.

    For every value V that at least one multiples-of-3 row can produce,
    compares exact_count_filtered(V, rows_filter=<all>) against
    exact_count_filtered(V, rows_filter=coprime6): the difference in each
    value's "excess" (count-1, floored at 0) sums to exactly the gap
    between the true total duplicate count and the true coprime-only
    duplicate count.

    Verified to match (actual_total_duplicates - coprime_only_duplicates)
    exactly, across every (max_depth, m) tested.
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
        count_all = exact_count_filtered(v, max_depth, m, lambda a: True)
        count_coprime_only = exact_count_filtered(v, max_depth, m, coprime6)
        correction += max(0, count_all - 1) - max(0, count_coprime_only - 1)
    return correction


def c_distinct_direct(max_depth, m):
    """
    C_distinct built from two directly-computed (exact, verified) pieces:
      total_cells - coprime_only_duplicates_direct(max_depth, m)
                  - mod3_correction(max_depth, m)

    Neither piece is a closed-form polynomial in max_depth/m -- both are
    exact direct computations -- but this cleanly separates "the coprime-
    to-6 collision structure" from "what multiples-of-3 rows add", which
    base_formula(m) alone could not do reliably.
    """
    total_cells = len(_real_matrix_entries(max_depth, m))
    return total_cells - coprime_only_duplicates_direct(max_depth, m) - mod3_correction(max_depth, m)


def correction_table(cases, verbose=False):
    """
    For each (max_depth, m) in cases:
      - N = max_depth (confirmed: total cells = m*(N-1) exactly)
      - base = base_formula(m)                  -- the LaTeX formula's term
      - actual_dup = true duplicates removed, computed directly from the
        real matrix (no formula, just built and counted)
      - correction = actual_dup - base           -- what's still missing
      - C_distinct = total_cells - base - correction, which by
        construction equals total_cells - actual_dup, i.e. the exact
        true distinct count

    Prints the table and returns it as a list of dicts.
    """
    import io
    import sys

    rows = []
    for max_depth, m in cases:
        buf = io.StringIO()
        old_stdout = sys.stdout
        if not verbose:
            sys.stdout = buf
        all_entries, distinct_values = build_matrix(max_depth, m)
        sys.stdout = old_stdout

        total_cells = len(all_entries)
        true_distinct = len(distinct_values)
        actual_dup = total_cells - true_distinct
        base = base_formula(m)
        correction = actual_dup - base
        reconstructed_distinct = total_cells - base - correction

        rows.append({
            "max_depth": max_depth, "m": m, "N": max_depth,
            "total_cells": total_cells, "base": base,
            "actual_dup": actual_dup, "correction": correction,
            "true_distinct": true_distinct,
            "reconstructed_distinct": reconstructed_distinct,
        })

    header = f"{'max_depth':>10} {'m':>3} {'total_cells':>11} {'base=(2m-1)(2m)/2':>18} {'actual_dup':>10} {'correction':>10} {'true_C_distinct':>15} {'reconstructed':>13} {'match':>5}"
    print(header)
    for r in rows:
        match = r["true_distinct"] == r["reconstructed_distinct"]
        print(f"{r['max_depth']:>10} {r['m']:>3} {r['total_cells']:>11} "
              f"{r['base']:>18} {r['actual_dup']:>10} {r['correction']:>10} "
              f"{r['true_distinct']:>15} {r['reconstructed_distinct']:>13} "
              f"{'OK' if match else 'FAIL':>5}")
    return rows


if __name__ == "__main__":
    max_depth, m = 39, 7
    all_entries, distinct_values = build_matrix(max_depth, m)

    print(f"max_depth={max_depth}, m={m}")
    print(f"total cells: {len(all_entries)}")
    print(f"distinct values (C_distinct): {len(distinct_values)}")
    print(f"duplicates removed: {len(all_entries) - len(distinct_values)}")

    print()
    print("verifying exact_count() against the real matrix:")
    verify_exact_count(max_depth, m, all_entries, distinct_values)

    print()
    print("correction table (base formula + correction = exact answer, by construction):")
    correction_table([(31, 5), (37, 6), (43, 7), (23, 4), (15, 3), (13, 2), (61, 10), (91, 15)])

    print()
    print("c_distinct_direct() vs ground truth -- exact, general (not fit to specific cases):")
    print("  total_cells - coprime_only_duplicates_direct(max_depth, m) - mod3_correction(max_depth, m)")
    for md, mm in [(31, 5), (37, 6), (43, 7), (13, 2), (61, 10), (91, 15), (23, 4), (15, 3)]:
        _, dv = build_matrix(md, mm)
        true_val = len(dv)
        computed = c_distinct_direct(md, mm)
        print(f"  max_depth={md:>3} m={mm:>2}: true={true_val:>4}  computed={computed:>4}  "
              f"{'OK' if true_val == computed else 'FAIL'}")
