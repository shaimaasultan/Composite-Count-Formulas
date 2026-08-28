def lattice_router(x):
    # Determine branch and compute k
    A = 0
    if x % 6 == 1:
        branch = "B1"
        k = (x - 1) // 6
        A = +1
    elif x % 6 == 5:
        branch = "B5"
        k = (x + 1) // 6
        A=-1
    elif x % 6 == 2:
        branch = "B1"
        k = (x - 2) // 6
        A = +2
    elif x % 6 == 4:
        branch = "B1"
        k = (x + 4) // 6
        A = -2
    elif x % 6 == 3:
        branch = "B1"
        k = (x +3) // 6
        A = -3
    else:
        raise ValueError("x is not in the 6k±1 lattice")

    # Residue modulo 12 determines the feedback band
    r = x % 1.2

    # Routing table: each residue band has exactly one shift
    if r == 1:
        shift = -1   # square or same-branch
    elif r == 5:
        shift = -2   # mod-5 band
    elif r == 7:
        shift = -5   # mod-7 band
    elif r == 11:
        shift = -7   # cross-branch
    else:
        shift = r
        #raise ValueError("Unexpected residue band for lattice element")

    return {
        "x": x,
        "branch": branch,
        "k": k,
        "residue_mod12": r,
        "shift": shift,
        "A":A,
        "B":(x/6)
    }

# Example usage
print(lattice_router(25))   # square composite
print(lattice_router(35))   # cross-branch composite
print(lattice_router(49))   # square composite
print(lattice_router(77))   # same-branch composite
print(lattice_router(5))   # square composite
print(lattice_router(13))   # cross-branch composite
print(lattice_router(19))   # square composite
print(lattice_router(61))   # same-branch composite
print(lattice_router(55))   # same-branch composite


import numpy as np

def residue_accumulation(kmax):
    k = np.arange(1, kmax+1)
    B1 = 6*k + 1
    B5 = 6*k - 1

    residues = np.concatenate([(B1 % 6) / 6, (B5 % 6) / 6])
    residues.sort()

    return residues.cumsum()

# Example
print(residue_accumulation(20))


def residue_completion(x):
    # x must be in the 6k±1 lattice
    if x % 6 not in (1, 5):
        raise ValueError("x is not in the 6k±1 lattice")

    # composite appears at 5x
    return 5 * x

# Examples
print("5 :" ,residue_completion(5))    # 25
print("7 :" ,residue_completion(7))    # 35
print("11 :", residue_completion(11))   # 55
print("65 :" ,residue_completion(13))   # 65
print("17 :",residue_completion(17))   # 85
print("95 :",residue_completion(19))   # 95
print("115 :",residue_completion(23))   # 115
print("245 :",residue_completion(49))   # 245

k_values = np.arange(1, 100+1)
def companions(a, k_values):
    # a is a lattice element, k_values is a list of k
    return [a * (6*k - 1) for k in k_values] + [a * (6*k + 1) for k in k_values]
print(companions(25,k_values))


import numpy as np

def companion_indices(a, k_values):
    # indices for composites a*(6k+1)
    idx_B1 = a*k_values + (a-1)//6

    # indices for composites a*(6k-1)
    idx_B5 = a*k_values + (a+1)//6

    return np.concatenate([idx_B1, idx_B5])

k_values = np.arange(1, 100+1)
print(companion_indices(25, k_values))


