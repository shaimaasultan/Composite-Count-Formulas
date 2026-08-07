import math


def coprime6(n):
    return n % 6 in (1, 5) 


def build_index_column(max_depth):
    """
    Branch1 (7,13,19,...) and branch5 (5,11,17,...) merged and sorted
    ascending, with 0 standing in for the excluded center value (1) --
    no multiples of 3 involved at all, no symmetric doubling.

    e.g. max_depth=19:
        [0, 5, 7, 11, 13, 17, 19]
    """
    return [0] + [v for v in range(5, max_depth + 1) if coprime6(v)]


def build_matrix(max_depth, m):
    """
    Builds the matrix on the simple merged-ascending branch index
    (0, 5, 7, 11, 13, 17, 19, ...) -- no symmetric doubling, no
    multiples of 3 anywhere.

    Row 0 (the excluded center) contributes no matrix cells. Every other
    row alternates base 5, 7, 5, 7, ... in simple sequence order (the
    first real row gets base 5, the second gets base 7, and so on), and
    that row's m columns are 5 consecutive branch values stepping by 6
    from that base. Each cell = row_value * column_value.

    Prints the index column, the per-row columns, the sorted list of all
    entries, the sorted distinct values, and every repeated value with
    its count.

    Returns (all_entries, distinct_values).
    """
    from collections import Counter

    index_column = build_index_column(max_depth)
    print(index_column)

    all_entries = []
    real_row_num = 0
    for a in index_column:
        if a == 0:
            continue  # the center: no matrix cells
        real_row_num += 1
        base = 5 if real_row_num % 2 == 1 else 7
        cols = [base + 6 * j for j in range(m)]
        print(cols)
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

    over_2 = {v: c for v, c in counts.items() if c > 2}
    print("repeated values with count > 2 (value: count):")
    for v in sorted(over_2):
        print(f"  {v}: {over_2[v]}")

    return all_entries, distinct_values


if __name__ == "__main__":
    max_depth, m = 55, 5
    all_entries, distinct_values = build_matrix(max_depth, m)

    print(f"max_depth={max_depth}, m={m}")
    print(f"total cells: {len(all_entries)}")
    print(f"distinct values (C_distinct): {len(distinct_values)}")
    print(f"duplicates removed: {len(all_entries) - len(distinct_values)}")
