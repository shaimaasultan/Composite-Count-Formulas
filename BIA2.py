import math

def is_square(n):
    return n >= 0 and int(math.isqrt(n))**2 == n

def scan_XY_distinct_squares(K_max=1000, XY_max=1000, threshold=5):
    results = []

    for X in range(1, XY_max+1):
        for Y in range(1, XY_max+1):
            # if X ==2 and Y == 2:
            #     continue
            # Must satisfy 1/X + 1/Y = 1
            if abs(1/X + 1/Y - 1) > 1e-12:
                continue

            for K in range(1, K_max+1):
                K2 = K*K

                # Vertical distances relative to horizon
                A = K2
                I = K2
                C = 2*K2
                G = 0
                D = 2*K2 - K2//X
                H = 2*K2 - K2//X - K2//Y
                F = 3*K2 - (C + I)
                B = 2*K2 - A

                values = [A, B, C, F, I, H, G, D]

                # Count perfect squares
                square_count = sum(set([is_square(v) for v in values]))
                if square_count < threshold:
                    continue

                # Distinctness rule:
                # 0 may repeat, but all other squares must be distinct
                nonzero_squares = [v for v in values if v != 0 and is_square(v)]
                if len(nonzero_squares) < threshold:
                    continue

                # Passed both rules → record it
                results.append({
                    "X": X,
                    "Y": Y,
                    "K": K,
                    "square_count": square_count,
                    "A": A,
                    "B": B,
                    "C": C,
                    "F": F,
                    "I": I,
                    "H": H,
                    "G": G,
                    "D": D
                })

    return results


# Example usage:
records = scan_XY_distinct_squares(threshold=1)
print("Found", len(records), "valid records")
for r in records[:-10]:
    print(r)
