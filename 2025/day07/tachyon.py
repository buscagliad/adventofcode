
import numpy as np

tgrid = np.zeros([300,300], dtype = int)
ways = np.zeros([300, 300], dtype = int)
yrow = 0
xcol = 0
START = -1
EMPTY = 0
BRANCH = -2
TLINE = 1
startx = 0
starty = 0

def init(fname):
    global yrow, xcol, startx, starty
    for l in open(fname, "r"):
        if len(l) < 2: break
        xcol = 0
        for c, a in enumerate(l):
            if a == '^':
                tgrid[yrow, c] = BRANCH
            elif a == 'S':
                startx = xcol
                starty = yrow
                tgrid[yrow, c] = START
            #elif a != '.':
            #    break
            xcol += 1
        yrow += 1

def pmat(g, nr, nc):
    numsp = 0
    for x in range(nr):
        for y in range(nc):
            if g[x,y] == EMPTY: print(".", end="")
            elif g[x,y] == BRANCH: 
                print("^", end = "")
                if g[x-1,y] == TLINE: numsp += 1
            elif g[x,y] == START: print("S", end = "")
            elif g[x,y] == TLINE: print("|", end = "")
        print()
    print(numsp)

def numsplits(g, nr, nc):
    numsp = 0
    for x in range(nr):
        for y in range(nc):
            if g[x,y] == BRANCH: 
                if g[x-1,y] == TLINE: numsp += 1
    return numsp

def nextrow(g, row):
    global startx, starty, ways
    if row == 0:
        g[starty, startx] = TLINE
        ways[starty, startx] = 1
        #print(starty, startx, ways[starty, startx])
        return
    for x in range(xcol):
        if g[row, x] == EMPTY:
            ways[row,x] += ways[row-1,x]
    for x in range(xcol):
        if g[row,x] == EMPTY: 
            #print("ROW, COL", row, x)
            #ways[row,x] = ways[row-1,x]
            if g[row-1,x] == TLINE: 
                g[row,x] = TLINE
        elif g[row,x] == BRANCH:
            g[row, x-1] = TLINE
            g[row, x+1] = TLINE
            ways[row, x-1] += ways[row-1,x]
            ways[row, x+1] += ways[row-1,x]

    # if row % 2 == 1:
        # for x in range(xcol):
            # ways[row, x] = ways[row-1, x]
        # return
            
    # for x in range(xcol):
        # if g[row, x] == EMPTY:
            # ways[row, x] += ways[row-1,x]
    # for x in range(xcol):
        # if g[row, x] == BRANCH:
    
init('data.txt')
#pmat(tgrid, yrow, xcol)

def pdb(w, r, g):
    #print("pdb: ", r)
    #print(g[r][:15], r, sum(w[r]))
    for l in range(15):
        if g[r][l] == BRANCH:
            print(" *", end = "")
        else:
            print("  ", end = "")
    print()
    print(w[r][:15], r, sum(w[r]))

ns = 0
for r in range(yrow):
    nextrow(tgrid, r)
    #pdb(ways, r, tgrid)
    

#pmat(tgrid, yrow, xcol)
print("Part 1: ", numsplits(tgrid, yrow, xcol))

# Part 2 - 3372 is too low
print("Part 2: ", sum(ways[yrow-1]))
