from collections import defaultdict
from math import isqrt , pi
import math

ALLOWED = {1, 5,9}

def sq(m):
    if m <= 0: return None
    r = isqrt(m)
    return r if (r)*(r) == (m) else None

def digit_ok(cells):
    return all(c % 10 in ALLOWED for c in cells)

def partners(A):
    out, n = [], A*A
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            e = n // d
            if d < e and (d + e) % 2 == 0:
                out.append(((d + e)//2, (e - d)//2))
    return out

from math import gcd

def candidates(limit, min_pairs=3):
    idx = defaultdict(set)
    m = 2
    while m*m <= limit:
        for k in range(1, m):
            if (m - k) % 2 and gcd(m, k) == 1:
                p, q, h = m*m - k*k, 2*m*k, m*m + k*k
                s = 1
                while s*h <= limit:
                    idx[s*h].add((s*abs(p - q), s*(p + q)))
                    s += 1
        m += 1
    return {n: sorted(P) for n, P in idx.items() if len(P) >= min_pairs}

def run(limit, want=9, use_digits=True):
    for n, P in sorted(candidates(limit).items()):
        if use_digits and (n*n) % 10 not in ALLOWED:
            continue
        S, T, E = 3*n*n, 2*n*n, n
        orient = [p for q in P for p in (q, q[::-1])]
        #print(orient)
        for a, i in orient:
            A, I = a, 2*n-a
            if use_digits and (A % 10 not in ALLOWED or I % 10 not in ALLOWED):
                continue
            for b, h in orient:
                B, H = b, n- b
                C  = 3*n - A - B
                G  = A + B - n
                D = 4*n-2* A - B
                F  = 2*A + B - 2 *n
                cells = [A, B, C, D, E, F, G, H, I]
                if min(cells) <= 0 or len(set(cells)) <8:
                    continue
                if use_digits and not digit_ok(cells):
                    continue
                k = sum(1 for x in cells if sq(x) is not None)
                if k >= want:
                    print(n, k, cells)

#run(10000, 4,False)
max_len = 31
max_Part = []
#for i in range(8080 , 10000):
for i in range(1 , 100):
    if len(partners(i)) >= 40 and i % 2 ==0 :
        max_len = len(partners(i))
        max_Part = [i , partners(i)]
        print(i , partners(i))



print(max_Part, len(max_Part)) 
print(partners(8080))
print(partners(586092))
# print(len(partners(8080)))