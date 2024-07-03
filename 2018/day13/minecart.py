'''

--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
(2,0) East
(9,3) South

/-->\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/   
(3,0) East
(9,4) East

/---v        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/   
(4,0) South
(10,4) East


/---\        
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/   
(4,1) South
(11,4) East

/---\        
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/   
(4,2) East
(12,4) North


/---\        
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/   
(5,2) East
(12,3) North


/---\        
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/   
(6,2) East
(12,2) North


/---\        
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   
(7,2) East
(12,1) West


/---\        
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   
(8,2) East
(11,1) West

0123456789012
/---\        
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/   
(9,2) South
(10,1) West


0123456789012
/---\        
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
(9,3) South
(9,1) West


/---\        
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/   
(9,4) West
(8,1) West




/---\        
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/   
(8,4) West
(7,1) South


/---\        
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/   
(7,4) North
(7,2) South


/---\        
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/   
(7, 3) CRASH


After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\        
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/   

In this example, the location of the first crash is 7,3.

'''
import numpy as np

NORTH = (0,-1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

INVALID = 0
VERT = 1
HORZ = 2
JUNCTION = 3
CORNUL = 4
CORNUR = 5
CORNLL = 6
CORNLR = 7

XGRID = 160
YGRID = 160
grid = np.zeros([XGRID,YGRID], dtype = int)
carts = []
gtext = []

LEFT = 0
STRAIGHT = 1
RIGHT = 2

DEBUG = False

second = 0

#
# turn will take the Left/Straight/Right value
# and return the next direction and the state of the next turn (LEFT/STRAIGHT/RIGHT)
#
def turn(cdir, lsr):
    if lsr == STRAIGHT:
        return cdir, RIGHT
    elif lsr == LEFT:
        if cdir == EAST: return NORTH, STRAIGHT
        elif cdir == SOUTH: return EAST, STRAIGHT
        elif cdir == WEST: return SOUTH, STRAIGHT
        elif cdir == NORTH: return WEST, STRAIGHT
    elif lsr == RIGHT:
        if cdir == EAST: return SOUTH, LEFT
        elif cdir == SOUTH: return WEST, LEFT
        elif cdir == WEST: return NORTH, LEFT
        elif cdir == NORTH: return EAST, LEFT

ID = 1
class Cart:
    def __init__(self, x, y, c):
        global ID
        self.ID = ID
        ID += 1
        self.active = True
        self.x = x
        self.y = y
        self.dir = (0,0)
        self.turn = LEFT
        match c:
            case '>': self.dir = EAST
            case '<': self.dir = WEST
            case 'v': self.dir = SOUTH
            case '^': self.dir = NORTH
            case _ : print("ERROR in Cart init: c = ", c)
        # print("Cart at (", self.x, ",", self.y, ")  with dir: ", self.dir, " c: ", c)
    def remove(self):
        # print("Removing Cart: ", self.ID, " at ", self.x, self.y)
        self.active = False
    def removed(self):
        return not self.active
    def out(self):
        global gtext, grid
        print("Cart at (", self.x, ",", self.y, ")  with dir: ", self.dir, "  gtext: ", gtext[self.y][self.x], "   grid: ", grid[self.x][self.y] )
    def move(self):
        global second
        if not self.active: return
        if not self.dir:
            print("ERROR _ ", elf.x, self.y)
        spot =  grid[self.x][self.y]
        #
        # check if current char makes sense for the direction
        #
        if 1 or self.ID == 11: 
            if self.dir[0] == 0:    # moving in north/south direction
                if gtext[self.y][self.x] == '-':
                    print("XXX ERROR Cart: ", self.ID, " is at ", second, "[", self.x, self.y, "] :: ", 
                        spot, gtext[self.y][self.x], "  dir: ", self.dir)
            else:
                if gtext[self.y][self.x] == '|':
                    print("ZZZ ERROR Cart: ", self.ID, " is at ", second, "[", self.x, self.y, "] :: ", 
                        spot, gtext[self.y][self.x], "  dir: ", self.dir)
        self.x += self.dir[0]
        self.y += self.dir[1]
        self.dir = self.changedir()
        spot =  grid[self.x][self.y]
        if spot == 0   or  grid[self.y][self.x] == ' ':
            print("YYY Cart: ", self.ID, " is at ", self.x+1, self.y+1, " :: ", spot, gtext[self.y][self.x], "  dir: ", self.dir)
            #exit(1)
    def changedir(self):
        gv = grid[self.x][self.y]
        cdur = self.dir
        if gv < JUNCTION: return cdur
        if gv == CORNUL:
            if cdur == NORTH: return EAST
            elif cdur == WEST: return SOUTH
        elif gv == CORNUR:
            if cdur == EAST: return SOUTH
            elif cdur == NORTH: return WEST
        elif gv == CORNLL:
            if cdur == SOUTH: return EAST
            elif cdur == WEST: return NORTH
        elif gv == CORNLR:
            if cdur == EAST : return NORTH
            elif cdur == SOUTH : return WEST
        elif gv == JUNCTION:
            self.dir, self.turn = turn(cdur, self.turn)
            if DEBUG: print("JUNCTION -- at: ", self.x, self.y, "  gv: ", gv, "  cdur: ", cdur)
            return self.dir
            
        print("changedir - ", self.ID, "  ERROR - at: ", self.x, self.y, "  GTEXT: ", gtext[self.x][self.y], "  gv: ", gv, "  cdur: ", cdur)
        exit(1)
    def collision(self, other):
        if self.x == other.x and self.y == other.y: return True
        return False

def process(filename):
    global carts, grid, gtext
    y = 0
    for line in open(filename, 'r'):
        gtext.append(line)
    for g in gtext:
        x = 0
        for c in g:
            if c == '\n': continue
            elif c == '-': grid[x][y] = HORZ
            elif c == '|': grid[x][y] = VERT
            elif c == '/': 
                # /- or /+ makes  an Upper Left corner
                if  x == 0 or g[x+1] in ['-', '+', '<', '>']:
                    grid[x][y] = CORNUL
                    if DEBUG: print("Upper Left Corner at ", x, y, grid[x-1][y])
                else:
                    grid[x][y] = CORNLR
                    if DEBUG: print("Lower Right Corner at ", x, y, grid[x-1][y])
            elif c == '\\':
                if x == 0 or g[x+1] in ['-', '+', '<', '>']:
                    grid[x][y] = CORNLL
                    if DEBUG: print("Lower Left Corner at ", x, y, grid[x-1][y])
                else:
                    grid[x][y] = CORNUR
                    if DEBUG: print("Upper RIght Corner at ", x, y, grid[x-1][y])
            elif c in ['>', '<', '^', 'v']:
                carts.append(Cart(x, y, c))
                if c in ['>', '<']:
                    grid[x][y] = HORZ
                elif c in ['^', 'v']:
                    grid[x][y] = VERT
            elif c == '+':
                grid[x][y] = JUNCTION
                if DEBUG: print("Junction at ", x, y)
            x += 1
        y += 1

process('data.txt')
done = False
part1 = False
acount = len(carts)
while True:
    acount = 0
    for c in carts:
        if c.active: acount += 1
    if acount == 1: break
    second += 1
    for c in carts:
        c.move()
        for i, cl in enumerate(carts):
            if cl.removed(): continue
            for j, cr in enumerate(carts):
                if cr.removed(): continue
                if j <= i: continue
                collision = cl.collision(cr)
                if collision:
                    if not part1:
                        print("Part1: at second: ", second, " first collision at ", cl.x, ",", cl.y, " :: ", gtext[cl.y][cl.x])
                        part1 = True
                    cl.remove()
                    cr.remove()
                    #for c in carts:
                        #if c.removed(): continue
                        #print("At second: ", second, "Cart: ", c.ID, " is at ", c.x, c.y, " :: ", gtext[c.y][c.x])
for c in carts:
    if c.active:
        print("Part2: position of last cart at second ", second, " is ", c.x,",",c.y)
# 98, 125 is not correct
# 98, 126 is not correct
# 44, 87 is correct (why????)

