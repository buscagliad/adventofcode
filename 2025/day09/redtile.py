
xys = []
N = 0
p1area = 0
p2area = 0
ULx = -1
ULy = -1

LRx = -1
LRy = -1

DEBUG = False

## point type:
## UL - upper left
## UR - upper right
## LL - lower left
## LR - lower right

UL=1
UR=2
LL=3
LR=4

def matchcorners(c1, c2):
    if c1 == c2: return False
    return True
    if c1 == UL and c2 == LR: return True
    if c1 == UR and c2 == LL: return True
    if c1 == LL and c2 == UR: return True
    if c1 == LR and c2 == UL: return True
    return False

def getcornertype(x1,y1,x2,y2,x3,y3):
    t = 0
    if x1 < x2 and y2 < y3: 
        t = 10 * t + UR
    if y1 > y2 and x2 > x3:
        t = 10 * t + UR
    if x1 < x2 and y2 > y3:
        t = 10 * t + LR
    if y1 < y2 and x2 > x3:
        t = 10 * t + LR
    if y1 < y2 and x2 < x3:
        t = 10 * t + LL
    if x1 > x2 and y2 > y3:
        t = 10 * t + LL
    if y1 > y2 and x2 < x3:
        t = 10 * t + UL
    if x1 > x2 and y2 < y3:
        t = 10 * t + UL
    return t
#
## contain will determine if there are non-red/green squares within the
## rectangle formed by (x1, y1) and (x3, y3)
## 
## the test is to see if there are two vertical or two horizontal 
## lines in the filed of (x1, y1) and (x3, y3) - which would have
## to include non-red or none-green squares
#
def contain(x1, y1, x3, y3):
    global N, xys
    xl = min(x1, x3)
    yu = min(y1, y3)
    xr = max(x1, x3)
    yd = max(y1, y3)
    
    icounts = 0
    
    for i in range(N):
        xa, ya, ma = xys[i]
        xb, yb, mb = xys[i+1]
        #
        # xa == xb - vertical segment - y's
        if xa == xb:
            if xl < xa < xr:
                miny = min(ya, yb)
                maxy = max(ya, yb)
                if yu <= miny <= yd  or  yu <= maxy <= yd:
                    icounts += 1
                    if (DEBUG): print("Vertical intersection: ", miny, maxy)
                    #return True
                if yu <= miny and yd >= maxy: 
                    icounts += 1
                    if (DEBUG): print("Vertical intersection: ", miny, maxy)
                    #return True
        #
        # ya == yb - horizontal segment - x's
        else:
            if yu < ya < yd:
                minx = min(xa, xb)
                maxx = max(xa, xb)
                if xl <= minx <= xr  or  xl <= maxx <= xr: 
                    if (DEBUG): print("Horizontal intersection: ", minx, maxx)
                    icounts += 1
                    #return True
                if xl <= minx and xr >= maxx: 
                    icounts += 1
                    #return True
        if icounts : return True
    return False

def comparea(x1, y1, x3, y3) :
    global p1area
    if contain(x1, y1, x3, y3) : return
    area = (abs(x1 - x3) + 1) * (abs(y1 - y3) + 1)
    if (area > p1area):
        if (DEBUG): print("AREA", x1, y1, x3, y3, area)
        p1area = area            
    
def dotris():
    global xys, N, p1area
    #print("vert", N, xys)
    p1area = 0
    for i in range(N):
        x1, y1, m1 = xys[i]
        for j in range(N):
            x3, y3, m3 = xys[j]
            if not matchcorners(m1, m3): continue
            if i == j: continue
            #if not (x1 == x3 or y1 == y3): continue
                
            comparea(x1, y1, x3, y3)
        
    return p1area


def init(fname):
    global xys, N
    global ULx, ULy
    global LRx, LRy
    first = True
    for l in open(fname, 'r'):
        if len(l) < 3: break
        m = l.strip().split(',')
        x = int(m[0])
        y = int(m[1])
        xys.append([x,y,0])
        if first:
            ULx = x
            ULy = y
            LRx = x
            LRy = y

            first = False
        else:
            ULx = min(x, ULx)
            ULy = min(y, ULy)
            LRx = max(x, LRx)
            LRy = max(y, LRy)
    N = len(xys)
    xys.append(xys[0])
    xys.append(xys[1])
    for i in range(N):
        j = (i - 1 + N) % N
        x1, y1, m = xys[j]
        x2, y2, m = xys[i]
        x3, y3, m = xys[i+1]
        xys[i][2] = getcornertype(x1,y1,x2,y2,x3,y3)
    xys[N] = xys[0]
    xys[N+1] = xys[1]

#
# if the corners x1, y1 and x2, y2 contain only red and green squares
# the truth of this assertion and the area is reutend
#
def allredgreen(x1,y1,c1,x2,y2,c2):
    #if c1 == c2: return False
    return not contain(x1, y1, x2, y2)
    

def maxrec(xy):
    global xys
    m1 = 0
    m2 = 0
    for n, [x1, y1, c1] in enumerate(xys):
        for [x2, y2, c2] in xy[n:]:
            area = (abs(x2-x1)+1) * (abs(y2-y1)+1)
            # print(x1, y1, x2, y2, area, m1)
            if (area > m1): m1 = area
            if allredgreen(x1,y1,c1, x2,y2,c2):
                if (area > m2): 
                    m2 = area
                    print(x1, y1, c1, x2, y2, c2, area, m2)
    return m1, m2

init("test.txt")

print(xys)
exit(1)

print("Part 1: ", maxrec(xys))
# Part 1:  4755278336 - correct

#print("Part 2: ", dotris())
# Part 2:  164017360 - too low
# Part 2:  4566760900 - too high
#print(xys)
