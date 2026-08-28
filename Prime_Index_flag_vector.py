import numpy as np

def companions(a, k_values):
    return np.concatenate([
        a * (6*k_values - 1),
        a * (6*k_values + 1)
    ])

def prime_index_flags(a, k_values):
    # generate companion composites
    comps = companions(a, k_values)

    # compute k-index for each composite
    k_from_B1 = (comps[comps % 6 == 1] - 1) // 6
    k_from_B5 = (comps[comps % 6 == 5] + 1) // 6

    k_indices = np.concatenate([k_from_B1, k_from_B5])

    # build flag vector
    flags = np.zeros_like(k_values, dtype=int)

    for k in k_indices:
        if k in k_values:
            flags[k_values == k] = 1

    return flags, k_indices

# Example
k_values = np.arange(1, 100+1)
flags, k_idx = prime_index_flags(5, k_values)

print("k-indices:", k_idx)

flags2, k_idx = prime_index_flags(7, k_values)
print("flags:", flags+flags2)
