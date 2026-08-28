from math import isqrt

def triples_for_k(k):
    """All Pythagorean triples (k, s, k+d) having k as a leg, via s^2 = d(2k+d)."""
    out = []
    dmax = (k*k)//2 + 1                 # largest gap: u=1 (odd k) / u=2 (even k)
    for d in range(1, dmax + 1):
        g = d*(2*k + d)                 # the staircase gap
        s = isqrt(g)
        if s*s == g:                    # gap is a perfect square -> triple
            out.append((k, s, k + d))
    return out

if __name__ == "__main__":
    # sanity
    for k in (3,4,5,15,20):
        print(k, triples_for_k(k))

def count_for_k(k):
    """Fast count of triples with leg k: k^2=(h-s)(h+s)=u*v, u<v, u=v mod 2."""
    ksq, c = k*k, 0
    u = 1
    while u*u < ksq:
        if ksq % u == 0:
            v = ksq // u
            if (u + v) % 2 == 0:
                c += 1
        u += 1
    return c

def pairs_to_2ksq(k):
    """All (a,b), a<=b, with a^2 + b^2 = 2*k^2.
    These are the opposite-cell pairs of a magic square of squares whose
    center is k^2: each line through the center sums to a^2 + k^2 + b^2 = 3*k^2.
    Every nontrivial pair (a!=b) corresponds to a Pythagorean triple with
    hypotenuse k, via p=(a+b)/2, q=(b-a)/2  ->  p^2 + q^2 = k^2."""
    target, out, a = 2*k*k, [], 0
    while 2*a*a <= target:
        b2 = target - a*a
        b = isqrt(b2)
        if b*b == b2 and b >= a:
            out.append((a, b))
        a += 1
    return out

def is_square(N):
    if N < 0:
        return False
    r = isqrt(N)
    return r*r == N

def rect_lines_for_k(k):
    """Magic lines centred at k^2 via TWO gaps (d1,d2): roots (k-d1, k, k+d2) with
    (k-d1)^2 + (k+d2)^2 = 2k^2 -- integer rectangle a x b with diagonal k*sqrt(2)."""
    out = []
    for a in range(0, k):
        b2 = 2*k*k - a*a
        if is_square(b2):
            b = isqrt(b2)
            out.append((a, k, b, k - a, b - k))     # (small, center, big, d1, d2)
    return out

def count_magic_lines(k):
    """N(k) = 1/2 ( prod over p|k, p=1 mod 4 of (2*e_p+1) - 1 ). Needs >=4 for a square."""
    n, prod, d = k, 1, 2
    f = {}
    while d*d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    for p, e in f.items():
        if p % 4 == 1:
            prod *= (2*e + 1)
    return (prod - 1)//2

def lines_by_area(k):
    """Magic lines at centre k^2 via the AREA condition:
    A = a*b is a valid rectangle area  <=>  2(k^2 + A) and 2(k^2 - A) are both squares.
    Diagonal is fixed at k*sqrt(2); the two half-triangles each have area A/2."""
    out = []
    for A in range(1, k*k + 1):
        if is_square(2*(k*k + A)) and is_square(2*(k*k - A)):
            apb, bma = isqrt(2*(k*k + A)), isqrt(2*(k*k - A))
            a, b = (apb - bma)//2, (apb + bma)//2
            if 0 < a < b:
                out.append((A, a, b))
    return out

def winners(k):
    """Magic squares of squares at centre k^2. Take two pairs as the diagonals
    (corners A, C); the edges B = 3k^2 - A - C and D = k^2 - A + C are FORCED and
    must also be perfect squares. Returns (A, C, B, D) for each full solution.
    Only two independent off-centre conditions exist; the rest are automatic."""
    c = k*k
    corners = [(a*a, 2*c - a*a) for a in range(1, k)
               if is_square(2*c - a*a) and isqrt(2*c - a*a) > k]
    out = []
    for i in range(len(corners)):
        for j in range(len(corners)):
            if i == j:
                continue
            for A in corners[i]:
                for C in corners[j]:
                    B, D = 3*c - A - C, c - A + C
                    if B > 0 and D > 0 and is_square(B) and is_square(D):
                        out.append((A, C, B, D))
    return out
