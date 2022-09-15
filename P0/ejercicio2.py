from cmath import sqrt


def fibonacci(n):
    if(n==1):
        return 1
    elif(n==0):
        return 0
    else:
        return fibonacci(n-1)+fibonacci(n-2)


f=open("entrada.txt","r")
n = int(f.read())
f.close()
fib = fibonacci(n)
f = open("salida.txt","w")
f.write(str(fib))
f.close
