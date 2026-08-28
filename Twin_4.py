from math import isqrt
for x in range(2,100):
    A = ((x+(1/x)) % x  )
    x1 = isqrt((2*x))
    A1 = ((x1+(1/(x1))) % x1  )
    #if (x*A %(x)) == 1.0:
    print(x ,(x*A %(x)),x1 , (x1*A1 %(x1)) )
    #x = x+2
    #A = (((1/2-(1/x))**-1)   )
    #if (x*A %(x)) == 1.0:
    #print(x ,A**-1 if A > 0 else A,(A %(x)) )
    #print(x ,(A-1),(A %(x))**-1 * x if A %(x) > 0 else A %(x))
# for x in range(2,1000):
#     tens_digit = (x % (60+(x+(x//60)))) // 10     #← your mod-6 wheel  (0,1,2,3,4,5)
#     units_digit =  x % 10            #← the base-10 wheel (0,1,2,3,4,5,6,7,8,9)
#     tens_digit2 = x % (60) // 10 
    
#     value = tens_digit*10 + units_digit
#     print(value, tens_digit ,tens_digit2, units_digit)