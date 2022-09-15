import random

def balance(str):

    if str[0]==']':
        return False

    sub = ''

    for i in range(0,len(str)):

        if len(sub)==0:
            sub+=str[i]
        elif sub[-1]=='[' and str[i]==']':
            sub = sub[:-1]
        else:
            sub+=str[i]

    if sub=='':
        return True
    else:
        return False



letters = ['[',']']
#str='[][]'
str = ''.join(random.choice(letters) for i in range(random.randrange(2,10,2)))
print(str)
print(balance(str))