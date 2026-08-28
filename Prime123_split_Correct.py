from math import isqrt

def split_by_form(n):
    if n %3 == 0:
        return [3 , int(n/3)]
    if n%2 == 0:
        return [2, n/2]
    if n % 6 == 1:
        r = isqrt(n)
        if r * r == n:
            return [r, r]                # 25, 49, 121, 169...
        else:
            A = int((n +1)/6)
            fact = 1
            if A %2 == 0:
                A=A-1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , n//i]
            split_by_form(A)
            A = int((n -1)/6)
            if A %2 == 0:
                A=A+1
            fact = 1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , n//i]
            split_by_form(A)
           
    elif n % 6 == 5:
        s = isqrt(n + 1)
        if s * s == n + 1:
            print(s-1, s+1)
            return [s - 1, s + 1]        # 35, 143, 323, 899...
        else:
            A = int((n +1)/6)
            fact = 1
            if A %2 == 0:
                A=A-1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , n//i]
            split_by_form(A)
            A = int((n -1)/6)
            if A %2 == 0:
                A=A+1
            fact = 1
            for i in range(A,1,-2):
                if n % i == 0:
                    fact = i
                    return [i , n//i]
            split_by_form(A)
    return None

def rep(n):
    if n <= 3:
        return str(n)
    for d in (2, 3):                     # peel 2s and 3s first
        if n % d == 0:
            return f"{d}*{rep(n // d)}"
    pair = split_by_form(n)
    if pair:
        a, b = pair
        return f"{rep(a)}*{rep(b)}"
    k, s = ((n+1)//6, "-") if (n+1) % 6 == 0 else ((n-1)//6, "+")
    core = "2*3" if k == 1 else f"2*3*{rep(k)}"
    return f"({core}{s}1)"



def sign_counts(s):
    plus = minus = 0
    i = 0
    while i < len(s) - 1:
        if s[i] in '+-' and s[i+1] == '1' and (i+2 >= len(s) or not s[i+2].isdigit()):
            if s[i] == '+': plus += 1
            else: minus += 1
        i += 1
    return plus, minus

def is_prime(N):
    is_prime = False
    if N % 2 == 0 or N%3 ==0: 
        print(f"NOT Prime = {rep(N)} = {N}")
        return

    pair = split_by_form(N)
    if pair:
        a, b = pair
        print(f"Not Prime = ({rep(a)}*{rep(b)}) = {a * b}")
        return

    print(f"Prime = {rep(N)} = {N}")


N = 412639
N = 412637
N = 4126375
N= 35
print(split_by_form(N))
is_prime(N)
