'''

--- Day 11: Chronal Charge ---

You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.

Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're not sure what negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1.

The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:

    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.

For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:

    The rack ID is 3 + 10 = 13.
    The power level starts at 13 * 5 = 65.
    Adding the serial number produces 65 + 8 = 73.
    Multiplying by the rack ID produces 73 * 13 = 949.
    The hundreds digit of 949 is 9.
    Subtracting 5 produces 9 - 5 = 4.

So, the power level of this fuel cell is 4.

Here are some more example power levels:

    Fuel cell at  122,79, grid serial number 57: power level -5.
    Fuel cell at 217,196, grid serial number 39: power level  0.
    Fuel cell at 101,153, grid serial number 71: power level  4.

Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2

For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1

What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?

Your puzzle input is 1133.

Your puzzle answer was 235,14.
--- Part Two ---

You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

    For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
    For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?

Your puzzle answer was 237,227,14.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

GSIZE = 301
DEBUG = False

# The power level in a given fuel cell can be found through the following process:

# Find the fuel cell's rack ID, which is its X coordinate plus 10.
# Begin with a power level of the rack ID times the Y coordinate.
# Increase the power level by the value of the grid serial number (your puzzle input).
# Set the power level to itself multiplied by the rack ID.
# Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
# Subtract 5 from the power level.

import numpy as np

def plevel(x, y, serialNumber):
    if x == 0 or y == 0: return -100
    rackid = x + 10
    pl = rackid * y
    pl += serialNumber
    pl = pl * rackid
    pl = ( pl // 100 ) % 10
    pl -= 5
    return pl

def test():
    for x, y, s, ans in [(122,79, 57, -5), 
        (217,196, 39, 0),
        (101,153, 71, 4) ]:
        print(x, y, s, plevel(x,y,s), ans)
        
def buildgrid(sn):
    g = np.zeros([GSIZE,GSIZE], dtype = int)

    for x in range(GSIZE):
        for y in range(GSIZE):
            g[x][y] = plevel(x, y, sn)
    return g

def maxgrid(g, n):
    maxp = 0
    maxx = 0
    maxy = 0
  
    p = 0
    for x in range(1, GSIZE - n):
        for y in range(1, GSIZE - n):
            p = 0
            for i in range(x, x+n):
                for j in range(y, y+n):
                    p += g[i][j]
            if p > maxp:
                maxp = p
                maxx = x
                maxy = y
    return maxx, maxy, maxp

#
# p already contains the power for each corner square for the n-1 x n-1 case
#
def nextblock(p, g, n):
    for x in range(1, GSIZE - n):
        for y in range(1, GSIZE - n):
            #p[x][y] += sum(g[x+n][y:y+n]) + sum(g[x:x+n+1][y+n])
            s = 0
            if DEBUG: print("Corner: ", x, y, " == ", p[x][y], "  n = ", n)
            for i in range(x, x+n-1):
                s += g[i][y+n-1]
                if DEBUG: print("    adding ", g[i][y+n-1], " at ", i, y+n-1)
            for j in range(y, y+n):
                s+= g[x+n-1][j]
                if DEBUG: print("    adding ",  g[x+n-1][j], " at ",  x+n-1, j)
            p[x][y] += s
    return p
    
        
def mpower(g):
    maxx, maxy, maxp = maxgrid(g, 3)
    return maxx, maxy, maxp

def test(cx, cy, tp, sn):
    x, y, p = mpower(sn)
    print("Upper left corner: ", x, y, "  Total power: ", p)
    print("  Solution corner: ", cx, cy, "  Total power: ", tp)



def printgrid(g, x, y, n):
    for j in range(y, y+n):
        for i in range(x, x+n):
            print(g[i][j], end = "  ")
        print()
        


def maxentry(g, pb, n):
    maxp = 0
    maxx = 0
    maxy = 0
    p = 0
    for x in range(GSIZE - n):
        for y in range(GSIZE - n):
            p = pb[x][y]
            if p > maxp:
                maxp = p
                maxx = x
                maxy = y
                if DEBUG: print("maxentry::  NxN: ", n, "  Power; ", maxp, "  Solution: ", 
                    maxx, ",", maxy, flush=True)
                if DEBUG: printgrid(g, maxx, maxy, n)
    return maxx, maxy, maxp
    

import copy

#
# Part 2 - we will search for an nxn power grid with the largest power
#

for a in [18, 42, 1133]:
    maxp = 0
    maxx = 0
    maxy = 0
    maxn = 0        #g2 = buildgrid(18)
    g = buildgrid(a)
    pb = copy.deepcopy(g)
    print("Serial Number: ", a)
    for n in range(2, GSIZE):
        pb = nextblock(pb, g, n)
        x, y, p = maxentry(g, pb, n)
        if DEBUG: print("Part 2:  NxN: ", n, "  Power; ", p, "  Solution: ", x, ",", y, ",", n, flush=True)
        if n == 3:
            print("Part 1: Upper left corner: ", x, y, "  Total power: ", p)
        if p > maxp:
            maxp = p
            maxx = x
            maxy = y
            maxn = n
            if DEBUG: 
                print("--> Part 2:  NxN: ", maxn, "  Power; ", maxp, "  Solution: ", maxx, ",", maxy, ",", maxn, flush=True)
                printgrid(g, maxx, maxy, maxn)
        if p < 1:
             print("Part 2:  NxN: ", maxn, "  Power; ", maxp, "  Solution: ", maxx, ",", maxy, ",", maxn, flush=True)
             break

