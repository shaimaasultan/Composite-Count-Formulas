import numpy as np

def prime_factor_router(x):
    # x must be in the 6k±1 lattice
    #if x % 6 not in (1, 5):
    #    raise ValueError("x is not in the 6k±1 lattice")

    # search only lattice numbers up to sqrt(x)
    limit = int(np.sqrt(x))
    k_values = np.arange(1, limit//6 + 2)

    lattice_candidates = np.concatenate([
        6*k_values + 1,
        6*k_values - 1
    ])

    # keep only candidates <= sqrt(x)
    lattice_candidates = lattice_candidates[lattice_candidates <= limit]

    # reverse mapping: find lattice factors
    factors = [a for a in lattice_candidates if x % a == 0]

    return {
        "x": x,
        "lattice_factors": factors,
        "cofactors": [x // a for a in factors]
    }

# Example
print(prime_factor_router(539))   # 49 * 11
print(prime_factor_router(77))    # 7 * 11
print(prime_factor_router(55))    # 5 * 11
print(prime_factor_router(1989))    # 5 * 11
print(prime_factor_router(2731539))    # 5 * 11
