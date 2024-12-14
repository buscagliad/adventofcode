'''

--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

Your puzzle answer was 226236192.

--- Part Two ---
During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?

Your puzzle answer was 8168.

Both parts of this puzzle are complete! They provide two gold stars: **

'''



WIDE = 101 # x direction
TALL = 103 # y direction

GID = 1

class robot():
    def __init__(self, x, y, dx, dy):
        global GID
        self.t = 0
        self.startx = x
        self.starty = y
        self.x = x
        self.y = y
        self.dx = dx 
        self.dy = dy
        self.gid = GID
        GID += 1
    def __lt__(self, other):
        if self.y < other.y: return True
        if self.y == other.y:
            if self.x < other.x: return True
        return False
    def reset(self):
        self.x = self.startx
        self.y = self.starty
        self.t = 0
    def inc(self):
        self.t += 1
        self.x += self.dx
        self.x %= WIDE
        self.y += self.dy
        self.y %= TALL
    def dec(self):
        self.t -= 1
        self.x -= self.dx
        self.x += WIDE 
        self.x %= WIDE
        self.y -= self.dy
        self.y += TALL
        self.y %= TALL
    def move(self, s):
        self.x += s * self.dx
        self.x %= WIDE
        self.y += s * self.dy
        self.y %= TALL
    def quad(self):
        if self.x < WIDE // 2 and self.y < TALL // 2: return 0
        if self.x < WIDE // 2 and self.y > TALL // 2: return 1
        if self.x > WIDE // 2 and self.y < TALL // 2: return 2
        if self.x > WIDE // 2 and self.y > TALL // 2: return 3
        return 4
    def xy(self):
        return (self.x,self.y)
    def when(self, x, y):
        print("do nothing")
    def out(self):
        print("ID: ", self.gid, " t: ", self.t, "  (x,y): ", self.x, self.y, "  (dx,dy): ", self.dx, self.dy)

robots = []

# p=19,90 v=-87,96
def process(l):
    global robots
    w = l.strip().split()
    xy = w[0][2:].split(',')
    x = int(xy[0])
    y = int(xy[1])
    xy = w[1][2:].split(',')
    dx = int(xy[0])
    dy = int(xy[1])
    r = robot(x,y,dx,dy)
    robots.append(r)

for l in open('data.txt'):
    process(l)

#process("p=19,90 v=-87,96")
for r in robots:
    r.move(100)

q = [0,0,0,0,0]
for r in robots:
    #r.out()
    q[r.quad()] += 1

print("Part 1: safety factor is: ", q[0]*q[1]*q[2]*q[3])

for r in robots:
    r.reset()

#
# Part 2 - assume a star at the top of the christmas tree - 
#          it would be at 50,0
#
# we first need to find the first time any robot is at 50,0
#
import matplotlib.pyplot as plt 
def plotrobots(a):
    x = []
    y = []
    for r in robots:
        x.append(r.x)
        y.append(TALL-r.y)
    # Create the plot
    plt.scatter(x, y)

    # Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Christmas Tree  t = " + str(a))

    # Display the plot
    plt.show()

#
# we are searching for a 'dense' portion of the graph
# i clearly played with a number of values, and found that
# 300 was the correct number for the Christmas tree to
# show up
#
for a in range(1, 10404):
    q=[0,0,0,0,0]
    for r in robots:
        r.inc()
        q[r.quad()] += 1
    if max(q) > 300:
        plotrobots(a)
        break
print("Part 2: the Christmas Tree shows up at: ", a)
