N = 5
limit = 100

coprimes = []
k_values = [k for k in list(range(5, limit+1 )) if k%2 !=0 and k%3 != 0]
def companions(a,k_values):
    k = 1
    while a* (6*k - 1)<= limit:
        if a* (6*k - 1) in k_values and a* (6*k - 1) not in coprimes:
            coprimes.append(a* (6*k - 1))
        k =k+1
    return coprimes 



coprimes = companions(1,k_values) 
 
    # --- BOOLEAN FILTER ---
print([k for k in coprimes])
filtered_k = [k+10 for k in k_values if k not in coprimes]

print("filtered k-values:", filtered_k)

print([k for k in k_values if k not in coprimes])
print([k+29*2 for k in k_values if k not in coprimes])


