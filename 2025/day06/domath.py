
import numpy as np

numrows = 0
vals = np.zeros((6, 2000), dtype = int)
ops = ""
cephs = np.zeros((6, 2000), dtype = int)

def getceph(ch, i):
    v = 0
    for r in range(numrows):
        if i >= len(ch[r]): continue
        if ch[r][i] == ' ': continue
        d = int(ch[r][i])
        v = 10 * v + d
    #print("getceph: ", i, v)
    return v

def colblank(ch, i):
    for x in range(numrows):
        if i >= len(ch[x]): continue
        if ch[x][i] != ' ': return False
    return True
    
def init(fname):
    global vals, ops, numrows, cephs
    numcols = 0
    for l in open(fname):
        ll = l.strip().split()
        if ll[0] == '+' or ll[0] == '*':
            ops = ll
        elif len(ll) > 1:
            numcols = len(ll)
            for i, n in enumerate(ll):
                #print(i, n)
                vals[numrows, i] = int(n)
            numrows += 1
    row = 0
    ll = []
    sindex = 0
    for l in open(fname):
        if len(ll) >= numrows: break
        kl = len(l)
        #print(row, kl-1)
        sindex = max(sindex, kl-2)
        ll.append(l[:kl-1])
        row += 1
    #print(sindex)
    #
    # create cephs
    #
    # print first and last 14 characters
    #for r in range(numrows):
    #    print(ll[r][:16], "  ", ll[r][sindex-16:])
    ci = 0# ceph index
    r = 0
    #print(ll)
    blanks = 0
    for col in range(sindex+1):
        if colblank(ll, col):
            ci += 1
            r = 0
            blanks += 1
            continue
        cephs[r, ci] = getceph(ll, col)
        #print(r, ci, cephs[r, ci])
        r += 1
    #for r in range(numrows):
    #    print(cephs[r][:4], " ", cephs[r][numcols-4:numcols])
    #print("Number of blanks: ", blanks)
            
init('data.txt')
#print(cephs)
def compute(vs):
    total = 0
    col = 0
    for j, op in enumerate(ops):
        if op == '*': 
            prod = True
            p = 1
        else: 
            prod = False
            p = 0
        for i in range(numrows):
            v = vs[i, j]
            if prod: 
                if v == 0: v = 1
                p *= v
            else: 
                p += v
        total += p
        # print(j, p, total)
    return total
    
print("Part 1: ", compute(vals))
print("Part 2: ", compute(cephs))
# 5337541 is too low
