#1312 @ 938,820: 27x15
import numpy as np

GSIZE = 1000
FILE = 'data.txt'
grid = np.zeros([GSIZE,GSIZE], dtype = int)


def process(line):
    w = line[1:].split()
    gid = int(w[0])
    xy = w[2].split(',')
    sx = int(xy[0])
    sy = int(xy[1][:len(xy[1])-1])
    dd = w[3].split('x')
    dx = int(dd[0])
    dy = int(dd[1])
    return gid, sx, dx, sy, dy

def fill(sx, dx, sy, dy):
    global grid
    for i in range(sx, sx+dx):
        for j in range(sy, sy+dy):
            grid[i][j] += 1
            
    #print(w, gid, sx, sy, dx, dy)

for line in open(FILE):
    gid, sx, dx, sy, dy = process(line)
    fill(sx, dx, sy, dy)

def count():
    global grid
    v = 0
    for i in range(GSIZE):
        for j in range(GSIZE):
            if grid[i][j] > 1: v += 1
    return v

print("Part 1: number of overlapping squares: ", count())

def allones(sx, dx, sy, dy):
    for i in range(sx, sx+dx):
        for j in range(sy, sy+dy):
            if grid[i][j] != 1: return False
    return True


for line in open(FILE):
    gid, sx, dx, sy, dy = process(line)
    if allones(sx, dx, sy, dy):
        print("Part 2: non-overlapping grid id is: ", gid)
        exit(1)
    


