import numpy as np

def prime_index_router(x):
    # search only lattice numbers up to sqrt(x)
    limit = int(np.sqrt(x))
    k_values = np.arange(1, limit//6 + 3)

    # lattice candidates
    B1 = 6*k_values + 1
    B5 = 6*k_values - 1

    # keep only candidates <= sqrt(x)
    B1 = B1[B1 <= limit]
    B5 = B5[B5 <= limit]

    # find which lattice numbers divide x
    factors_B1 = B1[x % B1 == 0]
    factors_B5 = B5[x % B5 == 0]

    # convert factors back to k
    k_from_B1 = (factors_B1 - 1) // 6
    k_from_B5 = (factors_B5 + 1) // 6

    return {
        "x": x,
        "k_indices": np.concatenate([k_from_B1, k_from_B5]),
        "lattice_factors": np.concatenate([factors_B1, factors_B5]),
        "cofactors": [x // a for a in np.concatenate([factors_B1, factors_B5])]
    }

# Examples
print(prime_index_router(539))   # 49 * 11
print(prime_index_router(77))    # 7 * 11
print(prime_index_router(55))    # 5 * 11
print(prime_index_router(1989))
print(prime_index_router(1539))
