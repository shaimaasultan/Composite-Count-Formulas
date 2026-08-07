import numpy as np

def prime_flags(kmax):
    # Branch vectors
    k = np.arange(1, kmax+1)
    B1 = 6*k + 1
    B5 = 6*k - 1

    # --- 1. Square feedback ------------------------------------
    sq1 = (6*k + 1)**2
    sq5 = (6*k - 1)**2
    squares = np.concatenate([sq1, sq5])

    # --- 2. Same-branch feedback -------------------------------
    A1 = 6*k + 1
    A5 = 6*k - 1

    SB11 = np.outer(A1, A1).ravel()
    SB55 = np.outer(A5, A5).ravel()
    same_branch = np.concatenate([SB11, SB55])

    # --- 3. Cross-branch feedback ------------------------------
    cross = np.outer(A5, A1).ravel()

    # --- Global composite set ----------------------------------
    composites = np.unique(
        np.concatenate([squares, same_branch, cross])
    )

    # --- Flags: 1 = composite, 0 = prime ------------------------
    flag_B1 = np.isin(B1, composites).astype(int)
    flag_B5 = np.isin(B5, composites).astype(int)

    # --- Prime-only vectors ------------------------------------
    primes_B1 = B1[flag_B1 == 0]
    primes_B5 = B5[flag_B5 == 0]

    return B1, B5, flag_B1, flag_B5, primes_B1, primes_B5

# Example
B1, B5, f1, f5, p1, p5 = prime_flags(30)
print("B1:", B1)
print("Flags B1:", f1)
print("Primes B1:", p1)
print("B5:", B5)
print("Flags B5:", f5)
print("Primes B5:", p5)
