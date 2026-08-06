import math
from collections import Counter


def coprime6(n):
    return n % 6 in (1, 5)


def build_index_column(max_depth):
    """
    Full symmetric list (descending max_depth..1, then 0, then back up to
    max_depth), with every nonzero multiple of 3 removed (3, 9, 15, 21,
    27, ...). The center (0) is kept -- only nonzero multiples of 3 are
    excluded.

    e.g. max_depth=31:
        [31, 29, 25, 23, 19, 17, 13, 11, 7, 5, 1, 0, 1, 5, 7, 11, 13, 17,
         19, 23, 25, 29, 31]
    """
    full = list(range(max_depth, 0, -2)) + [0] + list(range(1, max_depth + 1, 2))
    return [v for v in full if v == 0 or v % 3 != 0]


def build_matrix(max_depth, m):
    """
    Builds the matrix on the multiples-of-3-excluded index column:
      - base column: alternates 5,7,5,7,... but the zero row doesn't
        consume a step -- it shows 0 and the alternation resumes on the
        next row exactly where it left off.
      - the three middle rows (1, 0, 1) contribute no matrix cells.
      - every other row's m columns are 5 consecutive branch values,
        stepping by 6, starting at that row's base.
      - each cell = row_value * column_value.

    Prints the index column, the per-row columns (0 for the zero row),
    the sorted list of all entries, the sorted distinct values, and every
    repeated value with its count.

    Returns (all_entries, distinct_values).
    """
    index_column = build_index_column(max_depth)
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


if __name__ == "__main__":
    max_depth, m = 35, 10
    all_entries, distinct_values = build_matrix(max_depth, m)

    print(f"max_depth={max_depth}, m={m}")
    print(f"total cells: {len(all_entries)}")
    print(f"distinct values (C_distinct): {len(distinct_values)}")
    print(f"duplicates removed: {len(all_entries) - len(distinct_values)}")
