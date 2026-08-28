# for x in range(1,100):
#     A = (((x-(3/4)) % 6)*2 )
#     if (A == 8.5 or A ==0.5 ) :
#         #print((x,A))
#         print((x ,(x*A %x)*2))

# for x in range(1,200):
#     A = (((x-(3/4)) % 6)*2 )
#     if (A == 8.5 and x%5 !=0  ) :
#         print((x,A))
#         #print((x ,(x*A %x)*2))
import math
L = {}
for x in range(1, 10000,2 ):
    B = (((x-(6/8)) % 6)*2 )
    D =(((x+2-(6/8)) % 6)*2 )
    if (B == 8.5 and D == 0.5  ) :
        L[x] = x+2

L2_Y = [k % v  for v in L.values() for k in L.keys() if k != v and v%k ==0 and k%v not in L.values()]
L2_X = [v % k  for k in L.keys() for v in L.values() if k != v and  k%v ==0 and v%k not in L.keys()]
L = {}

S = (set(L2_X) | set(L2_Y))
#print(S)
L2_X=[]
L2_Y=[]
P = []
for x in range(10001,100000,6):
    if x%2 == 0 or x%3 == 0:
        continue

    for k in S:
        if (x % k == 0) and k != 1 and k!=x :
            if k not in P:
                P.append(k)
            if x//k not in P:
                P.append(x//k)
print(len(P))

def N_P(N):
    L= []
    for k in P:
        if (N % k == 0) and k not in L:
            L.append(k)
    return print(f"Factors of {N}: {L}")
N_P(4126375141919523791919279)
N_P(132493841032476234197382753441972635419379826774981234765919364528454827197351)
N_P(4126375141919523791919271)
N_P(7334938410324762341973827534419726354193798261)
N_P(412637514191952379171729)

print(7334938410324762341973827534419726354193798261 % 2521)


