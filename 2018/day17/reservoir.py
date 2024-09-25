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

UNKNOWN = 0
LEFT = 1
BOTTOM = 2
RIGHT = 3
TOP = 4

DEBUG = False

walls = []

WALL = -1
SAND = 0
PATH = 1    # water travelled through this spot
WATER = 2

drops = [(500,0)]

NOCONTAIN = 0
FLOATS = 1
CONTAINS = 2
CONTAINEDBY = 3

def fillline(lx, rx, y):
    global arr
    for x in range(lx, rx+1):
        if arr[x][y] == WALL:
            #print("fillline::  OH shit x/y: ", x, y, "  arr[x][y]: ", arr[x][y], " lx/rx: ", lx, rx)
            continue
        arr[x][y] = WATER
        
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
global_group = 1

def findbox(lx, rx, y):
    global arr, wallmap
    for x in range(lx, rx+1):
        #print(x, y, arr[x][y], wallmap[x][y])
        if arr[x][y] == WALL:
            boxid = wallmap[x][y]
            tb = getBox(boxid)
            ch = chr(ord('A') + boxid % 26)
            #print("Found box id: ", boxid, ch)
            return tb
    return None
#
# sides is a list of walls that make up sides of box
#
class Box():
    def __init__(self, sides):
        if len(sides) < 4: 
            self.open = True
        else:
            self.open = False
        
        #
        # determine the corners of the box:
        #
        self.bottomY = 0
        self.leftX   = maxx
        self.rightX  = minx
        self.leftY   = 0
        self.rightY  = 0
        self.groupID = sides[0].group
        self.charID = chr(ord('A') + self.groupID % 26)
        self.leftspill = None
        self.rightspill = None

        for s in sides:
            self.bottomY = max(s.yhigh, self.bottomY)
            self.leftX = min(s.xlow, self.leftX)
            self.rightX = max(s.xhigh, self.rightX)
        for s in sides:
            if s.kind == VERTICAL:
                if self.leftX == s.xlow:
                    self.leftY = s.ylow
                elif self.rightX == s.xlow:
                    self.rightY = s.ylow
        
                
        #
        # set spill points
        #
        self.leftspill = (self.leftX - 1, self.leftY-1)
        self.rightspill = (self.rightX + 1, self.rightY-1)
            
        self.topY = min(self.leftY, self.rightY)

        #
        # if containsBox is true, cBox is the box it contains (otherwise it is None)
        # 
        self.containType = NOCONTAIN
        self.cBox = None
    def clear(self, arr):  # only works on CLOSED boxes
        if self.open: return
        for y in range(self.rightY+1, self.bottomY):
            for x in range(self.leftX + 1, self.rightX):
                arr[x][y] = SAND
        
# AS FULL CONTAINMENT
# BOX: 547 OPENED    Left Drop:  (438, 568)  Right Drop:  (464, 568)  Left x/y:  439 569   Right x/y:  463 569   Y Top/Bottom:  569 580
# BOX: 551 OPENED    Right Drop:  (519, 105)  Left x/y:  499 105   Right x/y:  518 106   Y Top/Bottom:  105 117
    def contains(self, other):
        #
        # X ranges are in line
        #
        if self.leftX < other.leftX and other.rightX < self.rightX:
            #
            # Y ranges are in line
            #
            if self.bottomY > other.bottomY and other.bottomY > self.topY:
                self.cBox = other
                if other.topY > self.topY:
                    self.containType = CONTAINS
                    other.containType = CONTAINEDBY
                    other.cBox = self
                else:
                    self.containType = FLOATS
                return True
        return False
        
    #
    # fill will fill in arr with water per the boxes dimenstions
    # and return spills (either one or two) where the water overflows
    #
    # return spills
    #    only left or right if rising Cube -
    #
    def fill(self, arr, inx):
        # print("Calling fill, ID: ", self.groupID)
        spills = []
        if not self.open: return spills
        ##
        ## topY is the lowest value of Y to fill
        ## 
        if self.leftY == self.rightY:
            topY = self.leftY - 1
        else:
            topY = min(self.leftY, self.rightY) 
        if not self.open:
            if DEBUG: print("FILL: return on NOT open box: ", self.groupID)
            return []
        #if self.containType == CONTAINS and self.cBox.open:
        #    print("FILL: calling to fill internal box: ", self.cBox.groupID)
        #    return self.cBox.fill(arr, inx)    # contained boxes do NOT contain other boxes
        #elif self.containType == CONTAINEDBY:
        #    print("FILL: this is an internal box: ", self.cBox.groupID)
        #    return self.cBox.fill(arr, inx)    # contained boxes do NOT contain other boxes
        else:
            botY = self.bottomY
            #
            # test to see if this box has a box sticking out of it
            # if self.containType is FLOATS, then it does, in that case we run from left to start
            # of sticking out cube OR from right edge of box to right
            #

            if self.containType == FLOATS:  # sticking out
                tb = self.cBox
                # self.out()
                # tb.out()
                if inx < tb.leftX:
                    topY = self.leftY
                if inx > tb.rightX:
                    topY = self.rightY
                for y in range(topY, botY):
                    lx = self.leftX + 1
                    rx = self.rightX - 1
                    #
                    # is this a line that intersects floating box:
                    #
                    if y <= tb.bottomY:
                        if inx < tb.leftX:
                            rx = tb.leftX - 1
                        if inx > tb.rightX:
                            lx = tb.rightX + 1
                    if y <= tb.bottomY and y >= tb.topY:
                        fillline(lx, tb.leftX - 1, y)
                        fillline(tb.rightX + 1, rx, y)
                    else:
                        fillline(lx, rx, y)
                if inx < tb.leftX:
                    lx = self.leftX - 1
                    rx = tb.leftX - 1
                if inx > tb.rightX:
                    rx = self.rightX + 1
                    lx = tb.rightX + 1
                fillline(lx, rx, topY-1)
                #
                # return the left or right spill depending on which side the
                # water entered
                #
                if inx < tb.leftX:
                    spills.append(self.leftspill)
                else:
                    spills.append(self.rightspill)
                return spills
        
            elif self.containType == NOCONTAIN:
                if DEBUG: print("FILL: box ", self.charID, self.groupID, " no box sticking out --  topY/botY", topY, botY)
                for y in range(topY, botY):
                    lx = self.leftX+1
                    rx = self.rightX-1
                    if y == topY:
                        if self.leftY > topY:
                            lx = self.leftX - 1
                            if DEBUG: print("LEFT SPILL ", lx, self.leftspill)
                            spills.append(self.leftspill)
                        if self.rightY > topY:
                            rx = self.rightX + 1
                            if DEBUG: print("RIGHT SPILL ", rx, self.rightspill)
                            spills.append(self.rightspill)
                    fillline(lx, rx, y)
                return spills
            elif self.containType == CONTAINS:
                if DEBUG: print(" fill the contained box, then fill the container box")
                if DEBUG: print("FILL: box ", self.charID, self.groupID, " no box sticking out --  topY/botY", topY, botY)
                for y in range(topY, botY):
                    lx = self.leftX + 1
                    rx = self.rightX
                    if y == topY:
                        if self.leftY > topY:
                            lx = self.leftX - 1
                            if DEBUG: print("LEFT SPILL ", lx)
                            spills.append(self.leftspill)
                        if self.rightY > topY:
                            rx = self.rightX + 1
                            if DEBUG: print("RIGHT SPILL ", rx)
                            spills.append(self.rightspill)
                    fillline(lx, rx, y)
                    if not self.cBox.open:
                        self.cBox.clear(arr)
                return spills
            elif self.containType == CONTAINEDBY:
                if DEBUG: print("**** ==>  ",self.cBox.charID, " contains ", self.charID)
                #return self.cBox.fill(arr, inx)
                cytop = self.cBox.topY - 1
                cybot = self.cBox.bottomY
                isopen = self.open
                for y in range(cytop, cybot):
                    lx = self.cBox.leftX + 1
                    rx = self.cBox.rightX
                    if y == cytop:
                        if self.cBox.leftY > cytop:
                            lx = self.cBox.leftX - 1
                            spills.append(self.cBox.leftspill)
                        if self.cBox.rightY > cytop:
                            rx = self.cBox.rightX + 1
                            spills.append(self.cBox.rightspill)
                    fillline(lx, rx, y)

                return spills
                
            else:
                print("Bad contain type: ", self.containType)
                exit(1)
            # if there is a box contained, it is below the spill lines
            # we handle this 
            #
            # WORKING ON THIS:::  WOULD BE HELPFUL if we had each box with "containsBox" set
            # correctly for this part below
            #
 
    def out(self):
        print("BOX:", self.groupID, self.charID, end = "")
        if self.open: 
            print(" OPENED  ", end = "")
            if self.leftspill :
                print("  Left Drop: ", self.leftspill, end="")
            if self.rightspill :
                print("  Right Drop: ", self.rightspill, end="")
        else: 
            print(" CLOSED  ", end = "")
        print("  Left x/y: ", 
        self.leftX, 
        self.leftY,
        "  Right x/y: ",
        self.rightX,
        self.rightY,
        "  Y Top/Bottom: ", 
        self.topY, self.bottomY)
        if self.containType == FLOATS:
            print("   Contains a floating box: \n   ", end="")
            self.cBox.out()
        elif self.containType == CONTAINS:
            print("   Contains an internal box: \n   ",end="")
            self.cBox.out()

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
        self.group = 0
        if self.xlow < minx: minx = self.xlow
        if self.xhigh > maxx: maxx = self.xhigh

        if self.ylow < miny: miny = self.ylow
        if self.yhigh > maxy: maxy = self.yhigh
            
    def __lt__(self, other):
        return self.group < other.group

    def connectwith(self, other):
        global global_group
        if self.group > 0 and other.group > 0 and self.group != other.group:
            print("ERROR - in connectwith")
            self.out()
            other.out()
            return
        if self.group > 0:
            other.group = self.group
        elif other.group > 0:
            self.group = other.group
        else:
            global_group += 1
            self.group = global_group
            other.group = global_group
    def connected(self, other):
        if self.kind == other.kind: return False
        if self.kind == HORIZONTAL:
            horz = self
            vert = other
        else:
            horz = other
            vert = self
        
        if abs(horz.xlow - vert.xlow) + abs(horz.ylow - vert.ylow) <= 1: return True
        if abs(horz.xlow - vert.xlow) + abs(horz.ylow - vert.yhigh) <= 1: return True
        
        if abs(horz.xhigh - vert.xlow) + abs(horz.ylow - vert.ylow) <= 1: return True
        if abs(horz.xhigh - vert.xlow) + abs(horz.ylow - vert.yhigh) <= 1: return True
        
        return False

    def out2(self):
        print("x:: [", self.xlow, "..", self.xhigh, "]   ",
              "y:: [", self.ylow, "..", self.yhigh, "]  group: ", self.group)
    
#x=553, y=525..527
#y=30, x=554..581
    def out(self):
        if self.kind == VERTICAL:
            print("x=", self.xlow, ", y=", self.ylow, "..", self.yhigh, " group: ", self.group, sep="")
        else:
            print("y=", self.ylow, ", x=", self.xlow, "..", self.xhigh, " group: ", self.group, sep="")
    
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


##
## getBox will return the box with passed in ID (or None)
##
def getBox(n):
    if DEBUG: print("GetBox looking for ", n)
    for b in boxes:
        if b.groupID == n: return b
    return None

##
## returns box at bottom
##
def downbox(arr, drops, x, y):
    if DEBUG: print("Down Box at ", x, y)
    while y <= maxy and arr[x][y] != WALL:
        arr[x][y] = WATER
        if DEBUG: print("WATER set at ", x, y)
        y += 1
    if arr[x][y] != WALL:
        if DEBUG: print("y >= maxy ", y, maxy)
        return None
    b = getBox(wallmap[x][y])
    if b:
        if b.containType == CONTAINEDBY:
            b = b.cBox
    return b
    #
    # check to see if it hit the top right or left of the box
    #
    if (x,y) == (b.leftX, b.leftY):
        if DEBUG: print("LEFT  Need to add spills: ", x-1, y, "  and  ", x+1, y)
        fillline(x-1, x+1, y-1)
        drops.append((x-1, y-1))
        drops.append((x+1, y-1))
    elif (x,y) == (b.rightX, b.rightY):
        if DEBUG: print("RIGHT  Need to add spills: ", x-1, y, "  and  ", x+1, y)
        fillline(x-1, x+1, y-1)
        drops.append((x-1, y-1))
        drops.append((x+1, y-1))
    if DEBUG:
        if b: print("Bottom at ", x, y, "  returns: ", b.groupID)
        else: print("")
    return b
##
## counts number of water entries in the array
##
def countwater(arr):
    cnt = 0
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if arr[x][y] == WATER: cnt += 1
    return cnt
##
## output entire array
##
def printarr2(arr, lx, rx, uy, ly):
    for y in range(uy, ly+1):
        print("%4d " % y, end = "")
        for x in range(lx, rx+1):
            d = arr[x][y]
            ch = chr(ord('A') + wallmap[x][y] % 26)
            if x == 500 and y == 0: print("+", end="")
            elif d == SAND and x == 500: print(".", end="")
            elif d == WALL: print(ch, end="")
            elif d == SAND: print(" ", end="")
            elif d == WATER: print("+", end="")
            else: print("$", end="")
        print()
    print()
    
##
## output entire array
##
def printarr(arr, lx, rx, uy, ly):
    for y in range(uy, ly+1):
        print("%4d " % y, end = "")
        for x in range(lx, rx+1):
            d = arr[x][y]
            if x == 500 and y == 0: print("+ ", end="")
            elif d == WALL: print("# ", end="")
            elif d == SAND: print("  ", end="")
            elif d == WATER: print("+ ", end="")
            else: print("$ ", end="")
        print()
    print()

for line in open('data.txt'):
    process(line)

maxx += 1
minx -= 1

arr = np.zeros([maxx+30, maxy+20], dtype = int)
wallmap = np.zeros([maxx+30, maxy+20], dtype = int)
#print("ARR 0 panels: ", sum(sum(arr)))
if DEBUG: print(minx, maxx, miny, maxy)

ss = 0
gs = 0
for w in walls:
    ss += (w.xhigh - w.xlow + 1) * (w.yhigh - w.ylow + 1)
    gs += w.fill(arr)

##
## 
##
for i, w in enumerate(walls):
    for j, y in enumerate(walls):
        if j <= i: continue
        if w.connected(y):
            w.connectwith(y)
        
##
## group all walls that connect
##
for w in walls:
    for x in range(w.xlow, w.xhigh+1):
        for y in range(w.ylow, w.yhigh+1):
            wallmap[x][y] = w.group

walls.sort()
b = [walls[0]]
bgroup = walls[0].group
boxes = []
for w in walls[1:]:
    if bgroup == w.group:
        b.append(w)
    else:
        boxes.append(Box(b))
        b.clear()
        b.append(w)
        bgroup = w.group
boxes.append(Box(b))

##
## print map using a character for the outline of
## all boxes
##
def printwallmap():
    for y in range(miny, maxy+1):
        print("%4d " % y, end = "")
        for x in range(minx, maxx+1):
            d = wallmap[x][y]
            if x == 500 and y == 0: print("+ ", end="")
            elif d == 0:
                print("  ", end="");
            else:
                ch = chr(ord('A') + d % 26)
                print(ch, " ", end="",sep="")
        print()
    print()

if DEBUG: printarr(arr, minx, maxx, 0, maxy)
##
## output each box parameters
##
def outboxes():
    for b in boxes:
        b.out()

##
## Set all of the box containments
##
for thisb in boxes:
    for thatb in boxes:
        if thisb == thatb: continue
        thisb.contains(thatb)
        #if thisb.contains(thatb):
         #   print(thisb.groupID, thisb.charID, " contains ", 
          #        thatb.groupID, thatb.charID)

#printwallmap()


loops = 0
visited = []
while drops:
    loops += 1
    x,y = drops.pop()
    if (x,y) in visited: continue
    visited.append((x,y))
    b = downbox(arr, drops, x, y)
    if b: 
        ##
        ## need to check which box it fell on
        ##
        if b.open:
            ## did i hit the top edge?
            pass
            #if b.containType == CONTAINEDBY:
               # drops.append(b.cBox.leftX
        else:
            ## fill to spill points, then add spill points
            fillline(b.leftX, b.rightX, b.topY-1)
            drops.append((b.leftX-1, b.topY-1))
            drops.append((b.rightX+1, b.topY-1))
            if DEBUG: print("Dropped onto closed box: ", b.charID, b.topY)

        spills = b.fill(arr, x)
        if spills is None:
            if DEBUG: print("DO NOTHING")
        else:
            for s in spills:
                drops.append(s)
    if DEBUG: printarr(arr, minx, maxx, 0, maxy)
    


print("Part 1: number of cells that passed water is ", countwater(arr))

##
## part 2; just count the waters in the lowest part of each box
##
count = 0
for b in boxes:
    # b.cBox contains this box, if it is floating
    # then count the waters above the top of its container
    if b.containType == CONTAINEDBY:
        cbox = b.cBox
        if cbox.containType == FLOATS:
            botY = max(cbox.leftY, cbox.rightY)  # top edge of container cube
            for y in range(max(b.leftY, b.rightY), botY):
                for x in range(b.leftX + 1, b.rightX):
                    if arr[x][y] == WATER: count += 1
    else:
        boty = max(b.leftY, b.rightY)  # lowest top edge of box
        for y in range(max(b.leftY, b.rightY), b.bottomY):
            for x in range(b.leftX + 1, b.rightX):
                if arr[x][y] == WATER: count += 1

# 14475 is too low
# 24969 is too low
print("Part 2: number of cells hold water ", count)
