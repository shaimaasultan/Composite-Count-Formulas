"""
6k +/- 1 wheel factorization -- the honest endpoint of the "peel 2, 3" idea.

The candidate modulus  M = (N mod 6) + 6m  runs through the 6k+/-1 numbers
(5, 11, 17, 23, ...  or  1, 7, 13, 19, ...): the only possible prime factors of N
once the factors 2 and 3 are peeled off.  We SCAN m and test divisibility.

This is genuine trial division, ~3x faster than testing every integer, and it is
O(sqrt(N)) -- a constant-factor win, not an asymptotic one.  No fixed-modulus
"mod trick" beats it; that is the sqrt(N) wall.
"""

from math import isqrt


def smallest_factor(N):
    """Smallest nontrivial factor of N (or N itself if N is prime).
    Peels 2 and 3, then scans the 6k +/- 1 wheel up to sqrt(N)."""
    if N < 2:
        return N
    for p in (2, 3):                      # peel 2 and 3
        if N % p == 0:
            return p
    # now N is coprime to 6; candidates are 6k-1 and 6k+1
    i = 5                                 # first 6k-1
    step = 2                              # alternate +2, +4  ->  5,7,11,13,17,19,...
    while i * i <= N:
        if N % i == 0:
            return i
        i += step
        step = 6 - step                   # 2 -> 4 -> 2 -> ...
    return N                              # prime


def factorize(N):
    """Full prime factorization of N as a sorted list of primes (with multiplicity)."""
    N = int(N)
    factors = []
    while N > 1:
        p = smallest_factor(N)
        factors.append(p)
        N //= p
    return factors


def wheel_candidates(N):
    """The 6k+/-1 candidate divisors up to sqrt(N) -- BOTH residue classes
    {5,7,11,13,17,19,...} (6k-1 and 6k+1), with the trivial 1 excluded.
    These are the moduli of M=(N mod 6)+6m taken over both classes.

    NOTE: the one-class version  [(N%6)+6*m ...]  is buggy -- it scans only the
    class N mod 6, so it misses factors in the other class (e.g. 55=5*11 with
    N%6==1 but both primes 5 mod 6), and it includes the trivial modulus 1.
     A = [(N % 6) + 6*m for m in range(isqrt(N)//6 + 1) ]
    return [N % A for A in A]
    """
    lim = isqrt(N)
    out = []
    i, step = 5, 2                        # 5,7,11,13,17,19,... via +2,+4
    while i <= lim:
        out.append(i)
        i += step
        step = 6 - step
    return out


def wheel_scan(N):
    """Scan the wheel as  M = 6m - 1  and  M = 6m + 1  for m = 1, 2, 3, ...  (both
    6k+/-1 classes), and EXIT at the first M with  N mod M == 0  (return that factor).
    Peels 2 and 3 first; returns N itself if no factor <= sqrt(N) (N is prime).

    This is the 'run with +6m, stop at Mod(N,M)==0' form -- correct because it
    covers both residue classes, so it never misses a factor."""
    for p in (2, 3):                      # peel 2 and 3
        if N % p == 0:
            return p
    lim = isqrt(N)
    m = 1
    while 6 * m - 1 <= lim:
        for M in (6 * m - 1, 6 * m + 1):  # both classes: 5,7 / 11,13 / 17,19 / ...
            if M <= lim and N % M == 0:
                return M                  # early exit at the first m giving mod 0
        m += 1
    return N                              # prime

from math import gcd

WHEEL60 = [r for r in range(60) if gcd(r, 60) == 1]   # 16 spokes
WHEEL210 = [r for r in range(210) if gcd(r, 210) == 1]   # 48 spokes
WHEEL2310 = [r for r in range(2310) if gcd(r, 2310) == 1]

def wheel_scan_60(N):
    """Smallest factor of N via a mod-60 wheel, or None if N is prime."""
    if N < 2:
        return None
    for p in (2, 3, 5):            # base primes the wheel skips — test them first
        if N == p:  return None
        if N % p == 0: return p
    limit = isqrt(N)
    m = 0
    while 60*m + 1 <= limit:
        for r in WHEEL60:
            n = 60*m + r          # the ACTUAL candidate, not r
            if n == 1:            # skip the trivial divisor
                continue
            if n > limit:
                break
            if N % n == 0:
                return n          # real factor found → N is composite
        m += 1
    return None                   # nothing divides up to √N → N is prime

def wheel_scan_210(N):
    """Smallest factor of N via a mod-210 wheel, or None if N is prime."""
    if N < 2:
        return None
    for p in (2, 3, 5, 7):        # base primes the wheel skips — test first
        if N == p:  return None
        if N % p == 0: return p
    limit = isqrt(N)
    m = 0
    while 210*m + 1 <= limit:
        for r in WHEEL210:
            n = 210*m + r          # actual candidate = block offset + spoke
            if n == 1:             # skip trivial divisor
                continue
            if n > limit:
                break
            if N % n == 0:
                return n           # real factor → composite
        m += 1
    return None                    # nothing up to √N → prime

def wheel_scan_2310(N):
    """Smallest factor of N via a mod-60 wheel, or None if N is prime."""
    if N < 2:
        return None
    for p in (2, 3, 5 , 7 ,11):            # base primes the wheel skips — test them first
        if N == p:  return None
        if N % p == 0: return p
    limit = isqrt(N)
    m = 0
    while 2310*m + 1 <= limit:
        for r in WHEEL60:
            n = 2310*m + r          # the ACTUAL candidate, not r
            if n == 1:            # skip the trivial divisor
                continue
            if n > limit:
                break
            if N % n == 0:
                return n          # real factor found → N is composite
        m += 1
    return None                   # nothing divides up to √N → N is prime

def wheel_factors(N):
    """The candidates that actually divide N (both classes, no trivial 1).
    A correct list-based counterpart to smallest_factor; the latter is preferred
    for real work because it stops at the first factor (early exit)."""
    return [d for d in wheel_candidates(N) if N % d == 0]


if __name__ == "__main__":
    # tractable sizes: the wheel is O(sqrt N), so it handles factors up to ~1e12 fast.
    tests = [9563 , 3187,77, 143, 221, 55, 85, 187, 91 , 3599, 2501, 1_000_003, 600851475143, 180625]#, 132493841032476234197382753441972635419379826774981234765919364528454827197351]

    for N in tests:
        # f = factorize(N)
        # prod = 1
        # for x in f:
        #     prod *= x
        # print(f"{N} = {' * '.join(map(str, f))}   (check {'OK' if prod == N else 'FAIL'})")
        W = wheel_scan(N)
        #W = wheel_scan_60(N)
        print(f"Wheel scan result: N = {N} = {W } *  {N // W}  (check {'OK' if W*(N//W) == N else 'FAIL'})")
        #print(wheel_scan_60(N))
        print(wheel_scan_60(N))

    # The sqrt(N) wall: a big semiprime with two ~12-digit prime factors is out of
    # reach for trial division (its smallest factor is ~sqrt(N) away).  That is
    # where sub-exponential methods (Pollard rho / p-1, ECM, quadratic sieve) are
    # needed -- the wheel cannot beat sqrt(N).
    print("\n# 412637514191952379171729 = 2501256713 * 164972076655433")
    print("#   smallest factor ~2.5e9, so the wheel would scan ~8e8 candidates -- too slow;")
    print("#   use Pollard p-1 / rho for semiprimes this size (see AST.html's factorFull).")
