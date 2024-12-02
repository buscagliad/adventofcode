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

def bgrid(x1, x2, y1, y2, z1, z2):
    dx = abs(x2 - x1) // 2
    dy = abs(y2 - y1) // 2
    dz = abs(z2 - z1) // 2
    c = []
    for x in [x1-dx, x1, x1+dx, x2, x2+dx]:
        for y in [y1-dy, y1, y1+dy, y2, y2+dy]:
            for z in [z1-dz, z1, z1+dz, z2, z2+dz]:
                c.append([x,dx,y,dy,z,dz,compr(x,y,z),abs(x)+abs(y)+abs(z)])
    c = sorted(c, key=lambda c:(1000-c[6],c[7]))   
    return(c[0])          

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
#cont = np.zeros(1000, dtype=int)
large = bots[0]
small = bots[0]
[xlow,xhigh] = [100000000000, -100000000000]
[ylow,yhigh] = [100000000000, -100000000000]
[zlow,zhigh] = [100000000000, -100000000000]

for ai, a in enumerate(bots):
    #cont[ai] = compr(a.x, a.y, a.z)
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
# nx=25822178 
# ny=51180968 
# nz=51540158
# xlow = nx - 25000000
# xhigh = nx + 25000000
# ylow = ny - 25000000
# yhigh = ny + 25000000
# zlow = nz - 25000000
# zhigh = nz + 25000000
# for _ in range(25):
while True:
    c = bgrid(xlow, xhigh, ylow, yhigh, zlow, zhigh)
    #print(c)
    xlow = c[0]
    xhigh = c[0] + c[1]

    ylow = c[2]
    yhigh = c[2] + c[3]

    zlow = c[4]
    zhigh = c[4] + c[5]
    if c[1] <= 1 and c[3] <= 1 and c[5] <= 1: break

print("Part 2: manhattan distance of maximal (x,y,z) point: ", c[7])
# 941 is too high
# 859 is too high
# at ( 23702519 52113511 52542838 ) there are  888  bots, dist =  128358868

#c c  Too low::  887  bots, dist =  126840872
# 1268++++++++++++++40873 too high?
# Too high::  888  bots, dist =  128049484
# at ( 25791613 51211533 51540158 ) there are  916  bots, dist =  128543304 (not correct)
# at ( 25822178 51180968 51540158 ) there are  943  bots, dist =  128543304
