
EMPTY='.'
EID=0
BOXES='O'
BID=1
ROBOT='@'
RID=2
WALL='#'
WID=3

BIDL=10
BIDR=11
debug = False
nmoves = 0


def countboxes(g, xm, ym):
    boxcount = errcount = 0
    for y in range(ym):
        for x in range(xm):
            if g[x][y] == BIDL:
                boxcount += 1
                if g[x+1][y] != BIDR:
                    errcount += 1
    return boxcount, errcount

def chid(c):
    if c == EMPTY: return EID
    if c == BOXES: return BID
    if c == ROBOT: return RID
    if c == WALL: return WID
    return -1

def idch(c):
    if c == EID : return EMPTY
    if c == BID : return BOXES
    if c == BIDL : return '['
    if c == BIDR : return ']'
    if c == RID : return ROBOT
    if c == WID : return WALL
    return -1

UP='^'
DOWN='v'
LEFT='<'
RIGHT='>'

deltas={}
deltas[UP] = [0,-1]
deltas[DOWN] = [0,1]
deltas[LEFT] = [-1,0]
deltas[RIGHT] = [1, 0]

Rpos = [0,0]

import numpy as np
import copy

MAXY=50
MAXX=100
grid = np.zeros([MAXX,MAXY], dtype = int)
ogrid = np.zeros([MAXX,MAXY], dtype = int)
ymax = 0
xmax = 0

def copygrid(a, b): # copy b into a
    for i in range(MAXX):
        for j in range(MAXY):
            a[i][j] = b[i][j]

def diffgrid(a, b, mv):
    ulx = uly = 1000
    lrx = lry = 0
    for i in range(MAXX):
        for j in range(MAXY):
            if a[i][j] !=  b[i][j] :
                ulx = min(i, ulx)
                uly = min(j, uly)
                lrx = max(i, lrx)
                lry = max(j, lry)
    print("Move: ", nmoves, mv)
    for j in range(uly-1, lry+2):
        for i in range(ulx-1, lrx+2):
            print(idch(a[i][j]), end="")
        print("  ", end="")
        for i in range(ulx-1, lrx+2):
            print(idch(b[i][j]), end="")
        print()
    print()
                
def valid(x,y):
    if x < 0 or x >= xmax: return False
    if y < 0 or y >= ymax: return False
    return True

def processGrid(line):
    global grid, xmax, ymax, Rpos

    xmax = max(xmax, len(line.strip())*2)
    for j, a in enumerate(line.strip()):
        h = chid(a)
        x0 = 2 * j
        x1 = x0 + 1
        if h == RID:
            grid[x0][ymax] = RID
            grid[x1][ymax] = EID
            Rpos = [x0, ymax]
            if debug: print(Rpos)
        elif h == BID:
            grid[x0][ymax] = BIDL
            grid[x1][ymax] = BIDR
        elif h == WID or h == EID:
            grid[x0][ymax] = h
            grid[x1][ymax] = h
        else:
            print("WHAT?")
 
    ymax += 1

def posadd(p, d):
    return [p[0]+d[0], p[1]+d[1]]
    
def possub(p, d):
    return [p[0]-d[0], p[1]-d[1]]

#
# look to see if there are any blockers above them (walls)
# isclear returns three values:
# -1    a wall exists
#  0    clear and can move up or down
#  >=1  1 or more boxes encountered
# NOTE: xl..xr from y-1 are define the left/right edge of a box
#       when referring to a robot:  xl == xr, thus
#       xl - xr < 2
def isclear(xl,xr,y):
    nboxes = 0
    boxes = False   # set to True if a box is encountered
    if y <= 0 or y >= ymax - 1:
        return [(-1,-1,-1)]
    if abs(xr - xl) > 1: 
        print("ERROR - cannot exceed 1 delta: ", xl, xr, y)
        return [(-1,-1,-1)]
    if xr == xl:
        if grid[xl][y] == BIDL:
            return [(xl,xl+1,y)]
        elif grid[xl][y] == BIDR:
            return [(xl-1,xl,y)]
        elif grid[xl][y] == WID: 
            return [(-1,-1,-1)] 
        else:
            return [(0,0,0)]

    for x in range(xl, xr+1):
        ## return 'blocked' if a wall is encountered
        if grid[x][y] == WID: return [(-1,-1,-1)]  
        ## if any of the grid points above are not empty, they must be boxes
        if grid[x][y] != EID: boxes = True
    if boxes:   # we encountered boxes:
        if debug: print("isclear: found boxes")
        blist = []
        if grid[xl][y] == BIDR:  # then the left part needs to be included
            blist.append((xl-1,xl,y))
            if debug: print("isclear: xl-1,xl / y: ", xl-1, xl, y, "  grid: ", grid[xl-1][y])
        if grid[xr][y] == BIDL:  # then the right part needs to be included
            blist.append((xr,xr+1,y))
            if debug: print("isclear: xl,xl+1 / y: ", xr, xr+1, y, "  grid: ", grid[xr][y])
        if grid[xl][y] == BIDL:
            blist.append((xl,xl+1,y))
            if debug: print("isclear: xl,xl+1: ", xl, xl+1, y, "  grid: ", grid[xl][y])
        return blist
    return [(0,0,0)]

#
# vertmove will mv all xl to xr from yf to yt
def vertmove(xl, xr, yf, yt):
    global grid
    for x in range(xl, xr+1):
        grid[x,yt] = grid[x,yf]
        grid[x,yf] = EID

#
# moving left or right is 'easy'
# moving up or down - need to look at 'connected'
# boxes
def moveboxes(r, d, a):
    global grid, debug
    cboxes = 0
    p = posadd(r, d)
    if debug: print("moveboxes: ", r, d)
    if abs(d[0]) > 0:   ## move left or right
        # find end of @[][]...
        while grid[p[0]][p[1]] >= BIDL:
            cboxes += 1
            p = posadd(p,d)
            if debug: print("cboxes: ", cboxes, " Pos: ", p, "  grid: ", grid[p[0]][p[1]])
        # p is now pointint to a WALL or and empty space EID
        if debug: print("cboxes: ", cboxes)
        if grid[p[0]][p[1]] == EID:
            if debug: pgrid(nmoves, a)
            for k in range(cboxes+1, 0, -1):
                grid[r[0]+k*d[0]][r[1]] = grid[r[0]+(k-1)*d[0]][r[1]]
            grid[r[0]][r[1]] = EID
            if debug: pgrid(nmoves, a)
            return True
        else: # WALL
            return False
    #
    # moving up or down
    #
    else:
        ulist = []
        xl = xr = r[0]
        y = r[1]
        clr = [(xl, xr, y)]
        nclr = []
        #print("VERTICAL")
        ulist.append((xl, xr, y))
        done = False
        while not done:
            if debug: print("top of while loopwith: xl-xr = ", xl, xr, " y:", y)
            clrcount = 0
            for (xl, xr, y) in clr:
                y += d[1]
                if y < 1 or y >= ymax-1: 
                    #done = True
                    return False
                    break
                if debug: print("Calling isclear with: xl-xr = ", xl, xr, " y:", y)
                nclr = isclear(xl, xr, y)
                if debug: print("nclr: ", nclr)
                #
                # if any 
                ecnt = 0
                for nc in nclr:
                    if nc == (-1, -1, -1):
                        return False
                    if nc == (0,0,0):
                        ecnt += 1
                    else:
                        if not nc in ulist:
                            ulist.append(nc)
                if ecnt == len(nclr): done = True
            clr = copy.deepcopy(nclr)
            if len(nclr) == 0: done = True
        #
        # if we get here, the list ulist is a full set of all
        # move (up or down) operations, the list was created 
        # starting at the robot, we will traverse the list
        # in reverse order
        #
        if debug and  len(ulist) > 0:
            pgrid(nmoves, a)
        for (xl, xr, y) in reversed(ulist):
            if debug: print("calling vertmove with: xl xr: ", xl, xr, " y0 y1", y, y+d[1])
            vertmove(xl, xr, y, y+d[1])
        if debug and len(ulist) > 0:
            pgrid(nmoves, a)
        return True

def moveRobot(a):
    global Rpos, grid, ogrid, debug
    delta = deltas[a]
    npos = posadd(Rpos, delta)
    if debug: print(a," Robot moves from: ", Rpos, " To: ", npos, "  Delta: ", delta, " Grid: ", grid[npos[0]][npos[1]], BIDL)
    if grid[npos[0]][npos[1]] == EID:
        grid[Rpos[0]][Rpos[1]] = EID
        Rpos = npos
        grid[Rpos[0]][Rpos[1]] = RID
        if debug: pgrid(nmoves, a)
    elif grid[npos[0]][npos[1]] >= BIDL:
        if moveboxes(Rpos, delta, a):
            Rpos[0] = npos[0]
            Rpos[1] = npos[1]
    
def processMoves(line, cb, ce):
    global debug, nmoves, grid, ogrid
    m = 0
    copygrid(ogrid,grid)
    for a in line.strip():
        moveRobot(a)
        m += 1
        nmoves += 1
        #print(nmoves,flush=True)
        #if m < 28 and m > 32: debug = False
        #else: debug = False
        if True:
            ncb, nce = countboxes(grid, xmax, ymax)
            if nce != ce or ncb != cb:
                print("Grid: box count: ", ncb, "   errors: ", nce, " at move: ", nmoves)
                exit(1)
        if 943 <= nmoves <= 944:
            debug = True
        else:
            debug = False
        if debug: 
            pgrid(m, a)
            diffgrid(ogrid, grid, a)
        copygrid(ogrid,grid)

def pgrid(m, a):
    global grid, ymax, xmax
    print("Move ", m, " : ", a)
    for y in range(ymax):
        print("{:3d} ".format(y), end = "")
        for x in range(xmax):
            if (x,y) == Rpos: print('@', end="")
            else: print(idch(grid[x][y]), end="")
        print()
        

def gps():
    global grid, xmax, ymax
    gsum = 0
    for y in range(ymax):
        for x in range(xmax):
            if grid[x][y] == BIDL:
                gsum += 100 * y + x
    return gsum
    
Pgrid = True
for l in open('data.txt'):
    if len(l) < 3: 
        if Pgrid: 
            cb, ce = countboxes(grid, xmax, ymax)
            if debug: print("Grid: box count: ", cb, "   errors: ", ce)
            print("Initial gps: ", gps())

        Pgrid = False
        if debug: pgrid(0,' ')
    if Pgrid:
        processGrid(l)
    else:
        # print("Rpos: ", Rpos)
        processMoves(l, cb, ce)

print("Part2: gps coord sum: ", gps())
# 1482035 is too high
# 1443542 is too low
pgrid(0,'X')
def setrpos(x, y):
    global grid, Rpos
    if grid[x][y] != EID:
        print("Cannot set robot position to ", x, y, " already occupied")
    else:
        grid[Rpos[0], Rpos[1]] = EID
        Rpos = [x,y]
        grid[Rpos[0], Rpos[1]] = RID
        print("Robot position moved to ", Rpos)
# setrpos(61, 32)
# pgrid(101)
# moveRobot('<')
# pgrid(102)
# moveRobot('^')
# pgrid(103)
