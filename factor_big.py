"""
Factor arbitrary integers: small factors by the 6k+/-1 wheel, large ones by
Pollard's rho (Brent) with Miller-Rabin primality.  This is what actually factors
big semiprimes -- a precomputed small-prime list (a sieve) cannot, because its
entries never reach the large prime factors.
"""

import random
from math import gcd, isqrt

_SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_probable_prime(n):
    """Deterministic Miller-Rabin for n < 3.3e24 (and a very strong test above)."""
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _SMALL_PRIMES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard_rho(n):
    """Brent's variant -- returns a nontrivial factor of composite odd n."""
    if n % 2 == 0:
        return 2
    while True:
        y, c, m = random.randrange(1, n), random.randrange(1, n), 128
        g = q = 1
        r = 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def factorize(n):
    """Full prime factorization as a sorted list (with multiplicity)."""
    n = int(n)
    if n < 2:
        return []
    factors = []
    # peel small primes by the wheel first (fast, and helps rho)
    for p in _SMALL_PRIMES:
        while n % p == 0:
            factors.append(p)
            n //= p
    if n == 1:
        return sorted(factors)
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            factors.append(m)
            continue
        d = _pollard_rho(m)
        stack.append(d)
        stack.append(m // d)
    return sorted(factors)


def show(n):
    f = factorize(n)
    prod = 1
    for x in f:
        prod *= x
    ok = "OK" if prod == n else "FAIL"
    print(f"{n}\n  = {' * '.join(map(str, f))}   [{ok}]\n")


if __name__ == "__main__":
    for N in [
        412637514191952379171729,          # = 2501256713 * 164972076655433
        4126375141919523791919279,
        4126375141919523791919271,
        7334938410324762341973827534419726354193798261,
    ]:
        show(N)
