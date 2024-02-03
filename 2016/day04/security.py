
import numpy as np

def checksum(l):
    rs = ""
    for i in range(5):
        mi = max(l)
        for i in range(256):
            if l[i] == mi:
                # print(mi, chr(i))
                mi = i
                break
        rs += chr(mi)
        l[mi] = 0
    return rs


alpha="abcdefghijklmnopqrstuvwxyz"
def decrypt(st, code):
    nstr = ""
    for a in st:
        if a == '-':
            nstr += ' '
        elif a.isdigit():
            break
        else:
            n = (ord(a) - ord('a') + code) % 26
            nstr += alpha[n]
    return nstr

def parse(line):
    letters = [0] * 256
    cksum = ""
    sector = 0
    inchksum = False
    for a in line.strip():
        if inchksum:
            if not a == ']':
                cksum += a
        elif a.islower():
            letters[ord(a)] += 1
        elif a.isdigit():
            sector = sector * 10 + int(a)
        elif a == '[':
            inchksum = True
            
    excksum = checksum(letters)
    if cksum == excksum:
        # print("REAL    ", sector)
        return True, sector
    return False, 0


val = 0
st = ""
st_code = 0
for line in open('data.txt'):
    real, code = parse(line)
    if real: 
        val += code
        s = decrypt(line, code)
        if "north" in s:
            st_code = code
            st = s
    
print("Part 1: sum of the valid code sectors is: ", val)
print("Part 2: NP: ", st, "code is: ", st_code)
            
            
