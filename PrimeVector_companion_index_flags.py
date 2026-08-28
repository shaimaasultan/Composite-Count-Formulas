import numpy as np


def companion_index_flags(kmax):
    """
    Composite index flags for the 6k+-1 backbone, built directly from the
    Companion Mapping Theorem (Primes_Structure.tex): for a branch element
    a = 6m+-1 and a branch element b_k = 6k+-1, the companion c = a*b_k is
    again of the form 6n+-1, and is composite (with a as a non-trivial
    factor) whenever |a| > 1.

    This single sweep over all four sign combinations of (a, b_k) replaces
    the earlier square/same-branch/cross-branch split: squares are just the
    diagonal case a = b_k, automatically included rather than handled as a
    separate formula.

    Returns (B1, B5, composite_B1, composite_B5) where composite_B1[j] is
    True iff B1[j] = 6(j+1)+1 is composite (composite_B5 likewise for B5).
    """
    composite_B1 = np.zeros(kmax + 1, dtype=bool)
    composite_B5 = np.zeros(kmax + 1, dtype=bool)

    idx = np.arange(1, kmax + 1, dtype=np.int64)

    for a_sign in (1, -1):
        a = 6 * idx + a_sign          # all branch values a = 6m +- 1
        for b_sign in (1, -1):
            b = 6 * idx + b_sign      # all branch values b_k = 6k +- 1
            c = (a[:, None] * b[None, :]).ravel()  # companion set C(a), all a at once

            # c = 6j+1 -> B1 index j
            b1_mask = (c % 6 == 1)
            j1 = (c[b1_mask] - 1) // 6
            valid1 = (j1 >= 1) & (j1 <= kmax)
            composite_B1[j1[valid1]] = True

            # c = 6j-1 -> B5 index j
            b5_mask = (c % 6 == 5)
            j5 = (c[b5_mask] + 1) // 6
            valid5 = (j5 >= 1) & (j5 <= kmax)
            composite_B5[j5[valid5]] = True

    k = np.arange(1, kmax + 1, dtype=np.int64)
    B1 = 6 * k + 1
    B5 = 6 * k - 1

    return B1, B5, composite_B1[1:], composite_B5[1:]


if __name__ == "__main__":
    B1, B5, comp_B1, comp_B5 = companion_index_flags(100)
    print("Primes B1:", B1[~comp_B1])
    print("Primes B5:", B5[~comp_B5])
