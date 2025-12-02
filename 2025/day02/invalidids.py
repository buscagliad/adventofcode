debug = False

def goodrange(r1, r2):
    if len(r1) % 2 == 1 and len(r2) % 2 == 1 and len(r1) == len(r2):
        return True
    return False

def createnum(r, n):
    g = str(r)
    rn = ""
    for i in range(n):
        rn += g
    return int(rn)

def findbadids1(r1, r2):
    #print(r1, r2)
    badids = []
    n = len(r1)//2
    m = 10 ** n
    minv = int(r1)
    maxv = int(r2)
    #print("n = ", n)
    start = int(r1[:n])
    end = int(r2[:n])+1
    for s in range(start, end):
        v = s + m * s
        if v >= minv and v <= maxv:
            badids.append(v)
    return badids
#    k      0  1  2   3    4    5     6     7     8      9      10
repdigits1=[[],[],[1],[],  [2], [],   [3],  [], [4],    [],   [5]]
repdigits2=[[],[],[1],[1],[1,2],[1],[1,2,3],[1],[1,2,4],[1,3],[1,2,5]]
    
def sumbadids2(r1, r2, repdigits):
    rv = 0
    rvset = set()
    #print(r1, r2)
    l1 = len(r1)
    l2 = len(r2)
    minv = int(r1)
    maxv = int(r2)
    for k in range(l1, l2+1):
        for n in repdigits[k]:
            if l1 != l2 and k == l1:
                start = int(r1[:n])
                end = 10 ** (len(r1))//n - 1
                if (debug): print("A  start: ", start, " end: ", end, " r1: ", r1, " r2: ",r2, "  k: ", k, "  n: ", n)
            elif l1 != l2 and k == l2:
                start = 10 ** (n-1)
                end = int(r2[:n])+1
                if (debug): print("B  start: ", start, " end: ", end, " r1: ", r1, " r2: ",r2, "  k: ", k, "  n: ", n)
            else:
                start = int(r1[:n])
                end = int(r2[:n])+1
                if (debug): print("C  start: ", start, " end: ", end, " r1: ", r1, " r2: ",r2, "  k: ", k, "  n: ", n)

            #print(r1)            
            reps = k // n
            #print("n = ", n)
            for s in range(start, end):
                v = createnum(s, reps)
                if v >= minv and v <= maxv:
                    if v not in rvset:
                        if (debug): print(" V: ", v, end=" ")
                        rv += v
                        rvset.add(v)
            if (debug): print()
    return rv

badidsum1 = 0
badidsum2 = 0

for ln in open('data.txt'):

    pairs = ln.strip().split(',')

    ids = []
    for p in pairs:
        ids.append(p.split('-'))

    for idx in ids:
        r1 = idx[0]
        r2 = idx[1]

        # badids1 = findbadids1(r1, r2)
        # print(badids1)
        # badidsum1 += sum(badids1)
        badidsum1 += sumbadids2(r1, r2, repdigits1)
        badidsum2 += sumbadids2(r1, r2, repdigits2)

print("Part 1: ", badidsum1)
print("Part 2: ",badidsum2)
# Part 1 55916882972
