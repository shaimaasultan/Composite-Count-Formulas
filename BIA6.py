import math

def is_square(n):
    return n >= 0 and int(math.isqrt(n))**2 == n

def generate_geometry(X_a, X_b, z, wants):
    # Compute K from the rule (X_a^2 + X_b^2)/(2*z) = K^2
    S = X_a*X_a + X_b*X_b
    denom = 2*z

    # K^2 must be integer
    if S % denom != 0:
        return None

    K2 = S // denom
    K = int(math.isqrt(K2))

    # K must be perfect square
    if K*K != K2:
        return None

    # Heights A^2 and B^2
    A2 = X_a*X_a
    B2 = X_b*X_b

    # Horizontal segment AI
    A = (X_a, A2)
    I2 = K2
    I = (X_a + 2*K2, I2)

    # Vertical segment BH
    B = (X_b, B2)
    H = (X_b, B2 - 2*K2)

    # Vertical segment CG
    C2 = K2 + A2 + B2
    C = (X_b + 2*K2, C2)
    G = (X_b + 2*K2, C2 - 2*K2)

    if C2 < 0 :
        return None
    # Vertical segment FD
    F2 = 3*K2 - C2 - I2
    F = (X_b + 4*K2, F2)
    D = (X_b + 4*K2, F2 - 2*K2)

    # All heights
    heights = [A2, B2, C2, F2, I2, H[1], G[1], D[1]]

    # Check square-number rule
    roots = [math.isqrt(h) for h in set(heights) if is_square(h)]

    if len(roots) >= wants:
        return {
            "K": K,
            "z": z,
            "X_a": X_a,
            "X_b": X_b,
            "Square count": len(roots),
            "roots": roots,
            "A": A,
            "I": I,
            "B": B,
            "H": H,
            "C": C,
            "G": G,
            "F": F,
            "D": D,
            "heights": heights,
            "all_squares": all(is_square(h) for h in heights)
        }

    return None


# Example search
for X_a in range(1, 1000):
    for X_b in range(1, 1000):
        for z in range(1, 100):
            result = generate_geometry(X_a, X_b, z, wants=5)
            if result is not None:
                print(result)
