'''

--- Day 17: Reservoir Research ---

You arrive in the year 18. If it weren't for the coat you got in 1018, you would be very cold: the North Pole base hasn't even been constructed.

Rather, it hasn't been constructed yet. The Elves are making a little progress, but there's not a lot of liquid water in this climate, so they're getting very dehydrated. Maybe there's more underground?

You scan a two-dimensional vertical slice of the ground nearby and discover that it is mostly sand with veins of clay. The scan only provides data with a granularity of square meters, but it should be good enough to determine how much water is trapped there. In the scan, x represents the distance to the right, and y represents the distance down. There is also a spring of water near the surface at x=500, y=0. The scan identifies which square meters are clay (your puzzle input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504

Rendering clay as #, sand as ., and the water spring as +, and with x increasing to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...

The spring of water will produce water forever. Water can move through sand, but is blocked by clay. Water always moves down when possible, and spreads to the left and right otherwise, filling space that has clay on both sides and falling out otherwise.

For example, if five squares of water are created, they will flow downward until they reach the clay and settle there. Water that has come to rest is shown here as ~, while sand through which water has passed (but which is now dry again) is shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Two squares of water can't occupy the same location. If another five squares of water are created, they will settle on the first five, filling the clay reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Water pressure does not apply in this scenario. If another four squares of water are created, they will stay on the right side of the barrier, and no water will reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

At this point, the top reservoir overflows. While water can reach the tiles above the surface of the water, it cannot settle there, and so the next five squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...

Note especially the leftmost |: the new squares of water can reach this tile, but cannot stop there. Instead, eventually, they all fall to the right and settle in the reservoir below.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...

Finally, while there is nowhere left for the water to settle, it can reach a few more tiles before overflowing beyond the bottom of the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)

How many tiles can be reached by the water? To prevent counting forever, ignore tiles with a y coordinate smaller than the smallest y coordinate in your scan data or larger than the largest one. Any x coordinate is valid. In this example, the lowest y coordinate given is 1, and the highest is 13, causing the water spring (in row 0) and the water falling off the bottom of the render (in rows 14 through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other sand tiles the water can hypothetically reach (|), the total number of tiles the water can reach is 57.

How many tiles can the water reach within the range of y values in your scan?


'''

import numpy as np

VERTICAL = 1
HORIZONTAL = 2
DEBUG = False

walls = []

WALL = -1
SAND = 0
PATH = 1    # water travelled through this spot
WATER = 2


def getnum(s):
    rv = 0
    foundDigit = False
    for d in s:
        if d.isdigit():
            foundDigit = True
            rv = 10 * rv + int(d)
        else:
            if foundDigit:
                break
    return rv

#x=553, y=525..527
#y=30, x=554..581

minx = 100000
maxx = 0
miny = 100000
maxy = 0

bigsum = 0
class Wall():
    def __init__(self, s):
        global minx, maxx, miny, maxy, bigsum
        w = s.strip().split()
        self.kind = HORIZONTAL
        n = getnum(s)
        r1 = getnum(s[s.find(','):])
        r2 = getnum(s[s.find("."):])
        bigsum += (r2 - r1 + 1)
        if w[0][0] == 'x':
            self.kind = VERTICAL
            self.xlow = n
            self.xhigh = n
            self.ylow = r1
            self.yhigh = r2
        else:
            self.ylow = n
            self.yhigh = n
            self.xlow = r1
            self.xhigh = r2

        if self.xlow < minx: minx = self.xlow
        if self.xhigh > maxx: maxx = self.xhigh

        if self.ylow < miny: miny = self.ylow
        if self.yhigh > maxy: maxy = self.yhigh

    def out2(self):
        print("x:: [", self.xlow, "..", self.xhigh, "]   ",
              "y:: [", self.ylow, "..", self.yhigh, "]")
    
#x=553, y=525..527
#y=30, x=554..581
    def out(self):
        if self.kind == VERTICAL:
            print("x=", self.xlow, ", y=", self.ylow, "..", self.yhigh, sep="")
        else:
            print("y=", self.ylow, ", x=", self.xlow, "..", self.xhigh, sep="")
    
    def fill(self, arr):
        ints = 0
        for x in range(self.xlow, self.xhigh+1):
            for y in range(self.ylow, self.yhigh+1):
                if arr[x][y] == WALL:
                    ints += 1
                arr[x][y] = WALL
        return ints

def process(line):
    global walls
    walls.append(Wall(line))

def down(arr, x, y):
    if 1 or DEBUG: print("Down at ", x, y)
    while y < maxy and arr[x][y+1] == SAND:
        y += 1
        arr[x][y] = WATER
        print("DOWN: water at ", x, y)
    if y >= maxy:
        if DEBUG: print("  BOTTOM", y)
        return maxy
    if DEBUG: print("   returning  ", y)
    return y

#
# left will fill in arr with water from x-1, y ... E, y
# where E is just to the right of a WALL or
#       arr[x][y+1] is SAND
# if a WALL is hit, -1 is returned, if SAND at arr[E][y+1],
#    E is returned  
#
def left(arr, x, y):
    if 1 or DEBUG: print("Call LEFT with: ", x, y)
    lx = x
    if arr[lx][y] == WALL: return True, 0
    if DEBUG: print("LEFT at ", lx, y)
    done = False
    while not done:
        if arr[lx][y] == WALL:
            return True, 0
        elif arr[lx][y] == SAND:
            arr[lx][y] = WATER
            print("LEFT: water at ", lx, y)
            if arr[lx][y+1] == SAND:
                print("LEFT - SAND")
                return False, lx
        lx -= 1


#
# right - returns False, x   if a 'drop' is encounter at the position x
#         returns True, _  if a 'Wall' is encountered
#
def right(arr, x, y):
    if 1 or DEBUG: print("Call RIGHT with: ", x, y)
    rx = x
    if arr[rx][y] == WALL: return True, 0
    if DEBUG: print("Right at ", rx, y)
    done = False
    while not done:
        if arr[rx][y] == WALL:
            return True, 0
        elif arr[rx][y] == SAND:
            arr[rx][y] = WATER
            print("RIGHT: water at ", rx, y)
            if arr[rx][y+1] == SAND:
                return False, rx
        rx += 1

def fillem(arr, x, y):
    if (y >= maxy): 
        if 1 or DEBUG: print("fillem - HIT BOTTOM")
        return False
    dy = down(arr, x, y)
    if 1 or DEBUG: print("fillem:  down at ", x, y, "  stop at ", dy)
    if dy < 0 or (dy >= maxy): return
    if dy > 0 and dy <= maxy:
        #while dy > y and dy < maxy:
        r = True
        l = True
        while l and r and dy > y :
            l, lx = left(arr, x-1, dy)
            r, rx = right(arr, x+1, dy)
            dy -= 1
        if 1 or DEBUG: print("fillem: r/rx: ", r, rx, "  l/lx: ", l, lx)
        if not r:
            print("Dropping at ", rx, dy+1, y)
        if not l:
            print("Dropping at ", lx, dy+1, y)
        if not r: # and dy < y: 
            fillem(arr, rx, dy+1)
        if not l: # and dy < y :
            fillem(arr, lx, dy+1)
    return True
  
def countwater(arr):
    cnt = 0
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if arr[x][y] == WATER: cnt += 1
    return cnt
  
def printarr(arr, lx, rx, uy, ly):
    for y in range(uy, ly+1):
        print("%4d " % y, end = "")
        for x in range(lx, rx+1):
            d = arr[x][y]
            if x == 500 and y == 0: print("+ ", end="")
            elif d == WALL: print("# ", end="")
            elif d == SAND: print(". ", end="")
            elif d == WATER: print("~ ", end="")
            else: print("$ ", end="")
        print()
    print()

for line in open('test2.txt'):
    process(line)

maxx += 1
minx -= 1

arr = np.zeros([maxx+30, maxy+20], dtype = int)
#print("ARR 0 panels: ", sum(sum(arr)))
if DEBUG: print(minx, maxx, miny, maxy)

ss = 0
gs = 0
for w in walls:
    #w.out()
    ss += (w.xhigh - w.xlow + 1) * (w.yhigh - w.ylow + 1)
    gs += w.fill(arr)

if 1 or DEBUG: printarr(arr, minx, maxx, 0, maxy)


fillem(arr, 500, 0)
#print("ARR panels: ", sum(sum(arr)))
#printarr(arr, minx-1, maxx+1, 0, maxy)

print("Part 1: number of cells that passed water is ", countwater(arr))

if 1 or DEBUG: printarr(arr, minx, maxx, 0, maxy)
