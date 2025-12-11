
xys = []
ULx = -1
ULy = -1

LRx = -1
LRy = -1


def init(fname):
    global xys
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

def maxrec(xy):
    m = 0
    for n, [x1,y1] in enumerate(xy):
        for [x2, y2] in xy[n:]:
            area = (abs(x2-x1)+1) * (abs(y2-y1)+1)
            if (area > m): m = area
    return m

init("data.txt")

print("Part 1: ", maxrec(xys))

print(ULx, ULy, LRx, LRy)
