def is_prime(n):
    """
    Single-number primality test using the same 6k+-1 lattice logic as the
    bit/bool-flag range detectors (PrimeVector_bitvector_parallel_*.py):
    every prime > 3 lies in branch B1 (6k+1) or B5 (6k-1), and composites
    in those branches are produced by exactly three feedback mechanisms --
    square, same-branch, and cross-branch.

    For a single n, same-branch and cross-branch feedback collapse to one
    thing: n = (6a+-1)(6b+-1) for some a,b >= 1 means n has a divisor of
    the form 6j+-1 no larger than sqrt(n) -- i.e. trial division restricted
    to the 6k+-1 wheel. The square-feedback check is kept as a fast O(1)
    path (it would otherwise be caught by the trial-division loop anyway,
    just later).
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 6 not in (1, 5):
        return False

    # Square feedback fast path: squares of branch elements only land in B1.
    if n % 6 == 1:
        root = int(n ** 0.5)
        while root * root > n:
            root -= 1
        while (root + 1) ** 2 <= n:
            root += 1
        if root * root == n and root % 6 in (1, 5):
            return False

    # Same-branch / cross-branch feedback: trial division by 6k+-1 up to sqrt(n).
    limit = int(n ** 0.5)
    for p in range(5, limit + 1, 6):
        if n % p == 0 or n % (p + 2) == 0:
            return False

    return True


if __name__ == "__main__":
    print([n for n in range(2, 100) if is_prime(n)])


tests = [999983, 999979, 999999937, 1000000007, 1299709, 999996000000037**0, 25**2, 49**2, 
         6*179+1, 6*179-1, 997*991, 100000007, 2**31-1, (10**6+3)*(10**6+33)]
import sympy
for n in tests:
    mine = is_prime(n)
    truth = sympy.isprime(n)
    print(n, 'mine=', mine, 'sympy=', truth, 'MATCH' if mine==truth else 'MISMATCH')