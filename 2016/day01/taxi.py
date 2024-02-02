
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Walk:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fx = 0
        self.fy = 0
        self.fset = False
        self.hdg = NORTH
        self.places = []
    def step(self, s):
        # print(s)
        steps = int(s[1:])
        if s[0] == 'R':
            self.hdg += 1
            self.hdg %= 4
        else:
            self.hdg -= 1
            if self.hdg < 0: self.hdg = WEST
        dx = 0
        dy = 0
        if self.hdg == NORTH: 
            dy = 1
        elif self.hdg ==  SOUTH: 
            dy = -1
        elif self.hdg ==  WEST: 
            dx = -1
        elif self.hdg ==  EAST: 
            dx = 1
        else:
            print("ERROR")
            exit(2)
        for i in range(steps):
            self.x += dx
            self.y += dy
            #print(self.x, self.y)
            if (self.x, self.y) in self.places and not self.fset: # and self.fx == 0 and self.fy == 0:
                #print("Visited: ", self.x, self.y)
                self.fx = self.x
                self.fy = self.y
                self.fset = True
            self.places.append((self.x, self.y))
        
    def dist(self):
        return abs(self.x) + abs(self.y)
    def fdist(self):
        return abs(self.fx) + abs(self.fy)

w = Walk()
for line in open('data.txt'):
    ls = line.strip()
    for s in ls.split(', '):
        w.step(s)

print("Part 1: distance is: ", w.dist())
print("Part 2: first revisited place distance is: ", w.fdist())

