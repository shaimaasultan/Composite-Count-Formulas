import numpy as np

def branch_vectors(kmax):
    B1 = 6*np.arange(1, kmax+1) + 1   # 6k+1
    B5 = 6*np.arange(1, kmax+1) - 1   # 6k-1
    return B1, B5

def align_shift(B1, B5, shift):
    B5s = np.roll(B5, -shift)
    return list(zip(B1, B5s))

# Example usage
kmax = 20
B1, B5 = branch_vectors(kmax)

aligned_minus1 = align_shift(B1, B5, 1)   # same-branch corridor
aligned_minus2 = align_shift(B1, B5, 2)   # mod 5 alignment
aligned_minus5 = align_shift(B1, B5, 5)   # mod 7 alignment

print("Shift -1 (same-branch corridor):")
print(aligned_minus1[:10])

print("\nShift -2 (mod 5 alignment):")
print(aligned_minus2[:10])

print("\nShift -5 (mod 7 alignment):")
print(aligned_minus5[:10])
