import numpy as np

def bitvector_prime_detector(kmax):
    # Backbone indices
    k = np.arange(1, kmax+1)

    # Branch vectors
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

    # --- Bit vectors: 1 = composite, 0 = prime ------------------
    bit_B1 = np.isin(B1, composites).astype(np.uint8)
    bit_B5 = np.isin(B5, composites).astype(np.uint8)

    # --- Prime-only vectors ------------------------------------
    primes_B1 = B1[bit_B1 == 0]
    primes_B5 = B5[bit_B5 == 0]

    return B1, B5, bit_B1, bit_B5, primes_B1, primes_B5

# Example
B1, B5, bits1, bits5, p1, p5 = bitvector_prime_detector(30)
print("Bit vector B1:", bits1)
print("Bit vector B5:", bits5)
print("Primes B1:", p1)
print("Primes B5:", p5)
