import math


def f(x):
    """f(x) = (sqrt(x)*(sqrt(x)+1) - sqrt(x))^(1/2)   [same formula as your GeoGebra f]"""
    root = math.sqrt(x)
    return math.sqrt(root * (root + 1) - root)


def g(x, E=425):
    """g(x) = f(-x + 2*E^2)   [same as your GeoGebra g(x) = f(-x + 2*425^2)]"""
    return f(-x + 2 * E * E)


def g_exact(x, E=425):
    """Algebraically g(x) simplifies to sqrt(2*E^2 - x) -- direct, no nested sqrt."""
    return math.sqrt(2 * E * E - x)


if __name__ == "__main__":
    E = 425

    # sanity check: g(x) should match the simplified sqrt(2E^2 - x) for every input
    for x in (23**2, 205**2, 289**2, 373**2, 222121, 360721):
        a = g(x, E)
        b = g_exact(x, E)
        print(f"x={x:>8}  g(x)={a:.6f}  sqrt(2E^2-x)={b:.6f}  match={math.isclose(a, b)}")

    # each cell's squared value in -> its opposite-pair partner's root out
    print()
    print("g(205^2) =", g(205**2, E), " -> I")
    print("g(23^2)  =", g(23**2, E), " -> sqrt(B)")
    print("g(289^2) =", g(289**2, E), " -> D")
    print("g(373^2) =", g(373**2, E), " -> sqrt(X)")
