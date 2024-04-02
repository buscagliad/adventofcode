
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

danger = 0
for i in range(nscan):
    if scanner[i] == 0: continue
    k = (scanner[i] - 1) * 2
    if i % k == 0:
        danger += i * scanner[i]

print(danger)
    
