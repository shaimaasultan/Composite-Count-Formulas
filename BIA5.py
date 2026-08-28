import math

def is_square(n):
    return n >= 0 and int(math.isqrt(n))**2 == n

def generate_geometry(X_a, X_b , z , wants):
    # Compute K from the rule (X_a^2 + X_b^2)/2 = K^2
    K2 = X_a*X_a // (2*z) + X_b*X_b // (2*z)
    K = int(math.isqrt(K2))

    if K*K != K2:
        return # {"error": "K^2 is not a perfect square. Choose different X_a, X_b."}

    # Heights A^2 and B^2 are simply X_a^2 and X_b^2
    A2 = X_a*X_a
    B2 = X_b*X_b

    # Horizontal segment AI
    A = (X_a, A2)
    I2 = K2  # I^2 = K^2
    I = (X_a + 2*K2, I2)

    # Vertical segment BH
    B = (X_b, B2)
    H = (X_b, B2 - 2*K2)

    # Vertical segment CG
    C2 = 3*K2 - A2 - B2
    C = (X_b + 2*K2, C2)
    G = (X_b + 2*K2, C2 - 2*K2)

    # Vertical segment FD
    F2 = 3*K2 - C2 - I2
    F = (X_b + 4*K2, F2)
    D = (X_b + 4*K2, F2 - 2*K2)

    # Check square-number rule
    heights = [A2, B2, C2, F2, I2, H[1], G[1], D[1]]
    roots = [math.isqrt(h)  for h in set(heights) if is_square(h) ]
    squares_ok = all(is_square(h)  for h in heights )

    if len(roots) >= wants:
        return {
            "K": K,
            "z": z,
            "X_a":X_a,
            "X_b":X_b,
            "Square count" :len(roots),
            "roots" : roots,
            "A": A,
            "I": I,
            "B": B,
            "H": H,
            "C": C,
            "G": G,
            "F": F,
            "D": D,
            "heights": heights,
            "all_squares": squares_ok
        }


# Example usage:
for i in range(576,10000):
    for j in range(1,200):
        for k in range(1 ,1000):
            result = generate_geometry(X_a=i, X_b=j,z=k,wants=6)
            if result != None:
                print(result)
