import numpy as np

def bitvector_parallel(kmax):
    k = np.arange(1, kmax+1)

    # Branch vectors
    B1 = 6*k + 1
    B5 = 6*k - 1

    # Residue classes modulo 12
    r1 = B1 % 12
    r5 = B5 % 12

    # --- Feedback sets -----------------------------------------
    sq1 = (6*k + 1)**2
    sq5 = (6*k - 1)**2
    squares = np.concatenate([sq1, sq5])

    A1 = 6*k + 1
    A5 = 6*k - 1

    SB11 = np.outer(A1, A1).ravel()
    SB55 = np.outer(A5, A5).ravel()
    same_branch = np.concatenate([SB11, SB55])

    cross = np.outer(A5, A1).ravel()

    composites = np.unique(
        np.concatenate([squares, same_branch, cross])
    )

    # --- 12 parallel bit streams -------------------------------
    bitstreams = {}
    for residue in range(12):
        bitstreams[residue] = np.isin(composites % 12, residue).astype(np.uint8)

    # --- Composite flags for B1 and B5 --------------------------
    bit_B1 = np.isin(B1, composites).astype(np.uint8)
    bit_B5 = np.isin(B5, composites).astype(np.uint8)

    return bitstreams, bit_B1, bit_B5
    
bitstreams, bit_B1, bit_B5 = bitvector_parallel(30)
print( bitstreams)
print(bit_B1)
print(bit_B5)