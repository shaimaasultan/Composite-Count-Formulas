"""
Canonical {1, 2, 3, +, -, *} form of any natural number.

Engine:  wheel_factor.factorize  ->  prime factors.
Rule:    2 and 3 are atoms; every prime p > 3 is  p = 2*3*k +/- 1  (the 6k+/-1
         form), and k itself is written in the same canonical form, recursively.

So:  N  =  product of primes,  each prime  =  2*3*(canonical k) +/- 1.
This is the honest terminus of the whole thread: peel 2,3 (the wheel), then every
surviving prime is 6k+/-1, built from {1,2,3,+,-,*} alone.
"""

from wheel_factor import factorize, smallest_factor


def is_prime(n):
    return n > 1 and smallest_factor(n) == n


def canonical(n):
    """A string over {1,2,3,+,-,*} that evaluates to n."""
    n = int(n)
    if n <= 3:
        return str(n)                      # 0,1,2,3 atoms (n>=1 expected)
    if is_prime(n):
        if n % 6 == 1:                     # p = 2*3*k + 1,  k = (p-1)/6
            k = (n - 1) // 6
            return f"(2*3*{canonical(k)}+1)"
        else:                              # p % 6 == 5:  p = 2*3*k - 1, k = (p+1)/6
            k = (n + 1) // 6
            return f"(2*3*{canonical(k)}-1)"
    # composite: product over prime factors (with multiplicity)
    return "*".join(canonical(p) for p in factorize(n))


if __name__ == "__main__":
    for n in [5, 7, 11, 13, 17, 25, 77, 143, 180625, 425, 2501, 1000003, 123456789]:
        s = canonical(n)
        val = eval(s)                      # verify it evaluates back to n
        print(f"{n:>10} = {s}   [{'OK' if val == n else 'FAIL'}]")
