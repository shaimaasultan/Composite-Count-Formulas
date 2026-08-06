import math


def build_matrix(max_depth, m):
    """
    Reconstructs the coprime-product matrix exactly as specified.

    The index column is built EXACTLY as shown in the sheet -- the full
    symmetric list, descending from max_depth to 1, then 0, then back up
    to max_depth:
        [max_depth, max_depth-2, ..., 3, 1, 0, 1, 3, ..., max_depth-2, max_depth]
    Row numbers (1-indexed) run top to bottom over this full list.

    The base column (which of 5/7 starts that row's m columns) alternates
    5, 7, 5, 7, ... down the WHOLE list, but the zero row doesn't consume
    a step of that alternation -- it shows 0 (since any product through it
    is 0) and the alternation picks back up on the next row exactly where
    it left off, not from the zero row's own position. That's why the
    ascending half's alternation is offset by one relative to the raw row
    number (verified against the exact target sequence:
    5,7,5,7,...,5,7,0,5,7,5,7,...,5,7).

    For every row except the true zero row, the m columns are 5
    consecutive branch values, stepping by 6, starting at that row's base.
    Each cell = row_value * column.

    Returns (all_entries, distinct_values).
    """
    if max_depth < 3 or max_depth % 2 == 0:
        raise ValueError("max_depth must be an odd integer >= 3")

    # full index column, exactly as shown: descending to 1, then 0, then
    # back up to max_depth
    index_column = list(range(max_depth, 0, -2)) + [0] + list(range(1, max_depth + 1, 2))
    print(index_column)
    # base column: alternates 5,7,5,7,... but the zero row doesn't consume
    # a step -- it shows 0 and the alternation resumes on the next row
    # exactly where it left off
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
        cols = [base + 4 * j for j in range(m)]
        print(cols)
        if a == 1:
            continue  # the two a=1 rows still show real cols, but
                       # contribute no matrix cells (same as the zero row)
        for c in cols:
            all_entries.append(a * c)
       
    distinct_values = set(sorted(all_entries))

    print(sorted(all_entries))
    print(sorted(distinct_values))

    from collections import Counter
    counts = Counter(all_entries)
    repeated = {v: c for v, c in counts.items() if c > 1}
    print("repeated values (value: count):")
    for v in sorted(repeated):
        print(f"  {v}: {repeated[v]}")

    return all_entries, distinct_values


def c_distinct(max_depth, m):
    _, distinct_values = build_matrix(max_depth, m)
    return len(distinct_values)


if __name__ == "__main__":
    max_depth, m = 35, 6
    all_entries, distinct_values = build_matrix(max_depth, m)
    print(f"max_depth={max_depth}, m={m}")
    print(f"total cells: {len(all_entries)}")
    print(f"distinct values (C_distinct): {len(distinct_values)}")
    print(f"duplicates removed: {len(all_entries) - len(distinct_values)}")
