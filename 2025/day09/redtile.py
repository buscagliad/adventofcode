
xys = []
N = 0
maxarea = 0
ULx = -1
ULy = -1

LRx = -1
LRy = -1

#
# xcross will return True, if the line (x1, y) -> (x2, y) 
# crosses any vertical line segment in the database
#
def vertcross(x1, x2, y):
    global xys, N
    print("vert", N, xys)
    for i in range(N):
        xa, ya = xys[i]
        xb, yb = xys[i+1]
        if ya == yb: continue # horizontal
        xr = max(x1, x2)
        xl = min(x1, x2)
        yu = min(ya, yb)
        yd = max(ya, yb)
        ## NOTE: xa == xb
        if (xl < xa < xr) and (yu < y < yd): return True
    return False

#
# ycross will return True, if the line (x, y1) -> (x, y2) 
# crosses any horizontal line segment in the database
#
def horzcross(y1, y2, x):
    global N, xys
    print("horz", N, xys)
    for i in range(N):
        xa, ya = xys[i]
        xb, yb = xys[i+1]
        if xa == xb: continue # vertical
        yu = min(y1, y2)
        yd = max(y1, y2)
        xr = max(xa, xb)
        xl = min(xa, xb)
        print("Testing ", y1, y2, x, xa, ya, xb, yb)
        ## NOTE: ya == yb -> horizontal
        if (xl < x < xr) and (yu < ya < yd):
            return True
    return False

def dotris():
    global xys, N, maxarea
    print("vert", N, xys)
    for i in range(N):
        x1, y1 = xys[i]
        x2, y2 = xys[i+1]
        x3, y3 = xys[i+2]
        print(x1, y1, x2, y2, x3, y3)
        if x1 == x3 and horzcross(y1, y3, x1) : continue
        elif y1 == y3 and vertcross(x1, x3, y1): continue
        area = (abs(x1-x3)+1) * (abs(y1 - y3) + 1)
        if (area > maxarea):
            maxarea = area
    return maxarea


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
        xys.append([x,y])
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

def maxrec(xy):
    m = 0
    for n, [x1,y1] in enumerate(xy):
        for [x2, y2] in xy[n:]:
            area = (abs(x2-x1)+1) * (abs(y2-y1)+1)
            if (area > m): m = area
    return m

init("test.txt")

print("Part 1: ", maxrec(xys), N)

print(dotris())
