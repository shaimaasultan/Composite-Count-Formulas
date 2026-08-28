from math import isqrt

def is_square(N):
    """Return True if N is a perfect square (N >= 0)."""
    if N < 0:
        return False
    r = isqrt(N)          # exact integer floor of sqrt, works for arbitrarily large N
    return r * r == N

def triples_for_k(k):
    """All Pythagorean triples (k, s, k+d) having k as a leg, via s^2 = d(2k+d)."""
    out = []
    for d in range(1, (k*k) + 2):
        g = d*(2*k + d)          # the staircase gap
        s = isqrt(g)
        if s*s == g :             # gap is a perfect square -> triple
            out.append((k, s, k + d ))
    for k in out:
        print(f" k**2 = {k[0]**2},k={k[0]},s = {k[1]} ,d ={k[2]} , (d-s)**2 = {(k[2]-k[1])**2}, 2*k**2 - (d-s)**2 = {(2*k[0]**2-(k[2]-k[1])**2)} ,  3*k**2 - (d-s)**2 +(d-s)**2  = { (3*k[0]**2-(k[2]-k[1])**2)+((k[2]-k[1])**2) }  , 3*k**2 - (d-s)**2 ={(3*k[0]**2-(k[2]-k[1])**2)}")
        if (is_square(2*k[0]**2-(k[2]-k[1])**2)): 
            print("have squares")
            print(f"Target Sum = {(k[2]-k[1])**2 + (2*k[0]**2-(k[2]-k[1])**2) + k[0]**2 }")
    return (out)

def magic_pairs(k):
    """Opposite-cell pairs (a^2, b^2) with a^2 + b^2 = 2k^2, centred at k^2.
    Single test: 2*k^2 - a^2 must be a perfect square."""
    out, a = [], 0
    while a <= k:                    # a^2 <= k^2
        other = 2*k*k - a*a          # the opposite cell
        if is_square(other):         # <-- the only condition
            b = isqrt(other)
            if b > a:
                out.append((a*a, other))
        a += 1
    return out

def rect_lines_for_k(k):
    """Magic lines centred at k^2, via TWO gaps (d1, d2).
    Roots (k-d1, k, k+d2) with (k-d1)^2 + (k+d2)^2 = 2k^2:
    the diagonal of the a x b rectangle (a=k-d1, b=k+d2) equals k*sqrt(2),
    the diagonal of the k x k square. Gap condition: d1^2 + d2^2 = 2k(d1 - d2)."""
    out = []
    for a in range(0, k):              # a = small root = k - d1
        b2 = 2*k*k - a*a
        if is_square(b2):              # the single test
            b = isqrt(b2)              # b = big root = k + d2
            out.append((a, k, b, k - a, b - k))
    return out

def magic_lines(k):
    """Lines summing to 3k^2 for a magic square centred at k^2.
    Needs k as the HYPOTENUSE: s^2 + d^2 = k^2, then flankers (d-s)^2, (d+s)^2."""
    out = []
    for s in range(1, k):
        d2 = k*k - s*s
        d = isqrt(d2)
        if d*d == d2 and d >= s:          # s^2 + d^2 = k^2  (k is the hypotenuse)
            line = (d-s)**2 + k*k + (d+s)**2
            assert line == 3*k*k          # always holds
            out.append(((d-s)**2, k*k, (d+s)**2))
    return out

def lines_by_area(k):
    """Magic lines at centre k^2 found by the AREA condition:
    A = a*b is valid <=> 2(k^2 + A) and 2(k^2- A) are both perfect
    squares."""
    out = []
    for A in range(1, k*k + 1):
        if is_square(2*(k*k + A)) and is_square(2*(k*k- A)):
            apb, bma = isqrt(2*(k*k + A)), isqrt(2*(k*k- A))
            a, b = (apb- bma)//2, (apb + bma)//2
            if 0 < a < b:
                out.append((A, a, b))
    # rectangle area, sides
    return out


def winners(k , count_pairs , full =False):
    """Magic squares of squares at center k^2: pick two pairs as diagonals,
    the edges B=3k^2-A-C and D=k^2-A+C are FORCED and must also be squares."""
    from math import isqrt
    def sq(N):
        r = isqrt(N); return N >= 0 and r*r == N
    c = k*k
    corners = [(a*a, 2*c-a*a) for a in range(1,k) if sq(2*c-a*a) and isqrt(2*c-a*a) > k]
    if len(corners) >= count_pairs and full == False:
       return corners
    out = []
    for i in range(len(corners)):
        for j in range(len(corners)):
            if i == j: continue
            for A in corners[i]:
                for C in corners[j]:
                    B, D = 3*c-A-C, c-A+C
                    if B > 0 and D > 0 and sq(B) and sq(D):
                        out.append((A, C, B, D))     # a full 9-square solution
    return out

from math import isqrt

def search_closure(kmax):
    """Search for a full closure (a 9-square) via the sin2φ offsets.
    For each k, offsets are δ/k² = sin2φ; a 9-square needs FOUR that close:
    sin2φ₃ = sin2φ₁+sin2φ₂  and  sin2φ₄ = sin2φ₁−sin2φ₂, all real apexes."""
    for k in range(2, kmax):
        c = k*k
        # offsets of the genuine apexes (both cells square): δ = k² − a²
        offs = set()
        for a in range(1, k):
            b2 = 2*c - a*a; b = isqrt(b2)
            if b*b == b2 and b > k:
                offs.add(c - a*a)             # δ = k² sin2φ, an integer here
        if len(offs) < 4:
            continue
        ol = sorted(offs)
        for P in ol:
            for Q in ol:
                if Q >= P: break
                if P + Q <= c and (P+Q) in offs and (P-Q) in offs:   # closure + amplitude
                    return k, (P, Q, P+Q, P-Q)                        # a real 9-square
    return None

N =1105 #isqrt(195364) #isqrt(388962) #isqrt(194481)# isqrt(195364)
for i in range(400 , 1200):
#print(triples_for_k(N))
    print(magic_pairs(i))
    print(winners(i , 8 , True))
    print(search_closure(i))
# M = []
# for i in range(1,500):
#     L = rect_lines_for_k(i)
#     A = (i,len(L))
#     if A not in M and len(L) >= 6:
#         M.append(A)
#         print(A)
#     if len(L) >= 6:
#         print(L)
    for L in magic_lines(i):
        print(L , [isqrt(x) for x in L], "sum =", sum(L))
# wanted = 7
# for i in range(1000,5000):
#     L1 = lines_by_area(i)
#     if (len(L1) >= wanted):
#         print(f"| lines_by_area = {len(L1)} | {i} | {L1}")
#         print(f"================================")
#     L2 = rect_lines_for_k(i)
#     if(len(L2) >= wanted):
#         print(f"| rect_lines_for_k = {len(L2)} | {i} | {L2}")
#         print(f"================================")
#     L3 = winners(i,wanted)
#     if (len(L3) >= wanted) :
#         print(f"| winners = {len(L3)} | {i} | {L3} ")
#         print(f"================================")