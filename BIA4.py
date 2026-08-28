import math

def is_square(n):
    return n >= 0 and int(math.isqrt(n))**2 == n

def generate_geometry(X_a, K):
    K2 = K*K

    # Free square choices for A and B
    # You can change these if you want different configurations
    A2 = X_a**2
    B2 = 2*K2-A2

    if not is_square(B2):
        return

    # Horizontal segment AI
    A = (A2, K2)
    I = (A2+ 2*K2, K2)   # I^2 = K^2

    # Vertical segment BH
    B = (A2+ 2*K2, K2)
    H = (A2+ 4*K2, K2)

    # Vertical segment CG (constrained)
    C2 = 3*K2 - A2 - B2
    C = (C2, K2)
    G = (C2+ 2*K2, K2)

    # Vertical segment FD (constrained)
    F2 = 3*K2 - C2 - I[0]
    F = (F2, K2)
    D = (F2 + 2*K2, K2)

    B2= 3*K2 - A[0]-C2
    # Check square-number rule
    heights = [A2, B2, C2, F2, I[0], H[0], G[0], D[0]]
    squares_ok = all(is_square(h) for h in heights)
    print([(abs(x))**(0.5)  for x in [A2,B2,C2,F2,I[0] , H[0],G[0],D[0]]])
    print(A2**2+B2**2+C2**2 == 3*K**2 , C2**2+F2**2+I[0]**2 == 3*K**2)
    return {
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
result = generate_geometry(X_a=205, K=425)
print(result)
