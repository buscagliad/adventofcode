'''

--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

Your puzzle answer was 743.
--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

Your puzzle answer was 1493.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

class Hex:
    def __init__(self):
        self.center = 0
        self.q = 0
        self.s = 0
        self.r = 0
        self.maxd = 0

    def move(self, m):
        match m:
            case 'nw':
                self.q += -1
                self.s += 1
                self.r += 0
            case 'n':
                self.q += 0
                self.s += 1
                self.r += -1
            case 'ne':
                self.q += 1
                self.s += 0
                self.r += -1
            case 'se':
                self.q += 1
                self.s += -1
                self.r += 0
            case 's':
                self.q += 0
                self.s += -1
                self.r += 1
            case 'sw':
                self.q += -1
                self.s += 0
                self.r += 1
        d = self.distance()
        if d > self.maxd:
            self.maxd = d

    def out(self):
        print(" r: ", self.r,  "  q: ",  self.q,  "  s: ",  self.s)
        print("Distance: ", (abs(self.r) + abs(self.q) + abs(self.s))//2)
    
    def distance(self):
        return (abs(self.r) + abs(self.q) + abs(self.s))//2

    def maxdistance(self):
        return self.maxd

def process(line):
    h = Hex()

    for a in line.strip().split(","):
        h.move(a)

    print("Part 1: number of steps to get back to beginning is: ", h.distance())
    print("Part 2: maximum distance form beginning is: ", h.maxdistance())

for line in open("data.txt"):
    process(line)

def test():
    process("ne,ne,ne")
    process("ne,ne,sw,sw")
    process("ne,ne,s,s")
    process("se,sw,se,sw,sw")
