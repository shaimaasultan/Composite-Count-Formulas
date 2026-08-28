import math
L = {}
for x in range(1, 10000,2 ):
    B = (((x-(6/8)) % 6)*2 )
    D =(((x+2-(6/8)) % 6)*2 )
    if (B == 8.5 and D == 0.5  ) :
        L[x] = x+2
        #print((x, x+2) , (B,D) , (x%5,(x+2)%5))

L2_Y = [k % v  for v in L.values() for k in L.keys() if k != v and v%k ==0 and k%v not in L.values()]
L2_X = [v % k  for k in L.keys() for v in L.values() if k != v and  k%v ==0 and v%k not in L.keys()]
L = {}

S = (set(L2_X) | set(L2_Y))
L2_X=[]
L2_Y=[]
P = []
for x in range(99000,100000):
    if x%2 == 0 or x%3 == 0:
        continue
    L= []
    for k in S:
        if (x % k == 0) and k != 1 and k!=x and k not in L:
            L.append(k)
            L.append(x/k)
            L.append(math.prod(L)//x)
            if k not in P:
                P.append(k)
            if x/k not in P:
                P.append(x/k)
    if len(L) > 0:
        print((x,L))

#########################################################

signatures = []

for x in range(99000, 100000):
    if x % 2 == 0 or x % 3 == 0:
        continue

    factors = []
    for k in S:
        if k != 1 and k != x and x % k == 0:
            factors.append((k, x // k))

    if factors:
        # pure factor pairs
        sig_prod = 1
        for a, b in factors:
            sig_prod *= a * b

        signature = sig_prod // x
        signatures.append((x, factors, signature))
        print(x, factors, signature)

hidden = []
for x, factors, sig in signatures:
    if len(factors) <= 1 and sig > x**2:
        hidden.append((x, sig))

def N_P_signature(N):
    factors = []
    for k in P:
        if k != 1 and k != N and N % k == 0:
            factors.append((k, N // k))

    if not factors:
        print("No factors from P")
        return

    sig_prod = 1
    for a, b in factors:
        sig_prod *= a * b

    signature = sig_prod // N
    print("Factors:", factors)
    print("Signature:", signature)

N_P_signature(13249384103247623419738275344197263541937982677498123476591)