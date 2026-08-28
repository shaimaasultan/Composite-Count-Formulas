# from math import isqrt

# def sq(m):
#     if m <= 0: return None
#     r = isqrt(m)
#     return r if r*r == m else None

# def solve_center(grid):
#     """grid: 9 values, center as None. Returns C^2 candidates per line."""
#     a, b, c, d, _, f, g, h, i = grid
#     lines = {
#         "row 1":  ([a, b, c], False),
#         "row 2":  ([d, f],    True),
#         "row 3":  ([g, h, i], False),
#         "col 1":  ([a, d, g], False),
#         "col 2":  ([b, h],    True),
#         "col 3":  ([c, f, i], False),
#         "diag \\":([a, i],    True),
#         "diag /": ([c, g],    True),
#     }
#     fixed, withC = {}, {}
#     for name, (vals, has_center) in lines.items():
#         s = sum(vals)
#         (withC if has_center else fixed)[name] = s
#     return fixed, withC

# grid = [744**2, 1**2, 576**2,
#         2**2,   None,  3**2,
#         943**2, 4**2,  817**2]

# grid = [None, 1**2, None,
#         2**2,   None,  3**2,
#         None, 4**2,  None]

# fixed, withC = solve_center(grid)
# print("lines without C:", fixed)
# print("lines with C (sum + C^2):", withC)

# if len(set(fixed.values())) == 1:
#     S = next(iter(fixed.values()))
#     for name, partial in withC.items():
#         print(name, "needs C^2 =", S - partial)
# else:
#     print("no C can work — these lines disagree and don't contain C")


# from collections import defaultdict
# from math import isqrt

# def sq(m):
#     if m <= 0: return None
#     r = isqrt(m)
#     return r if r*r == m else None

# def partners(A):
#     """All (B, C) with B^2 - A^2 = C^2."""
#     out = []
#     n = A * A
#     d = 1
#     while d * d < n:
#         if n % d == 0:
#             e = n // d
#             if (d + e) % 2 == 0:          # both same parity
#                 B, C = (d + e) // 2, (e - d) // 2
#                 if C > 0:
#                     out.append((B, C))
#         d += 1
#     return out

# def hyp_table(limit):
#     """n -> all center pairs (x, y) with x^2 + y^2 = 2n^2."""
#     table = defaultdict(set)
#     for leg in range(3, limit):
#         for B, C in partners(leg):          # B^2 - leg^2 = C^2
#             if B <= limit:
#                 p, q = leg, C
#                 table[B].add((abs(p - q), p + q))
#     return table

# def search_all(limit, want=8):
#     table = hyp_table(limit)
#     print(table)
#     for n, P in table.items():
#         P = sorted(P)
#         if len(P) < 3:
#             continue
#         S, T, E = 3*n*n, 2*n*n, n*n
#         for a, i in P:
#             for c, g in P:
#                 if (a, i) == (c, g): continue
#                 A, I, C, G = a*a, i*i, c*c, g*g
#                 B, H = S - A - C, S - G - I
#                 Dc, F = S - A - G, S - C - I
#                 cells = [A, B, C, Dc, E, F, G, H, I]
#                 if min(cells) <= 0 or len(set(cells)) != 9: continue
#                 k = sum(1 for x in cells if sq(x) is not None)
#                 if k >= want:
#                     print(n, k, cells)

# search_all(1000,want=7)


from collections import defaultdict
from math import isqrt

def sq(m):
    if m <= 0: return None
    r = isqrt(m)
    return r if r*r == m else None

def hypotenuse_index(limit):
    """B -> set of center pairs (x, y) with x^2 + y^2 = 2B^2."""
    idx = defaultdict(set)
    for leg in range(3, limit):
        for B, C in partners(leg):
            if B <= limit:
                idx[B].add((abs(leg - C), leg + C))
    return idx

def candidates(limit, min_pairs=3):
    idx = hypotenuse_index(limit)
    return {n: sorted(P) for n, P in idx.items() if len(P) >= min_pairs}

def partners(A):
    """All (B, C) with B^2 - A^2 = C^2."""
    out = []
    n = A * A
    d = 1
    while d * d < n:
        if n % d == 0:
            e = n // d
            if (d + e) % 2 == 0:          # both same parity
                B, C = (d + e) // 2, (e - d) // 2
                if C > 0:
                    out.append((B, C))
        d += 1
    return out

def run(limit, want=7):
    for n, P in sorted(candidates(limit).items()):
        S, T, E = 3*n*n, 2*n*n, n*n
        orient = [p for q in P for p in (q, q[::-1])]
        for a, i in orient:                    # main diagonal
            for b, h in orient:                # middle column
                A, I, B, H = a*a, i*i, b*b, h*h
                C  = S - A - B                 # top row
                G  = T - C                     # anti-diagonal
                Dc = S - A - G                 # left column
                F  = T - Dc                    # middle row
                cells = [A, B, C, Dc, E, F, G, H, I]
                if min(cells) <= 0 or len(set(cells)) != 9:
                    continue
                k = sum(1 for x in cells if sq(x) is not None)
                if k >= want:
                    print(n, k, cells)


run(100000 , 7)