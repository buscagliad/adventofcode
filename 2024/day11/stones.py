import math
import copy as cp
import numpy as np

test1 = [125,17]

data = [0, 4, 4979, 24, 4356119, 914, 85734, 698829]

def stone(n):
    if n == 0: return 1, -1
    d = int(math.log10(n)) + 1
    if d % 2 == 0:
        m = 10 ** (d // 2)
        return n // m, n % m
    else:
        return 2024 * n, -1
        
st = {}
for i in data:
    st[i] = 1

turn = []

p1sum = 0
p2sum = 0

for i in range(1,76):
    turn.clear()
    for q in st:
        s = q
        if st[q] == 0: continue
        a, b = stone(s)
        #print(q, "-->", a, b)
        turn.append((a, s, st[s]))
        if b>=0: turn.append((b, s, st[s]))

    for k in st:
         st[k] = 0

    for t, k, add in turn:
        if t in st:
            st[t] += add
        else: 
            st[t] = add
    tsum = 0
    for x in st:
        tsum += st[x]
    if i == 25: p1sum = tsum
    p2sum = tsum

print("Part 1: stones after 25 blinks: ", p1sum)
print("Part 2: stones after 75 blinks: ", p2sum)
