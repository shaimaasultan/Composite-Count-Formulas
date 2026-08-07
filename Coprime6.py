def coprime6(n): return n % 6 in (1, 5)

def count_via_splits(V, factors_multiset):
    '''For each distinct value in the factor multiset, split it off
    (leaving the product of the rest), and count how many directions
    (row,col) vs (col,row) are valid -- both coprime-to-6 gives 2,
    one side not coprime-to-6 gives 1.'''
    distinct_splits = set()
    for i, f in enumerate(factors_multiset):
        rest = factors_multiset[:i] + factors_multiset[i+1:]
        rest_product = 1
        for r in rest: rest_product *= r
        distinct_splits.add((f, rest_product))

    total = 0
    for single, rest_product in distinct_splits:
        dirs = 0
        if coprime6(single): dirs += 1  # rest_product as row (any odd), single as col (needs coprime6)
        if coprime6(rest_product): dirs += 1  # single as row, rest_product as col
        total += dirs
    return total

# 385 = 5*7*11 (three distinct, all coprime-to-6)
print('385 = 5*7*11:', count_via_splits(385, [5,7,11]), '(observed: 6)')
# 175 = 5*5*7
print('175 = 5*5*7:', count_via_splits(175, [5,5,7]), '(observed: 4)')
# 105 = 3*5*7 (3 is NOT coprime-to-6)
print('105 = 3*5*7:', count_via_splits(105, [3,5,7]), '(observed: 3)')

#385 = 5*7*11: 6 (observed: 6)
#175 = 5*5*7: 4 (observed: 4)
#105 = 3*5*7: 3 (observed: 3)"