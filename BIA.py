import math

def find_A_I_from_B_and_K(B, K):
    """
    Given:
      B = square number (e.g., 9 means B^2 = 81)
      K = square number (e.g., 4 means K^2 = 16)

    Compute:
      I such that I - B = 4*K^2
      A such that A^2 is midpoint between B^2 and I^2
    """
    from math import isqrt 
    # Step 1: compute I
    I = isqrt((4 * (K**2)+B^2)/2)

    # Step 2: compute A^2 midpoint
    A_squared = (B**2 + I**2) / 2

    # Step 3: compute A
    A = math.isqrt(int(A_squared))

    # Check if A is a perfect square
    if A*A != A_squared:
        return {
            "B": B,
            "K": K,
            "I": I,
            "A_squared": A_squared,
            "A": None,
            "perfect_square": False
        }

    return {
        "B": B,
        "K": K,
        "I": I,
        "A_squared": A_squared,
        "A": A,
        "perfect_square": True
    }


# Example usage:
result = find_A_I_from_B_and_K(B=182, K=202)
print(result)
