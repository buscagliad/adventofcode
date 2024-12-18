
import numpy as np

maize = []
xmax = 0
ymax = 0
Epos = None
Spos = None

East = (1,0)
South = (0,1)
West = (-1,0)
North = (0,-1)

def valid(p):
    global maize
    x = p[0]
    y = p[1]
    if x <= 0 or x >= xmax: 
        print("valid: x = ", x)
        return False
    if y <= 0 or y >= ymax: 
        print("valid: y = ", y)
        return False
    if maize[x][y] == '#': 
        print("valid: maize[x][y] = ", maize[x][y])
        return False
    return True

def processGrid(line):
    global maize, xmax, ymax, Spos, Epos


def process(fn):
    global xmax, ymax, Epos, Spos
    xmax = 0
    ymax = 0
    for l in open(fn):
        maize.append(l.strip())
        xmax = max(xmax, len(l.strip()))
        for j, a in enumerate(l.strip()):
            if a == 'S':
                Spos = (j, ymax)
            if a == 'E':
                Epos = (j, ymax)
        ymax += 1

process('test1.txt')
print(Spos, Epos)
        # position, direction, cost
q = [[Spos, East, 0]]
track={}
n = 100
while q and n > 0:
    n = n - 1
    (p, d, c) = q.pop()
    print("p", p, "  d", d, "  c", c, "  Epos", Epos)
    if p == Epos:
        print(p,d,c)
        break
    if not valid(p): 
        print(p, " is not valid")
        continue
    if (p,d) not in track: 
        track[(p,d)] = c
    elif track[(p,d)] < c: 
        track[(p,d)] = c
    
    for dirs in [(1,0),(0,1),(-1,0),(0,-1)]:
        if dirs == d:
            q.append(((p[0]+dirs[0], p[1]+dirs[1]),dirs,c+1))
        else:
            q.append((p,dirs,c+1000))

print(maize[Epos[0]][Epos[1]])
print(maize[Spos[0],Spos[1]])

