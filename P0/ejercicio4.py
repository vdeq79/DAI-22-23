import re

def check1(str):
    return re.search(r'(?!\s)\s[A-Z]\Z',str)

print(check1("Apellido N"))