
xys = []

def init(fname):
    global xys
    for l in open(fname, 'r'):
        if len(l) < 3: break
        m = l.strip().split(',')
        xys.append([int(m[0]),int(m[1])])

def maxrec(xy):
    m = 0
    for n, [x1,y1] in enumerate(xy):
        for [x2, y2] in xy[n:]:
            area = (abs(x2-x1)+1) * (abs(y2-y1)+1)
            if (area > m): m = area
    return m

init("data.txt")

print("Part 1: ", maxrec(xys))
