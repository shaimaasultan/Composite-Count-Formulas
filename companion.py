
k_values = list(range(1, 100+1))

def companions(a, k_values):
    # a is a lattice element, k_values is a list of k
    companions = [a * (6*k - 1) for k in k_values] 
    idx_B1 = [(a*k + (a-1)//6)-1 for k in k_values]
    return companions , idx_B1
N = 5
companions , idx_B1 = companions(N,k_values)
print(" N :" , N)
print("companions : " ,companions )
print("idx_B1 : " ,idx_B1)

def companion_indices(a, k_values):
    idx_B1 = [(a*k + (a-1)//6) for k in k_values]
    idx_B5 = [(a*k + (a+1)//6) for k in k_values]
    return idx_B1 + idx_B5   # pure Python list


def companion_flags(a, k_values):
    idx = companion_indices(a, k_values)
    flags = [0]*len(k_values)

    for i, k in enumerate(k_values):
        if k in idx:
            flags[i] = 1

    return flags

flags_5 = companion_flags(5, k_values)
flags_7 = companion_flags(7, k_values)

combined = [f1 + f2 for f1, f2 in zip(flags_5, flags_7)]
print(k_values)
print(combined)

