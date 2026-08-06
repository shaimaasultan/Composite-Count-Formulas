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