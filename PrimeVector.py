import numpy as np

def prime_vectors(kmax):
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

    # --- Prime-only vectors ------------------------------------
    primes_B1 = B1[~np.isin(B1, composites)]
    primes_B5 = B5[~np.isin(B5, composites)]

    return primes_B1, primes_B5

# Example: primes in first 30 lattice positions
pB1, pB5 = prime_vectors(10000)
print("Primes in B1:", pB1)
print("Primes in B5:", pB5)
