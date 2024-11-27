'''

--- Day 23: Experimental Emergency Teleportation ---

Using your torch to search the darkness of the rocky cavern, you finally locate the man's friend: a small reindeer.

You're not sure how it got so far in this cave. It looks sick - too sick to walk - and too heavy for you to carry all the way back. Sleighs won't be invented for another 1500 years, of course.

The only option is experimental emergency teleportation.

You hit the "experimental emergency teleportation" button on the device and push I accept the risk on no fewer than 18 different warning messages. Immediately, the device deploys hundreds of tiny nanobots which fly around the cavern, apparently assembling themselves into a very specific formation. The device lists the X,Y,Z position (pos) for each nanobot as well as its signal radius (r) on its tiny screen (your puzzle input).

Each nanobot can transmit signals to any integer coordinate which is a distance away from it less than or equal to its signal radius (as measured by Manhattan distance). Coordinates a distance away of less than or equal to a nanobot's signal radius are said to be in range of that nanobot.

Before you start the teleportation process, you should determine which nanobot is the strongest (that is, which has the largest signal radius) and then, for that nanobot, the total number of nanobots that are in range of it, including itself.

For example, given the following nanobots:

pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1

The strongest nanobot is the first one (position 0,0,0) because its signal radius, 4 is the largest. Using that nanobot's location and signal radius, the following nanobots are in or out of range:

    The nanobot at 0,0,0 is distance 0 away, and so it is in range.
    The nanobot at 1,0,0 is distance 1 away, and so it is in range.
    The nanobot at 4,0,0 is distance 4 away, and so it is in range.
    The nanobot at 0,2,0 is distance 2 away, and so it is in range.
    The nanobot at 0,5,0 is distance 5 away, and so it is not in range.
    The nanobot at 0,0,3 is distance 3 away, and so it is in range.
    The nanobot at 1,1,1 is distance 3 away, and so it is in range.
    The nanobot at 1,1,2 is distance 4 away, and so it is in range.
    The nanobot at 1,3,1 is distance 5 away, and so it is not in range.

In this example, in total, 7 nanobots are in range of the nanobot with the largest signal radius.

Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?

Your puzzle answer was 691.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Now, you just need to figure out where to position yourself so that you're actually teleported when the nanobots activate.

To increase the probability of success, you need to find the coordinate which puts you in range of the largest number of nanobots. If there are multiple, choose one closest to your position (0,0,0, measured by manhattan distance).

For example, given the following nanobot formation:

pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
Many coordinates are in range of some of the nanobots in this formation. However, only the coordinate 12,12,12 is in range of the most nanobots: it is in range of the first five, but is not in range of the nanobot at 10,10,10. (All other coordinates are in range of fewer than five nanobots.) This coordinate's distance from 0,0,0 is 36.

Find the coordinates that are in range of the largest number of nanobots. What is the shortest manhattan distance between any of those points and 0,0,0?

Answer: 
         *-----------------*
        /|                /|
       / |               / |
      *-----------------*  |
      |  |              |  |
      |  *--------------|--*
      | /               | /
      |/                |/
      *-----------------*
'''

import numpy as np
from queue import PriorityQueue

grid = np.zeros((1000,1000), dtype=int)

class cube:
    def __init__(self, x, dx, y, dy, z, dz):
        self.corners = []
        self.delta = [dx, dy, dz]
        self.debug = False
        self.maxn = 0
        self.maxc = [x,y,z]
        for i in [0, dx]:
            for j in [0, dy]:
                for k in [0, dz]:
                    c = [x+i,y+j,z+k]
                    n = compr(c[0], c[1], c[2])
                    self.corners.append([c,n])
                    if n > self.maxn:
                        self.maxn = n
                        self.maxc = c                    

        if self.debug: 
            print("**************************************************")
            for c, n in self.corners:
                print(c, n)

    def __lt__(self, other):
        return self.maxn < other.maxn


    def split(self):
        if self.debug: print("^^^^^^^^^^^^^^^^ SPLIT ^^^^^^^^^^^^^^^^^^^^^^")
        sp = []
        deltax = self.delta[0] // 4
        deltay = self.delta[1] // 4
        deltaz = self.delta[2] // 4
        x = self.maxc[0]
        for dx in [-deltax, 0, deltax]:
            y = self.maxc[1]
            for dy in [-deltay, 0, deltay]:
                z = self.maxc[2]
                for dz in [-deltaz, 0, deltaz]:
                    sp.append(cube(x, dx, y, dy, z, dz))
                    z += 2 * deltaz
                y += 2 * deltay
            x += 2 * deltax
        return sorted(sp, key=lambda sp: sp.maxn, reverse=True)
    def out(self):
        print("N: ", self.maxn, "  (x,y,z): ",self.maxc, "  Dist: ", 
            abs(self.maxc[0])+abs(self.maxc[1])+abs(self.maxc[2]))

class nano:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.count = 0
        self.orbit = []
    def dist(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y) + abs(self.z-other.z)
    def check(self, other):
        d = self.dist(other)
        if self.r >= d:
            self.count += 1
            self.orbit.append(other)
    def contains(self, other):
        return self.dist(other) <= self.r
    def cansee(self, x, y, z):
        d = abs(self.x-x) + abs(self.y-y) + abs(self.z-z)
        if d <= self.r: return True
        return False
    def out(self, t=""):
        print(t, self.x, self.y, self.z, self.r, self.count)

bots = []

def init(fname):
    global bots
    for l in open(fname, "r"):
        l = l.replace(">, r=", " ");
        l = l.replace("pos=<","")
        l = l.replace(","," ")
        a = l.strip().split()
        n = nano(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        bots.append(n)

def compr(x, y, z, debug = False):
    n = 0
    for b in bots:
        if b.cansee(x, y, z): n += 1
    if debug: print("at (", x, y, z, ") there are ", n, " bots, dist = ", abs(x)+abs(y)+abs(z));
    return n




init("data.txt")

maxs = 0
cont = np.zeros(1000, dtype=int)
large = bots[0]
small = bots[0]
[xlow,xhigh] = [100000000000, -100000000000]
[ylow,yhigh] = [100000000000, -100000000000]
[zlow,zhigh] = [100000000000, -100000000000]

for ai, a in enumerate(bots):
    cont[ai] = compr(a.x, a.y, a.z)
    if a.r > large.r: 
        large = a
    if a.r < small.r: 
        small = a
    if xlow > a.x: xlow = a.x
    if ylow > a.y: ylow = a.y
    if zlow > a.z: zlow = a.z
    if xhigh < a.x: xhigh = a.x
    if yhigh < a.y: yhigh = a.y
    if zhigh < a.z: zhigh = a.z


n = 0
for b in bots:
    if large.contains(b): n += 1
print("Part 1: Number of nanobots in range of bot with strongest signal: ", n)


cubeq = PriorityQueue()

# testcube = cube(0, 1000, 0, 1000, 0, 1000)
# s = testcube.split()
# for a in s:
    # a.out()
# exit(1)
nx=25822178 
ny=51180968 
nz=51540158

nanocube = cube(xlow, xhigh-xlow, ylow, yhigh-ylow, zlow, zhigh-zlow)
nanocube.out()
s = nanocube.split()
s[0].out()
print("first split: ", len(s))
ss = s[0].split()
ss[0].out()
print("second split: ", len(ss))

exit(1)

for _ in range(10):
    for a in s:
        a.out()
        cubeq.put((1000-a.maxn, a))

# for x in [xlow, (xlow+xhigh)//2, xhigh]:
    # for y in [ylow, (ylow+yhigh)//2, yhigh]:
        # for z in [zlow, (zlow+zhigh)//2, zhigh]:
            # n = compr(x, y, z, True)
            # cubeq.put((1000-n, [x, y, z]))
# N:  418   (x,y,z):  15180888 91142140 56993562   Dist:  163316590   dx,dy,dz:  200012026 138951534 103272101



while not cubeq.empty():
    c = cubeq.get()
    c[1].out()
    
    s = c[1].split()
    for a in s:
        cubeq.put((1000-a.maxn, a))
    #    cubeq.put((1000-a.n, [a.xl, a.yl, a.zl]))
    #
# refine answer above to one closes to 0,0,0
#

compr(nx, ny, nz, True)

# 941 is too high
# 859 is too high
# at ( 23702519 52113511 52542838 ) there are  888  bots, dist =  128358868

#c c  Too low::  887  bots, dist =  126840872
# 1268++++++++++++++40873 too high?
# Too high::  888  bots, dist =  128049484
# at ( 25791613 51211533 51540158 ) there are  916  bots, dist =  128543304 (not correct)
# at ( 25822178 51180968 51540158 ) there are  943  bots, dist =  128543304
