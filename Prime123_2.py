from math import isqrt

def is_sq(n):
    if n < 0: return None
    r = isqrt(n)
    return r if r * r == n else None

def small_factor(n):
    """Try the pattern rules first, then trial division."""
    # rule 1: perfect square  ->  n = r * r
    r = is_sq(n)
    if r and r > 1:
        return r

    # rule 2: twin product  ->  n = (6a-1)(6a+1),  (n+1)/36 square
    if (n + 1) % 36 == 0:
        a = is_sq((n + 1) // 36)
        if a and a > 0:
            return 6 * a - 1

    # rule 3: Fermat  ->  n = x^2 - y^2 = (x-y)(x+y)
    x = isqrt(n)
    if x * x < n: x += 1
    for _ in range(1000):                 # only pays off for close factors
        y = is_sq(x * x - n)
        if y is not None and x - y > 1:
            return x - y
        x += 1

    # fallback: 6k±1 wheel
    for d in (2, 3):
        if n % d == 0: return d
    k = 1
    while True:
        for d in (6*k - 1, 6*k + 1):
            if d * d > n: return None     # prime
            if n % d == 0: return d
        k += 1

def rep(n):
    if n <= 3:
        return str(n)
    d = small_factor(n)
    if d:
        return f"{rep(d)}*{rep(n // d)}"
    k, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    core = "2*3" if k == 1 else f"2*3*{rep(k)}"
    return f"({core}{s}1)"


# for i in range(1):
#     if i % 2 ==0 or i %3 ==0:
#         continue 
#     print((i,rep(i)))

# for i in range(1, 100000):
#     if i % 2 and i % 3:
#         s = rep(i)
#         assert eval(s) == i, (i, s)
# print("all match")

# from sympy import isprime

# def top_level_product(s):
#     d = 0
#     for c in s:
#         if c == '(': d += 1
#         elif c == ')': d -= 1
#         elif c == '*' and d == 0: return True
#     return False

# for i in range(5, 100000):
#     if i % 2 and i % 3:
#         assert top_level_product(rep(i)) != isprime(i), i
# print("all match")

# seen = {}
# for i in range(1, 100000):
#     if i % 2 and i % 3:
#         s = rep(i)
#         assert s not in seen, (i, seen[s])
#         seen[s] = i
# print(seen)


L = [(len(rep(i)), i) for i in range(5, 100000) if i % 2 and i % 3]
print(max(L), sum(l for l, _ in L) / len(L))