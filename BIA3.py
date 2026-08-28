import math
from fractions import Fraction

def is_square(n):
    return n >= 0 and int(math.isqrt(n))**2 == n

def scan_rational_XY(K_max=500, p_max=500, q_max=500, threshold=5):
    results = []

    for p in range(2, p_max+1):
        for q in range(1, q_max+1):

            X = Fraction(p, q)

            # Skip X = 1 (division by zero)
            if X == 1:
                continue

            # Compute Y from the rational identity
            Y = 1 + Fraction(1, X - 1)

            # Now scan K
            for K in range(1, K_max+1):
                K2 = K*K

                # Vertical distances relative to horizon
                A = K2
                I = K2
                C = 2*K2
                G = 0

                # D and H use rational X,Y
                D = 2*K2 - K2 * Fraction(1, X)
                H = 2*K2 - K2 * Fraction(1, X) - K2 * Fraction(1, Y)

                # F and B from your rules
                F = 3*K2 - (C + I)
                B = 2*K2 - A

                # Convert all to integers if possible
                values = [A, B, C, F, I, H, G, D]

                # Only keep integer values
                if any(v.denominator != 1 for v in values):
                    continue

                values = [int(v) for v in values]

                # Count perfect squares
                square_count = sum(is_square(v) for v in values)
                if square_count < threshold:
                    continue

                # Distinctness rule: 0 may repeat, others must be unique
                nonzero_squares = [v for v in values if v != 0 and is_square(v)]
                if len(nonzero_squares) != len(set(nonzero_squares)):
                    continue

                # Valid record
                results.append({
                    "X": float(X),
                    "Y": float(Y),
                    "K": K,
                    "square_count": square_count,
                    "A": values[0],
                    "B": values[1],
                    "C": values[2],
                    "F": values[3],
                    "I": values[4],
                    "H": values[5],
                    "G": values[6],
                    "D": values[7]
                })

    return results


# Example usage:
records = scan_rational_XY(threshold=1)
print("Found", len(records), "valid rational records")
for r in records[:10]:
    print(r)
