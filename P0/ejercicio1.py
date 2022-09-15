from math import isqrt

def criba(n):
    list = [True] * (n-1)

    for i in range(2,isqrt(n)+1):
        if list[i-2]:
            for j in range(i,int(n/i)+1):
                list[i*j-2] = False

    return list



list = (criba(200))
for i in range(0,len(list)):
    if list[i]:
        print(i+2)