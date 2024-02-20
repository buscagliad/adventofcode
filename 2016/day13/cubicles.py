from collections import deque
import numpy as np

FAV_NUM = 10
MAX_MAT = 100

grid = np.zeros((MAX_MAT,MAX_MAT), dtype = int)

def iswall(x, y):
    n = x*x + 3*x + 2*x*y + y + y*y + FAV_NUM
    s = bin(n)
    k = s.count('1')
    return k % 2 == 1

def buildGrid(fav_num):
    global grid
    global FAV_NUM
    FAV_NUM = fav_num
    for x in range(MAX_MAT):
        for y in range(MAX_MAT):
            if iswall(x, y):
                grid[x][y] = -1
            else:
                grid[x][y] = 0

def printGrid(X, Y):
    for y in range(Y):
        for x in range(X):
            if grid[x][y] == -1:
                print('#', end="")
            else:
                print('.', end="")
        print()

def mintravel(fnum, startx, starty, endx, endy):
    buildGrid(fnum)
    if grid[endx][endy] == -1:
        print("ERROR - end point is a wall")
        return 0
    minsteps = 1000000000
    state = deque()
    visited = {}
    state.append((startx, starty, 0))
    while state:
        x, y, steps = state.popleft()
        if x < 0: continue
        if y < 0: continue
        if grid[x][y] == -1: continue
        if (x,y) in visited: continue
        visited[(x,y)] = steps
        if steps > minsteps: continue
        if x == endx and y == endy:
            if steps < minsteps:
                minsteps = steps
            continue
        for d in [-1, 1]:
            state.append((x+d, y, steps+1))
            state.append((x, y+d, steps+1))
    atmost50 = 0
    for s in visited.items():
        a = s[1]
        if a <= 50:
            atmost50 += 1
    return minsteps, atmost50

minsteps, atmost50 = mintravel(1358,1,1,31,39)
print("Part 1: min travel is: ", minsteps)
print("Part 2: number of locations reached in at most 50 steps: ", atmost50)
#print("Part 1: min travel is: ", mintravel(10,1,1,7,4))
