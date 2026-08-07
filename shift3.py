import numpy as np

def composite_detector(kmax):
    # Branch vectors
    k = np.arange(1, kmax+1)
    B1 = 6*k + 1
    B5 = 6*k - 1

    # --- 1. Square feedback ------------------------------------
    sq1 = (6*k + 1)**2
    sq5 = (6*k - 1)**2
    squares = np.concatenate([sq1, sq5])

    # --- 2. Same-branch feedback -------------------------------
    # B1 × B1
    A1 = 6*k + 1
    SB11 = np.outer(A1, A1).flatten()

    # B5 × B5
    A5 = 6*k - 1
    SB55 = np.outer(A5, A5).flatten()

    same_branch = np.concatenate([SB11, SB55])

    # --- 3. Cross-branch feedback ------------------------------
    cross = np.outer(A5, A1).flatten()

    # --- Combine all feedback composites ------------------------
    composites = np.unique(
        np.concatenate([squares, same_branch, cross])
    )

    # --- Detect composites in B1 and B5 -------------------------
    #C1 = B1[np.isin(B1, composites)]
    #C5 = B5[np.isin(B5, composites)]

    return  composites

# Example
composites = composite_detector(14)
print(composites)
#print("Composites in B1:", C1)
#print("Composites in B5:", C5)
