
import numpy as np

scanner = np.zeros(200, dtype=int)
nscan = 0

def process(line):
    global nscan
    w = line.strip().split()
    v = w[0][:len(w[0])-1]
    index = int(v)
    nscan = index + 1
    scanner[index] = int(w[1])

for line in open("data.txt"):
    process(line)

def getdanger (offset):    
    danger = 0
    tf = False
    for i in range(nscan):
        if scanner[i] == 0: continue
        k = (scanner[i] - 1) * 2
        if (offset + i) % k == 0:
            tf = True
            danger += i * scanner[i]
    return tf, danger

_, dgr = getdanger(0)
print("Part 1: severity of this layout is: ", dgr)


tf = True
wait = 2

while tf:
    tf, dgr = getdanger(wait)
    #print(tf, wait, dgr)
    if tf: wait += 4

print("Part 2: wait this long to get through unscathed: ", wait)
