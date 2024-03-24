'''
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle answer was 480.
--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle answer was 349975.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

def getxy(n, M):
    k = 1
    ksq = 1
    x = M
    y = M
    ring = 0
    ## find the corner (all of the form (2k + 1)^2
    while ksq < n:
        k += 2
        ksq = k * k
        x += 1
        y -= 1
        ring += 1

    diff = ksq - n
    q = diff // (k-1)
    r = diff % (k-1)
    if q == 0:
        x -= r
    elif q == 1:
        x -= (k - 1)
        y += r
    elif  q == 2:
        y += (k - 1)
        x -= (k - 1)
        x += r
    else:
        y += (k - 1)
        y -= r
    
    #print("\nk: ", k, "  ksq: ", ksq, "  diff: ", diff, "  x: ", x, "  y: ", y, "  q: ", q, "  r: ", r, "  ring: ", ring)
    #return abs(x) + abs(y)
    return x, y

#for N in range(10, 26):
#    print(N, getxy(N, 0))

#exit(1)

N = 347991
x1, y1 = getxy(N, 0)
p1Answer = abs(x1) + abs(y1)
print("Part 1: number of steps from ", N, " to center is: ", p1Answer)

import numpy as np

SIZE = 200
MSIZE = SIZE//2

grid = np.zeros([SIZE,SIZE], dtype = int)

def val(x, y):
    s = 0
    for dx, dy in [(-1, -1), (-1,0),  (-1, 1),
                    (0, -1),          ( 0, 1),
                    (1, -1), ( 1, 0), ( 1, 1)]:
        s += grid[x+dx][y+dy]
    return s

k = 1
ksq = 1
x = MSIZE
y = MSIZE
grid[x][y] = 1
n = 1 # nth number of cube
gridv = grid[x][y]

while gridv < N:
    n += 1
    x, y = getxy(n, MSIZE)
    gridv = grid[x][y] = val(x, y)

print("Part 2: first grid value that exceeds ", N, " is: ", gridv)
