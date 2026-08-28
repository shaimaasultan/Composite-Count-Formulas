from math import gcd

def triples(limit):
    """All (A, C, B) with A^2 + C^2 = B^2, B <= limit."""
    out = []
    m = 2
    while m * m <= limit:
        for k in range(1, m):
            if (m - k) % 2 == 1 and gcd(m, k) == 1:   # primitive
                a, c, b = m*m - k*k, 2*m*k, m*m + k*k
                s = 1
                while s * b <= limit:                  # multiples
                    out.append((s*a, s*c, s*b))
                    s += 1
        m += 1
    return sorted(out, key=lambda t: t[2])

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

square_of_Squares = {}
for i in range(200):
    S = partners(i)
    if len(S) >= 9:
        square_of_Squares[i] = S
    print(i , S)

print("Square Of Squares :" , square_of_Squares)
    