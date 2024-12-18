
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

#
# compute the number of linear sides of
# the set s
#
def sides2(s):
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
    print("Rectangles: ", n, cn, rv)
    for y in range(height):
        for x in range(width):
            print(f"{bound[x][y]:4}", end="")
        print()
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
        sds = sides2(s)
        part2 += sds * len(s)
        print(sval, chr(grid[sval]), " Area: ", len(s), "  Sides: ", sds, " = ", len(s) * sds,"    Perim: ", per1, flush=True)
        print(ij,"-->", testSoln[ij])
        ij += 1
    else:
        done = True

def match(grid, x1, y1, x2, y2):
    if valid(x1, y1) and valid(x2, y2):
        if grid[x1][y1] == grid[x2][y2]: return True
    return False

def isboundary(grid, x, y):
    if match(grid, x, y, x-1, y): return -1, 0
    return 0,0
#
# returns perimeter, linear perimeter, and flag indicating it is contained by
# another gardern (which means its linear perimeter should be doubled when
# looking for fencing 
#
def ptrack(grid, x, y):
    visited={}
    garden = grid[x][y]
    path = queue((x,y,0,0,True,))
    while path:
        (x,y,p,lp,ext) = path.pop()
        if (x,y) in visited: continue
        visited.add((x,y))
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            a = x + dx
            b = y + dy
            #if isboundary(grid, a, b, garden
        
    

print("Part 1: total price of fencing is: ", part1)
print("Part 2: total price of fencing is: ", part2)
# part 2 782464 is too low
# part 2 938042 is too high
