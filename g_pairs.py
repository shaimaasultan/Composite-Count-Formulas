import math


def g_pairs(E=425):
    """
    For u^2 + v^2 = 2*E^2, find every integer u <= x_max whose partner
    v = g(u^2) = sqrt(2*E^2 - u^2) is also an integer.
    Returns the essentially distinct pairs (u, v) with u <= v.
    """
    two_e2 = 2 * E * E

    pairs = []
    for u in range(1, E):
        remainder = two_e2 - u * u
        v = math.isqrt(remainder)
        if v * v == remainder and u <= v:
            pairs.append((u, v))
    return pairs


if __name__ == "__main__":
    E = 850

    print(f"search u up to (E={E}): ")
    results = g_pairs(E)
    print(f"\nu^2 + v^2 = 2*{E}^2 = {2*E*E}")
    if not results:
        print("no integer pairs found in this range")
    for u, v in results:
        print(f"({u}, {v})")
