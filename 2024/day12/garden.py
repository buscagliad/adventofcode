'''

--- Day 12: Garden Groups ---

Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC

This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+

Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:

OOOOO
OXOXO
OOOOO
OXOXO
OOOOO

The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.

The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.

Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.

In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).

Here's a larger example:

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

It contains:

    A region of R plants with price 12 * 18 = 216.
    A region of I plants with price 4 * 8 = 32.
    A region of C plants with price 14 * 28 = 392.
    A region of F plants with price 10 * 18 = 180.
    A region of V plants with price 13 * 20 = 260.
    A region of J plants with price 11 * 20 = 220.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 18 = 234.
    A region of I plants with price 14 * 22 = 308.
    A region of M plants with price 5 * 12 = 60.
    A region of S plants with price 3 * 8 = 24.

So, it has a total price of 1930.

What is the total price of fencing all regions on your map?

Your puzzle answer was 1477762.
--- Part Two ---

Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC

The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of 436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA

It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)

The larger example from before now has the following updated prices:

    A region of R plants with price 12 * 10 = 120.
    A region of I plants with price 4 * 4 = 16.
    A region of C plants with price 14 * 22 = 308.
    A region of F plants with price 10 * 12 = 120.
    A region of V plants with price 13 * 10 = 130.
    A region of J plants with price 11 * 12 = 132.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 8 = 104.
    A region of I plants with price 14 * 16 = 224.
    A region of M plants with price 5 * 6 = 30.
    A region of S plants with price 3 * 6 = 18.

Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?

Your puzzle answer was 923480.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import numpy as np
import heapq
from collections import deque


grid = np.zeros([150,150], dtype = int)
selected = np.zeros([150,150], dtype = int)
used = np.zeros([150,150], dtype = int)

ymax = 0
xmax = 0

DEBUG = False


def process(line):
    global grid, xmax, ymax

    xmax = max(xmax, len(line.strip()))
    for i, a in enumerate(line.strip()):
        h = ord(a)
        grid[i][ymax] = h
    ymax += 1

NORTH=0
EAST=1
SOUTH=2
WEST=3
DIR=["NORTH","EAST","SOUTH","WEST"]
DELTAS = [(0,-1),(1,0),(0,1),(-1,0)]

deltax = [0,1,0,-1]
deltay = [-1,0,1,0]


def valid(v, x, y):
    if x < 0 or y < 0: return False
    if x >= xmax or y >= ymax: return False
    if grid[x][y] == v: return True
    return False

#
# perim can only be called with the first 
# grid point seen in getparams
#
   
def corner(s):
    xx = yx = 0 
    xn = yn = 1000
    for x,y in s:
        xx = max(x, xx)
        yx = max(y, yx)
        xn = min(x, xn)
        yn = min(y, yn)
    return xn,yn,xx,yx

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
    return corner(s)

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

   
    
def pset(s):
    xx = yx = 0 
    xn = yn = 1000
    for x,y in s:
        xx = max(x, xx)
        yx = max(y, yx)
        xn = min(x, xn)
        yn = min(y, yn)
    for y in range(yn, yx+1):
        for x in range(xn, xx+1):
            if (x,y) in s:
                print(chr(grid[x][y]), end="")
            else:
                print(" ", end="")
        print()
    return xn, xx, yn, yx



for l in open('data.txt'):
    process(l)


          
def getedges(x,y,s):
    rv = []
    for di, (dx, dy) in enumerate(DELTAS):
        nx = x + dx
        ny = y + dy
        if not (nx,ny) in s:
            if DEBUG: print (x,y," Edge found at: ", nx,ny)
            rv.append(di)
    return rv
            

def getfences(s):
    rv = {}
    for g in s:
        edges = getedges(g[0],g[1],s)
        rv[g] = edges
    return rv

def pfences(rv):
    for xy, fs in rv.items():
        print(xy, " fence directions: ", fs)
        
def trimfences(fences):
    for (x,y), fencesides in fences.items():
        if DEBUG: print("At ", x, y, " with sides: ", fencesides)
        #x,y = f[0]
        for sides in fencesides:
            locald=[]
            if sides in [NORTH, SOUTH]:
                locald = [(-1,0),(1,0)]
            else:
                locald = [(0,-1),(0,1)]
            nx = x
            ny = y
            for (dx,dy) in locald:
                done = False
                while not done:
                    nx += dx
                    ny += dy
                    if (nx,ny) in fences:
                        if (nx,ny) == (x,y): continue
                        if DEBUG: print("    Wanting to remove fence: ", sides, " from ", nx,ny)
                        if sides in fences[(nx,ny)]:
                            if DEBUG: print("    ------- removing fence: ", sides, " from ", nx,ny)
                            fences[(nx,ny)].remove(sides)
                        else:
                            done = True
                    else:
                        done = True
    num = 0
    for xy, fs in fences.items():
        if DEBUG: print(xy, " fence directions: ", fs)
        num += len(fs)

    return num
        
s = set()
done = False
part1 = 0
part2 = 0
ij = 0
while not done:
    #
    # find any unsearched garden (first non-zero entry of selected)
    x, y = getcoord(selected)
    if DEBUG: print("Current selected coordinate: ", x, y, " :: ", chr(grid[x][y]))
    s.clear()
    if x >= 0 and y >= 0:
        # get all points (s) that make up selected garden
        ulx, uly, lrx, lry = perset(s, grid[x][y], x, y)

        # mark each point in garden as having been selected
        for a in s:
            sval = a
            selected[a] = 1
        if DEBUG: pset(s)
        per1 = perim(s)
        part1 += per1 * len(s)
        fences = getfences(s)
        linperim = trimfences(fences)
        part2 += linperim * len(s)
    else:
        done = True


print("Part 1: total price of fencing is: ", part1)
print("Part 2: total price of fencing is: ", part2)
# part 2 782464 is too low
# part 2 938042 is too high
