import re

def check1(str):
    return re.search(r'^[a-zA-Z0-9_]+\s[A-Z]\Z',str)

def check2(str):
    return re.search(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}',str)

def check3(str):
    return re.search(r'[0-9]{4}[\s-][0-9]{4}[\s-][0-9]{4}[\s-][0-9]{4}',str)

print(check1("Apellido N"))
print(check2("a@ dlo.com"))
print(check3("1234 5678 9012 3456"))