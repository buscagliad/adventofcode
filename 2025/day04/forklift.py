import numpy as np

gridA=np.zeros((200,200), dtype = int)
gridB=np.zeros((200,200), dtype = int)
xsz = 0
ysz = 0

EMPTY = 0
ROLL = 1

def numpaper(n, m, grid):
    np = 0
    if grid[m][n] == EMPTY: return 8
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0: continue
            if dx + n < 0: continue
            if dy + m < 0: continue
            if dx + n >= xsz: continue
            if dy + m >= ysz: continue
            if grid[dy + m][dx + n] == ROLL: np += 1
    return np

def init(fname, grid):
    global xsz, ysz
    for l in open(fname, "r"):
        if (len(l) < 2): continue
        xsz = max(xsz, len(l.strip()))
        for n in range(xsz):
            if l[n] == '@':
                grid[ysz][n] = ROLL
        ysz += 1
    #print(grid)
    #print(xsz, ysz)
    
init('data.txt', gridA)
count = 0



## B <-- A
def copyem(B, A):
    global xsz, ysz
    for i in range(xsz):
        for j in range(ysz):
            B[j][i] = A[j][i]

def cycle(gridA, gridB):
    num = 0
    copyem(gridB, gridA)
    for j in range(0, ysz):
        for i in range(0, xsz):
            np = numpaper(i, j, gridA)
            if np < 4: 
                mark = 'x'
                num += 1
                gridB[j][i] = EMPTY
            else: mark = gridA[j][i]
    return num

count = cycle(gridA, gridB)

print("Part 1: ", count)
Afirst = False
nc = count
while nc > 0:
    if Afirst:
        nc = cycle(gridA, gridB)
        Afirst = False
    else:
        nc = cycle(gridB, gridA)
        Afirst = True
    count += nc
    #print (nc, count)
        
print("Part 2: ", count)
