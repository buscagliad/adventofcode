import numpy as np

DEBUG = False



def pgrid(g, n):
    for j in range(n):
        for i in range(n):
            if g[j,i]: print('#', end = "")
            else: print(' ', end = "")
        print()
        
def gline(g, x1, y1, x2, y2):
    for i in range(min(x1,x2), max(x1,x2)+1):
        for j in range(min(y1,y2), max(y1,y2)+1):
            #print(i,j)
            g[j,i] = 1

def findlast(ln, n):
    while n and not ln[n]: n -= 1
    return n

def findfalse(ln, n, s):
    while ln[s]: 
        if s >= n: return -1
        s += 1
    return s

def fgrid(g, n):
    for j in range(n):
        state = 0 ## always start a new line with state off
        onoff = 0
        i = 0
        lastN = findlast(g[j], n)
        while(i < lastN):
            if g[j,i]: 
                i = findfalse(g[j], n, i)
                onoff = g[j-1,i]
                continue
            g[j,i] = onoff
            i += 1
                
def insertEveryOtherZero(m):
    lm = len(m)
    for n in range(lm):
        m.insert(2*n, 0)

def makemap(data):
    mm = []
    for a in data:
        if a in mm: continue
        mm.append(a)
    mm.sort()
    insertEveryOtherZero(mm)
    return mm

def boxcount(g, x1, y1, x2, y2):
    s = 0
    minx = min(x1, x2)
    miny = min(y1, y2)
    maxx = max(x1, x2)+1
    maxy = max(y1, y2)+1
    for y in range(miny, maxy):
        s += sum(g[y][minx:maxx])
    #print(minx, maxx, miny, maxy, s, (maxx-minx)*(maxy-miny))
    return s == (maxx-minx)*(maxy-miny)

def init(fname):
    gx=[]
    gy=[]
    grid = np.zeros((500,500), dtype=int)
    areas=[]
    first = True
    for l in open(fname, 'r'):
        if len(l) < 3: break
        m = l.strip().split(',')
        gx.append(int(m[0]))
        gy.append(int(m[1]))
    compx = makemap(gx)
    compy = makemap(gy)
    for i, x1 in enumerate(gx):
        y1 = gy[i]
        for j in range(i+1, len(gx)):
            x2 = gx[j]
            y2 = gy[j]
            areas.append([(abs(x2-x1)+1)*(abs(y2-y1)+1),compx.index(x1), compy.index(y1), compx.index(x2), compy.index(y2)])
    areas.sort(reverse=True)
  
    N = len(gx)

    print("Part 1: ", areas[0][0])
    #print(areas[0])
    x1 = compx.index(gx[0])
    y1 = compy.index(gy[0])
    for i in range(N):
        x2 = compx.index(gx[i])
        y2 = compy.index(gy[i])
        gline(grid, x1, y1, x2, y2)
        x1 = x2
        y1 = y2
    gline(grid, x1, y1, compx.index(gx[0]), compy.index(gy[0]))
    #pgrid(grid, N)
    fgrid(grid, N)
    #pgrid(grid, N)
    for a, x1, y1, x2, y2 in areas:
        if boxcount(grid, x1, y1, x2, y2):
            print("Part 2: ", a)
            exit(1)
  
init("data.txt")

#print(xys)
#exit(1)

#print("Part 1: ", maxrec(xys))
# Part 1:  4755278336 - correct

#print("Part 2: ", dotris())
# Part 2:  164017360 - too low
#Part 2:  1534043700 - correct
# Part 2:  4566760900 - too high
#print(xys)
