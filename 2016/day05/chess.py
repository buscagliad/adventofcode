
# Python 3 code to demonstrate the
# working of MD5 (byte - byte)

import hashlib


def getnextdigit(input_str, n):
    done = False
    while not done:
        n += 1
        hash_str = input_str + str(n)
        result = hashlib.md5(hash_str.encode())
        firstfive = result.hexdigest()[0:5]
        if firstfive == "00000":
            return result.hexdigest()[5], result.hexdigest()[6], n

def getcode(cd_str):
    code = ""
    scode = ['.', '.', '.', '.', '.', '.', '.', '.']
    n = 1
    while scode.count('.') > 0:
        c, ac, n = getnextdigit(cd_str, n)
        if len(code) < 8: code += c
        i = ord(c) - ord('0')
        if i >=0 and i < 8:
            #print("i: ", i,"  ac: ", ac)
            if scode[i] == '.' : scode[i] = ac
    code2 = ""
    for a in scode:
        code2 += a
    return code, code2

code, code2 = getcode("wtnhxymk")

print("Part 1: code is: ", code)
print("Part 2: code is: ", code2)

#print("Part 1: code is: ", getcode("wtnhxymk"))
