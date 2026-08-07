import numpy as np

def align_branches(kmax):
    # Branch vectors
    B1 = 6*np.arange(1, kmax+1) + 1   # 6k+1
    B5 = 6*np.arange(1, kmax+1) - 1   # 6k-1

    # Shift B5 left by one cell
    B5_shifted = np.roll(B5, -6)

    # Zip alignment
    aligned = list(zip(B5_shifted[:-1], B1[:-1]))

    return aligned

# Example: first 10 aligned pairs
pairs = align_branches(20)
for p in pairs:
    print(p)
