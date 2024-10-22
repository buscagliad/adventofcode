
oldr1 = 0
oldr0 = 0

def process(line):
    global oldr1, oldr0
    s = line.strip().split(', ')
    if len(s) < 5: return
    if s[0][0:2] == 'ip': return
    #if int(s[1]) == 0:
    #    return
    r0 = int(s[0])
    r1 = int(s[1])
    r2 = int(s[2])
    r3 = int(s[3])
    r4 = int(s[4])
    r5 = int(s[5])
    if (r0 != oldr0):
        oldr0 = r0
        print("RO: ", r0, "R1: ", r1, "R2: ", r2, 
            "R3: ", r3, "R4: ", r4, "R5: ", r5)


for l in open('flow.txt'):
    process(l)


N = 954
s = 0
for a in range(1, N+1):
    for b in range(1, N+1):
        if a * b == N:
            s += a
            break

print(s)
