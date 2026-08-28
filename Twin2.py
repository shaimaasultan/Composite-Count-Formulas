import math

# --- Phase 1: Build residue‑locked lattice pairs -----------------------------

L = {}
for x in range(10001, 100000, 6):      # Only 6k+1 lattice numbers
    r = (x - 0.75) % 6
    B = 2 * r
    D = 2 * ((x + 2 - 0.75) % 6)

    if B == 8.5 and D == 0.5:
        L[x] = x + 2
        print((x, x+2), (B, D), (x % 5, (x+2) % 5))

keys   = list(L.keys())
values = list(L.values())

# --- Phase 2: Build modular companion sets ----------------------------------

L2_Y = []
L2_X = []

for k in keys:
    for v in values:
        if k == v:
            continue

        # v divisible by k → remainder k % v
        if v % k == 0:
            r = k % v
            if r not in values:
                L2_Y.append(r)

        # k divisible by v → remainder v % k
        if k % v == 0:
            r = v % k
            if r not in keys:
                L2_X.append(r)

S = L2_X + L2_Y

print(set(L2_X))
print(set(L2_Y))
print(math.sqrt(1000), len(S))

# --- Phase 3: Factor signature scan near 100k -------------------------------

for x in range(99000, 100000):
    if x % 2 == 0 or x % 3 == 0:
        continue

    factors = []
    for k in S:
        if k != 1 and k != x and x % k == 0:
            factors.append(k)
            factors.append(x // k)

    print((x, factors))
