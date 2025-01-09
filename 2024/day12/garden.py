
import numpy as np

grid = np.zeros([150,150], dtype = int)
selected = np.zeros([150,150], dtype = int)
used = np.zeros([150,150], dtype = int)

ymax = 0
xmax = 0

def valid(x,y):
    if x < 0 or x >= xmax: return False
    if y < 0 or y >= ymax: return False
    return True

def process(line):
    global grid, xmax, ymax

    xmax = max(xmax, len(line.strip()))
    for i, a in enumerate(line.strip()):
        h = ord(a)
        grid[i][ymax] = h
    ymax += 1

NORTH=0
EAST=1
SOUTH=2
WEST=3

DELTAS = [(0,-1),(1,0),(0,1),(-1,0)]
deltax = [0,1,0,-1]
deltay = [-1,0,1,0]
#
# isboundary will determine if x+/-1 or y+/-1 is different from x,y
# the delta is
#
def isboundary(grid, x, y):
    g = grid[x][y]
    for dx,dy in DELTAS:
        if (grid[x][y] != grid[x+dx][y+dy]): return True
    return False


def valid(v, x, y):
    if x < 0 or y < 0: return False
    if x >= xmax or y >= ymax: return False
    if grid[x][y] == v: return True
    return False

#
# perim can only be called with the first 
# grid point seen in getparams
#
import heapq
from collections import deque

def perset(s, v, x, y):
    global selected
    s.clear()
    q = deque()
    q.append((v, x, y))
    while q:
        (v, x, y) = q.popleft()
        if not valid(v,x,y): continue
        if selected[x][y]: continue
        if (x,y) in s: continue
        selected[x][y] = 1
        s.add((x,y))
        q.append((v, x-1, y))
        q.append((v, x+1, y))
        q.append((v, x, y+1))
        q.append((v, x, y-1))
        #q.append((v, x, y-1))


    

def getparams(v):
    perim = 0
    area = 0
    first = True
    for i in range(xmax):
        for j in range(ymax):
            if grid[i][j] == v: 
                area += 1
                if first:
                    g_perim = 0
                    perim = perim(v, i, j)
                    first = False
    return area, perim

def getcoord(s):
    global selected
    for x in range(xmax):
        for y in range(ymax):
            if selected[x][y] == 0:
                return x, y
    return -1, -1

#
# s is a set of contiguous x,y parameters that form 
# a contiguous garden.  if x,y in s, then at least 
# one of x-1,y, x+1,y x,y-1 and x,y+1 are in s
#
def perim(s):
    p = 0
    for (x, y) in s:
        if (x+1, y) not in s: p += 1
        if (x-1, y) not in s: p += 1
        if (x, y-1) not in s: p += 1
        if (x, y+1) not in s: p += 1
    return p

       

def edge(nesw, x, y):
    nx = x + DELTAS[nesw][0]
    ny = y + DELTAS[nesw][1]
    if nx < 0 or nx >= xmax: return True
    if ny < 0 or ny >= ymax: return True
    if grid[nx][ny] != grid[x][y]: return True
    return False
    
def pset(s):
    xx = yx = 0 
    xn = yn = 1000
    for x,y in s:
        xx = max(x, xx)
        yx = max(y, yx)
        xn = min(x, xn)
        yn = min(y, yn)
    for y in range(yn, yx+1):
        for x in range(xn, xx+1):
            if (x,y) in s:
                print(chr(grid[x][y]), end="")
            else:
                print(" ", end="")
        print()
    return xn, xx, yn, yx
 
    
#
# s is a set of contiguous x,y parameters that form 
# a contiguous garden.  if x,y in s, then at least 
# one of x-1,y, x+1,y x,y-1 and x,y+1 are in s
#
def linperim(s):
    p = 0

    xset=set()
    yset=set()
    l = 0
    ##
    ## find the starting point: 
    ##
    startx = starty = 1000
    for (x, y) in s:
        if startx > x:
            startx = x
            starty = y
        elif startx == x and starty > y:
            starty = y
    print("Start x/y: ", startx, starty)
    xn,xx,yn,yx = pset(s)
    used=set()
    curdir = SOUTH
    predir = (curdir+2) % 4
    done = False
    x = startx
    y = starty
    
    while not done:
        prevp = (x + deltax[predir], y + deltay[predir])
        nextp = (x + deltax[curdir], y + deltay[curdir])
        if not nextp in s:
            print("A Edge counted: ", x,y)
            found = False
            while not found:
                curdir = (curdir + 1) % 4
                predir = (curdir + 2) % 4
                nextp = (x + deltax[curdir], y + deltay[curdir])
                if nextp in s  and  nextp not in used: found = True
            used.add((x,y))
            l += 1
            (x,y) = nextp
        elif (x,y) in s:
            if not prevp in s:
                print("B Edge counted: ", x,y)
                l += 1
            used.add((x,y))
            (x,y) = nextp
        else:
            (x,y) = prevp
            used.add((x,y))
            print("C Edge counted: ", x,y)
            l += 1
            curdir = (curdir + 1) % 4
            predir = (curdir + 2) % 4
        if (x,y) == (startx, starty): 
            print("Done at ", x, y)
            done = True
    # for x,y in s:
        # if edge(EAST, x, y): l+= 1
        # if x > 0 and x < xmax:
            # if grid[x-1][y] == grid[x+1][y]:
                # l += 0
            # else:
                # l += 1
        # if y > 0 and y < ymax:
            # if grid[x][y-1] == grid[x][y+1]:
                # l += 0
            # else:
                # l += 1
    print("Linear perim: ", l)
    return l
    
    started = False
    xlist = set()
    ylist = set()
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            if (x,y) in s:
                yset.add((x,y))
                if not started: 
                    if not (x,y-1) in s:
                        ylist.add((x,y))
                        l += 1
                started = True
            else:
                if started: 
                    if (x,y-1) in s:
                        ylist.add((x,y))
                        l += 1
                started = False
    started = False
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in s:
                print(chr(grid[x][y]), end="")
                if not started:
                     if not (x-1,y) in s: 
                        ylist.add((x,y))
                        l += 1
                started = True
            else:
                if started: 
                     if (x-1,y) in s: 
                        ylist.add((x,y))
                        l += 1
                print(' ', end="")
                started = False
        print()
    print("Linear perim: ", l)
    print("Add list X: ", xlist, "  Y: ", ylist)
    return l
        
def surrounded(s, x, y):
    p = 0
    if (x+1, y) in s: p += 1
    if (x-1, y) in s: p += 1
    if (x, y-1) in s: p += 1
    if (x, y+1) in s: p += 1
    return p

def openedges(s, x, y):
    p = 4
    if (x+1, y) in s: p -= 1
    if (x-1, y) in s: p -= 1
    if (x, y-1) in s: p -= 1
    if (x, y+1) in s: p -= 1
    return p

def sumb(b, x0, x1, y):
    s = 0
    #print("sumb ", x0, x1, y)
    for x in range(x0, x1):
        s += b[x][y]
    return s
#
# returns True if box is 'surrounded'
# by the garden markers in b
#
def setbox(b, n, x, y, w, h):
    sx = x      # starting x position
    sy = y
    ex = -1
    ey = -1
    if x >= w or y >= h: return False   # x and y must be in the garden box b
    while x < w and y < h and b[x][y] == 0: 
        b[x][y] = n
        x += 1
    x -= 1
    ex = x
    while y+1 < h and sumb(b,sx, x+1, y+1) == 0:
        y += 1
        ey = y
        for a in range(sx, x+1):
            b[a][y] = n
    #
    # check if ex or ey is at edge - if so
    # return False
    #
    if sx < 1 or sy < 1 or ex + 1 >= w or ey + 1 >= h: return False

    # For the box to be contained, all b elements must be either
    # n or -1
    for x in range(sx-1, ex+2):
        for y in range(sy-1, ey+2):
            # excluding corner points
            if x == sx-1 and y == sy-1: continue
            if x == ex+1 and y == sy-1: continue
            if x == sx-1 and y == ey+1: continue
            if x == ex+1 and y == ey+1: continue
            if b[x][y] != n and b[x][y] != -1: 
                return False
    return True
            
#
# bound in a width x height array where a -1 indicates
# an element of the garden.  Any box found that is contained
# on all four sidex is a 'contained box' and is countend 
# seperately - box + contained box = all boxes in garden
def countrectangles(bound, width, height):
    n = 1
    cn = 0
    for x in range(width):
        for y in range(height):
            if bound[x][y] != 0: continue
            else: surrounded = setbox(bound, n, x, y, width, height)
            if surrounded: cn +=1
            else: n += 1
    return n-1, cn

visited = {}

def isvalid(g, x, y, v):
    global visited
    if (x,y) in visited: return False
    if grid[x][y] != v: return False
    for nx, ny in [(x-1,y), (x+1, y), (x, y-1), (x, y+1)]:
        visited[(x,y)] = 1
        if grid[nx][ny] != v: return True
    return False
    

def countperim(g, x, y):
    global visited
    v = g[x][y]
    visited.clear()
    visited[(x,y)] = 2
    startx = x
    starty = y
    s = 0
    q = [(x+1,y,1,0),(x-1,y,-1,0),(x,y-1,0,-1),(x,y+1,0,1)]
    dx = 0
    dy = 0
    count = 0
    while q:
        x,y,ddx,ddy= q.pop()
        if (startx, starty) == (x,y): break
        if isvalid(g, x, y, v):
            visited[(x,y)] = 1
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx = x + dx
                ny = y + dy
                if (nx,ny) in visited: continue
                if isvalid(g, nx, ny, v):
                    q.append((nx,ny,dx,dy))
                    if not dx == ddx or not dy == ddy:
                        count += 1
    print("VISITED: ", visited)
    return count
                    
#
# compute the number of linear sides of
# the set s
#
def sides2(s, debug = False):
    print(s)
    if (len(s) == 1): return 4
    #
    # find upper left corner
    #
    ulx = 9999
    uly = 9999
    lrx = -1
    lry = -1
    dx = 0
    dy = 0
    for (x, y) in s:
        ulx = min(ulx, x)
        uly = min(uly, y)
        lrx = max(lrx, x)
        lry = max(lry, y)
    height = lry-uly+1
    width = lrx-ulx+1
    bound = np.zeros([width, height], dtype=int)
    #print("Line 231", s)
    # offset by 1 in x and y to put a boundary around bound
    for (x,y) in s:
        bound[x-ulx][y-uly] = -1
    # for b in range(height):
        # for a in range(width):
            # print(bound[a][b], flush=True, end=" ")
        # print()
    n, cn = countrectangles(bound, width, height)
    rv = 4 + 2*n + 4*cn
    if debug:
        print("Rectangles: ", n, cn, rv)
        for y in range(height):
            for x in range(width):
                print(f"{bound[x][y]:4}", end="")
            print()
    (x,y) = s.pop()
    print("new counter: ", countperim(grid, x, y))
    return rv

def getdeltas(dx, dy):
    if dx == 0 and dy == 1:
        return [(0,1),(1,0),(-1,0)]
    elif dx == 0 and dy == -1:
        return [(1,0),(0,-1),(-1,0)]
    elif dx == 1 and dy == 0:
        return [(0,1),(1,0),(0,-1)]
    elif dx == -1 and dy == 0:
        return [(0,1),(0,-1),(-1,0)]
    print("ERROR in getdeltas: ", dx, dy)
    exit(1)

def sidevalid(x, y, mx, my):
    if x < 0 or y < 0: return False
    if x >= mx or y >= my: return False
    return True
#
# compute the number of linear sides of
# the set s
#
def sides(s):
    if (len(s) <= 2): return 4
    #
    # find upper left corner
    #
    ulx = 9999
    uly = 9999
    lrx = -1
    lry = -1
    dx = 0
    dy = 1
    for (x, y) in s:
        ulx = min(ulx, x)
        uly = min(uly, y)
        lrx = max(lrx, x)
        lry = max(lry, y)
    height = lry-uly+3
    width = lrx-ulx+3
    bound = np.zeros([width, height], dtype=int)
    print("bound: w: ", width, " h: ", height)
    #print("Line 231", s)
    #
    # fill in bound with data from s
    #
    for (x,y) in s:
        bound[x-ulx+1][y-uly+1] = -1
    y = 1
    for x in range(width):
        if bound[x+1][y] == -1: break
    # q = []
    # bound[x][y] = 1
    # # start down (0, 1) or right (1, 0)
    # q.append((x,y), 0, 1, 1)
    # q.append((x,y), 1, 0, 1)
    # maxn = 1
    # n = 1
    done = False
    while not done:
        # nx = x + dx
        # ny = y + dy
        #if not sidevalid(x,y,width,height): continue
        # print(len(q), maxn, flush=True)
        #bound[x][y] = n
        # maxn = max(n, maxn)
        for ndx, ndy in getdeltas(dx, dy):
            nx = x + ndx
            ny = y + ndy
            if not sidevalid(nx, ny, width, height): continue
            b = bound[nx][ny]
            if (dx, dy) == (ndx, ndy):
                if b == -1:
                    bound[x+ndx][y+ndy] = n
                    q.append(((x+ndx,y+ndy), ndx, ndy, n))
                # ignore other cases
            else:
                if b == -1:
                    bound[x+ndx][y+ndy] = n+1
                    q.append(((x+ndx,y+ndy), ndx, ndy, n+1))
                elif b > 0 and b <= n:
                    bound[x+ndx][y+ndy] = n+1
                    q.append(((x+ndx,y+ndy), ndx, ndy, n+1))
    print("Max Path is: ", maxn) 
    print(bound)
    return maxn


for l in open('test.txt'):
    process(l)

testSoln=[
    'A region of R plants with price 12 * 10 = 120.',
    'A region of V plants with price 13 * 10 = 130.',
    'A region of M plants with price 5 * 6 = 30.',
    'A region of I plants with price 14 * 16 = 224.',
    'A region of C plants with price 14 * 22 = 308.',
    'A region of I plants with price 4 * 4 = 16.',
    'A region of S plants with price 3 * 6 = 18.',
    'A region of J plants with price 11 * 12 = 132.',
    'A region of F plants with price 10 * 12 = 120.',
    'A region of C plants with price 1 * 4 = 4.',
    'A region of E plants with price 13 * 8 = 104.',
]
def mdist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

# p2 - p1
def mdiff(p1, p2):
    return (p2[0]-p1[0],p2[1]-p1[1])

def madd(p1, p2):
    return (p2[0]+p1[0],p2[1]+p1[1])

def getboundaries(s):
    bset = set()
    cur = (-1,-1)
    dx = dy = 0
    for p in s:
        if isboundary(grid, p[0], p[1]):
            if cur[0] == -1:
                cur = p
            else:
                bset.add(p)
                if mdist(cur, p):
                    d = mdiff(cur, p)
    #
    # with the boundary set, count how many turns 
    # made
    #
    turns = 4
    while bset:
        rb = None
        for b in bset:
            if mdist(b, cur) == 1:
                newd = mdiff(b, cur)
                if newd != d:
                    turns += 1
                    d = newd
                    rb = b
                    break
        if rb:
            bset.remove(rb)
        else:
            cur = b
            bset.remove(b)
    print("getboundaries: ", turns)
    

def match(grid, x1, y1, x2, y2):
    if valid(x1, y1) and valid(x2, y2):
        if grid[x1][y1] == grid[x2][y2]: return True
    return False

#
# returns perimeter, linear perimeter, and flag indicating it is contained by
# another gardern (which means its linear perimeter should be doubled when
# looking for fencing 
# linear perimeter counts the number of turns
#
## edge till always be on the 'right' side of traversal
## travel       delta     edge    delta
## dir  dx  dy  index    ex  ey   index
##  E   1   0     0      0    1     1
##  S   0   1     1     -1    0     2
##  W  -1   0     2      0   -1     3
##  N   0  -1     3      1    0     0
##
##  if x,y,dx,dy is valid (x,y) is a member of garden
##                        and x+ex, y+ey is NOT a member of garden
##                        if e+ex, y+ey is NOT a match with the current edge
##                        set internal to False (for good)
##     jump to x+dx, y+dy, add perim
##  else
##     jump back to x-dy y-dy, turn right, add linperime
def ptrack(grid, x, y):
    deltas = ((1,0),(0,1),(-1,0),(0,-1))
    visited={}
    garden = grid[x][y]
    start_index = -1
    skip = True
    print("*****  ptrack:  x,y: ", x, y, "  garden: ", grid[x][y])
    #
    # find proper starting direction and boundary garden
    #
    for i, (dx,dy) in enumerate(deltas):
        if (grid[x][y] != grid[x+dx][y+dy]): 
            boundary_garden = grid[x+dx][y+dy]
            start_index = i
    
    if start_index < 0: 
        print("ptrack error: ", x, y)
        return 0, 0, False
    # starting point:
    start  = (x,y,start_index)
    path = [(x, y, start_index, True, 1, 1)]
    # (x,y) the point to be visited
    # start_index (dx,dy) the direction of travel
    # True originally indicates the track is completely contained
    # path[3] is the total perimeter
    # path[4] is the linear perimeter
    while path:
        (x,y,di,contained,perim,linperim) = path.pop()
        print("   >>> ", x, y, di, contained, perim, linperim)
        if not skip and (x,y,di) == start: 
            return perim, linperim, contained
        skip = False
        # have we exited the garden?
        dx, dy = deltas[di]
        if not valid(x,y,di) or grid[x][y] != garden:
            path.append((x-dx,y-dy,(di+1)%4,contained,perim,linperim+1))
        else:
            if (x,y,di) in visited: continue
            visited.add((x,y,di))
        nx = x+dx
        ny = y+dy
        ex,ey = deltas[(di+1)%4]
        ex += nx
        ey += ny
        #
        # if next grid point is in our garden 
        # AND if the edge point is not in our garden 
        # - the full perimeter is incremented but
        # the linear perimeter is not
        # ELSE the edge point is in our garden which means
        # we'll turn and increment both total and linear perim
        if grid[nx][ny] == garden:
            if grid[ex][ey] != garden:
                path.append((nx, ny, di, 
                        (grid[ex][ey] == boundary_garden) and contained,
                        perim + 1, linperim))
            else:
                path.append((nx, ny, (di+1)%4, 
                        contained,
                        perim + 1, linperim + 1))
        #
        # if next grid point is not in our garden we move back and rotate
        # right the direction of the 'probe'  this would increate the linear
        # permiteter, but not affect the overall perimeter
        #
        else:
             path.append((x, y, (di+1)%4, 
                    contained,              # i don't think containment is changed
                    perim, linperim + 1))
        

        
s = set()
done = False
part1 = 0
part2 = 0
ij = 0
while not done:
    #
    # find any unsearched garden (first non-zero entry of selected)
    x, y = getcoord(selected)
    s.clear()
    if x >= 0 and y >= 0:
        # get all points (s) that make up selected garden
        perset(s, grid[x][y], x, y)

        # mark each point in garden as having been selected
        for a in s:
            sval = a
            selected[a] = 1
        #print(perim(s))
        #print(sval, len(s), sum(sum(selected)), flush = True) 
        per1 = perim(s)
        part1 += per1 * len(s)
        sds = linperim(s)
        part2 += sds * len(s)
        getboundaries(s)
        print(sval, chr(grid[sval]), " Area: ", len(s), "  Sides: ", sds, " = ", len(s) * sds,"    Perim: ", per1, flush=True)
        print(ij,"-->", testSoln[ij])
        ij += 1
        # p, lp, contained = ptrack(grid, x, y)
        # print("Perim: ", p, "  linear perim: ", lp, "   contained: ", contained)
    else:
        done = True


print("Part 1: total price of fencing is: ", part1)
print("Part 2: total price of fencing is: ", part2)
# part 2 782464 is too low
# part 2 938042 is too high
