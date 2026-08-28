Request

from math import isqrt
from square_of_squares_smart import ismagic
def is_sq(m):
    r=isqrt(m); return m>=0 and r*r==m
    nE=4225
    # offsets (half-differences) for root 65
    A,B,C,D=4056,3696,3000,2016
    g={'A':E+A,'B':E+B,'C':E+C,'D':E+D,'E':E,'F':E-D,'G':E-C,'H':E-B,'I':E-A}
    for row in ('ABC','DEF','GHI'):
        print('  ',[f"{g[k]}{'*' if is_sq(g[k]) else ''}" for k in row])
    print('squares =', sum(is_sq(v) for v in g.values()), 'of 9')
    print('MAGIC   =', ismagic(g))
    # why not magic: check the lines
    S=3*E
    lines={'R1':'ABC','R2':'DEF','R3':'GHI','C1':'ADG','C2':'BEH','C3':'CFI','Dg':'AEI','Da':'CEG'}
    print('line sums (magic would be', S, '):')
    for n,ks in lines.items():
        s=sum(g[k] for k in ks); 
        print(f'   {n}: {s}{"  OK" if s==S else "  off"}')
  