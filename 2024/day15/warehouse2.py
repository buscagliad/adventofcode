
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

grid = np.zeros([150,150], dtype = int)

ymax = 0
xmax = 0

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
#  0    clear and can move up
#  >=1  1 or more boxes encountered
# NOTE: xl..xr from y-1 are dense boxes containing only [] no walls or empties
def isclear(xl,xr,y):
    nboxes = 0
    boxes = False   # set to True if a box is encountered
    for x in range(xl, xr+1):
        if grid[x][y] == WID: return [(-1,-1,-1)]
        if grid[x][y] != EID: boxes = True
    if boxes:   # we encountered boxes:
        if debug: print("isclear: found boxes")
        if grid[xl][y] == BIDR:  # then the left part needs to be included
            xl -= 1
            if debug: print("isclear: xl / y: ", xl, y, "  grid: ", grid[xl][y])
        if grid[xr][y] == BIDL:  # then the right part needs to be included
            xr += 1
            if debug: print("isclear: xr / y: ", xr, y, "  grid: ", grid[xr][y])
        while grid[xl][y] == EID: xl += 1
        while grid[xr][y] == EID: xr -= 1
        bxl = -1
        bxr = -1
        blist = []
        for x in range(xl, xr+1):
            if bxl < 0 and grid[x][y] == BIDL: bxl = x
            if grid[x][y] == EID or x == xr:
                blist.append((bxl,x,y))
                bxl = -1
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
def moveboxes(r, d):
    global grid
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
            for k in range(cboxes+1, 0, -1):
                grid[r[0]+k*d[0]][r[1]] = grid[r[0]+(k-1)*d[0]][r[1]]
            grid[r[0]][r[1]] = EID
            return True
        else: # WALL
            return False
    #
    # moving up or down
    #
    else:
        done = False
        ulist = []
        xl = xr = r[0]
        y = r[1]
        clr = [(xl, xr, y)]
        nclr = []
        #print("VERTICAL")
        ulist.append((xl, xr, y))
        while not done:
            if debug: print("top of while loopwith: xl-xr = ", xl, xr, " y:", y)
            clrcount = 0
            for (xl, xr, y) in clr:
                y += d[1]
                if debug: print("Calling isclear with: xl-xr = ", xl, xr, " y:", y)
                nclr = isclear(xl, xr, y)
                if debug: print("nclr: ", nclr)
                #
                # if any 
                for nc in nclr:
                    if nc == (-1, -1, -1):
                        return False
                    if nc == (0, 0, 0):
                        clrcount += 1
                    else:
                        ulist.append(nc)
                if clrcount == len(nclr):
                    done = True
                    break
            clr = copy.deepcopy(nclr)
            #y += d[1]
                    
        #
        # if we get here, the list ulist is a full set of all
        # move (up or down) operations, the list was created 
        # starting at the robot, we will traverse the list
        # in reverse order
        #        
        for (xl, xr, y) in reversed(ulist):
            if debug: print("calling vertmove with: xl xr: ", xl, xr, " y0 y1", y, y+d[1])
            vertmove(xl, xr, y, y+d[1])
        return True

def moveRobot(a):
    global Rpos, grid
    delta = deltas[a]
    npos = posadd(Rpos, delta)
    if debug: print(a," Robot moves from: ", Rpos, " To: ", npos, "  Delta: ", delta, " Grid: ", grid[npos[0]][npos[1]], BIDL)
    if grid[npos[0]][npos[1]] == EID:
        grid[Rpos[0]][Rpos[1]] = EID
        Rpos = npos
        grid[Rpos[0]][Rpos[1]] = RID
    elif grid[npos[0]][npos[1]] >= BIDL:
        if moveboxes(Rpos, delta):
            Rpos[0] = npos[0]
            Rpos[1] = npos[1]
    

def processMoves(line):
    global debug
    m = 0
    for a in line.strip():
        moveRobot(a)
        m += 1
        if m < 28 and m > 32: debug = False
        else: debug = False
        if debug: pgrid(m)

def pgrid(m):
    global grid, ymax, xmax
    print("Move ", m)
    for y in range(ymax):
        for x in range(xmax):
            if (x,y) == Rpos: print('@', end="")
            else: print(idch(grid[x][y]), end="")
        print()
        
Pgrid = True
for l in open('data.txt'):
    if len(l) < 3: 
        Pgrid = False
        if debug: pgrid(0)
    if Pgrid:
        processGrid(l)
    else:
        # print("Rpos: ", Rpos)
        processMoves(l)

def gps():
    global grid, xmax, ymax
    gsum = 0
    for y in range(ymax):
        for x in range(xmax):
            if grid[x][y] == BIDL:
                gsum += 100 * y + x
    return gsum
print(xmax,ymax)

print("Part2: gps coord sum: ", gps())
# 1482035 is too high

def setrpos(x, y):
    global grid, Rpos
    if grid[x][y] != EID:
        print("Cannot set robot position to ", x, y, " already occupied")
    else:
        grid[Rpos[0], Rpos[1]] = EID
        Rpos = [x,y]
        grid[Rpos[0], Rpos[1]] = RID
        print("Robot position moved to ", Rpos)

setrpos(61, 32)
pgrid(101)
moveRobot('<')
moveRobot('^')
pgrid(102)
