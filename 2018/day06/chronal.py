'''

--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

Your puzzle answer was 3890.
--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?

Your puzzle answer was 40284.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import numpy as np

pairs = []

def process(line):
    w = line.split()
    x = int(w[0][:-1])
    y = int(w[1])
    return x,y


grid = np.zeros([1000, 1000], dtype = int)
xmax = -100
ymax = -100
xmin = 1000
ymin = 1000

for line in open('data.txt'):
    x, y = process(line)
    pairs.append((x,y))
    xmax = max(x, xmax)
    ymax = max(y, ymax)
    xmin = min(x, xmin)
    ymin = min(y, ymin)

for i, p in enumerate(pairs):
    minv = 100000
    minp = (-1,-1)
    if i == len(pairs)-1: break
    for j, p2 in enumerate(pairs):
        if j <= i: continue
        d = abs(p[0]-p2[0])+abs(p[1]-p2[1])
        if d < minv:
            minp = p2
            minv = d
    #print(p, minp, minv)

def closest(x, y):
    ri = 0
    rd = 100000000
    match = False
    for i, p in enumerate(pairs):
        d = abs(p[0]-x)+abs(p[1]-y)
        if d < rd:
            match = False
            ri = i
            rd = d
        elif d == rd:
            match = True
    if match: return -1
    return ri
        
def sumdist(x, y):
    sumd = 0
    for i, p in enumerate(pairs):
        d = abs(p[0]-x)+abs(p[1]-y)
        sumd += d
    return sumd
        
        
InfiniteEdge = set()

for x in range(xmin, xmax+1):
    for y in range(ymin, ymax+1):
        g = closest(x, y)
        grid[x][y] = g
        if x == xmax or x == xmin or y == ymin or y == ymax:
            InfiniteEdge.add(g)

PAIR = chr(178)

            
def printgrid():
    for y in range(1000):
        for x in range(1000):
            n = closest(x,y)
            if n < 0:
                print('.', end = "")
            elif (x,y) in pairs:
                print(PAIR, end = "")
            else:
                ch = chr(ord('a') + n) if n < 26 else chr(ord('A') + n - 26)
                print(ch, end = "")
            print(",", end = "")
        print()

def Edge(n):
    return n in InfiniteEdge

def largeArea():
    count = [0] * len(pairs)
    for y in range(ymin+1, ymax):
        for x in range(xmin+1, xmax):
            n = grid[x][y]
            if n >= 0 and not Edge(n):
                count[n] += 1
    mc = max(count)
    mi = count.index(mc)
    #print("area: ", mc, "  index: ", mi, "  Pair: ", pairs[mi])
    return mc

#print("x range: ", xmin, xmax, "  y range: ", ymin, ymax)
#for n, p in enumerate(pairs):
#    if (Edge(n)):
#        print(p, n)
##
## 4146 is too high
## 4116 is too high
##
print("Part 1: Largest area not infinity: ", largeArea())

MAXN = 10000

c = 0
for x in range(1000):
    for y in range(1000):
        if (sumdist(x,y) < MAXN): c += 1
print("Part 2: total number of positions < 10000 from all points is: ", c)
#printgrid()
