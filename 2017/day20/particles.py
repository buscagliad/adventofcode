'''

--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parentheses), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

Your puzzle answer was 300.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?


'''
import math

def isasqr(a: int):
    b = int(math.sqrt(float(a)))
    if b*b == a: return b
    return 0

class Coord:
    def __init__(self, p, v, a, debug = False):
        self.p = p
        self.v = v
        self.a = a
        self.n = 0
        self.p0 = p
        self.v0 = v
        self.a0 = a
        self.debug = debug
    def move(self):
        self.v += self.a
        self.p += self.v
        self.n += 1
    def dist(self):
        return abs(self.p)
    def out(self):
        print(" p: ", self.p, "  v: ", self.v, "  a: ", self.a, "  dist: ", self.dist())
    def moven(self, n):
        self.n = n
        self.v = self.v0 + n * self.a
        self.p = self.p0 + self.v0 * n + self.a * (n * n + n) // 2
    def collides(self, other):
        dp = self.p0 - other.p0
        dv = self.v0 - other.v0
        da = self.a0 - other.a0
        if self.debug: print("dp: ", dp, "  dv: ", dv, "  da: ", da)
        if dp == 0 and dv == 0 and da == 0:
            return True, 0
        if dv == 0 and da == 0:
            return False, 0
            
        #
        # if da == 0 n is 2 dp / (2 dv + da)
        #
        if (da == 0):
            if self.debug: print("da == 0")
            k = (2 * dp) % (2 * dv + da)
            if k == 0:
                return True, (2 * dp) // (2 * dv + da)
            else:
                return False, 0
        #
        # (da) n^2 + (2 * dv + da) n + 2 * dp = 0
        a = da
        b = 2 * dv + da
        c = 2 * dp
        rad = b * b - 4 * a * c
        if self.debug: print(a, b, c, rad)
        if rad < 0 : return False, 0
        elif rad > 0:
            radsqrt = isasqr(rad)

            # if rad is not a perfect square return False
            if radsqrt == 0: return False, 0
        else:
            radsqrt = 0
        d1 = -b + radsqrt
        d2 = -b - radsqrt
        res = None
        if self.debug: print("--- d1, d2, (2 * a)", d1, d2, (2 * a))
        if d1 == 0 or d2 == 0: return True, 0
        if d1 * a  > 0:
            if self.debug: print("A:  d1, 2*a, d1 % (2 * a)", d1, 2*a, d1 % (2 * a))
            if d1 % (2 * a) == 0:
                res = d1//(2 * a)
        if d2 * a > 0:
            if self.debug: print("B:  d2, 2*a, d2 % (2 * a)", d2, 2*a, d2 % (2 * a))
            if d2 % (2 * a) == 0:
                v = d2//(2 * a)
                if not res:
                    res = v
                else:
                    if v < res: res = v
        if res:
            return True, res
        return False, 0

class Particle:
    def __init__(self, x, y, z, vx, vy, vz, ax, ay, az, nm, debug = False):
        self.x = Coord(x, vx, ax)
        self.y = Coord(y, vy, ay)
        self.z = Coord(z, vz, az)
        self.collided = 0
        self.name = nm
        self.debug = debug
    def equal(self, other):
        if ( self.x.p == other.x.p and
             self.y.p == other.y.p and
             self.z.p == other.z.p) : return True
        return False
    def move(self):
        self.x.move()
        self.y.move()
        self.z.move()
    def moven(self, n):
        self.x.moven(n)
        self.y.moven(n)
        self.z.moven(n)
    def dist(self):
        return self.x.dist() + self.y.dist() + self.z.dist()
    def collides(self, other):
        tx, nx = self.x.collides(other.x)
        if (self.debug): print(">>>>>> x: ", tx, nx)
        if not tx: return False, 0
        ty, ny = self.y.collides(other.y)
        if (self.debug): print(">>>>>> y: ", ty, ny)
        if not ty: return False, 0
        if not ny == nx: return False, 0
        tz, nz = self.z.collides(other.z)
        if (self.debug): print(">>>>>> z: ", tz, nz)
        if not tz: return False, 0
        if not nz == ny: return False, 0

        if other.collided:
            print("OUCH!! ", self.name, other.name)
        return True, nz
    def remove(self, nz):
        self.collided = nz
    def out(self):
        print(self.name, "(", self.x.p0, ",", self.y.p0, ", ", self.z.p0, ")   at ", 
            self.x.n, "  Pos:  ", self.x.p, self.y.p, self.z.p)
        
        
       

def crack(w):

    nl = w[3:w.find('>')]
    v = nl.split(',')
    return int(v[0]), int(v[1]), int(v[2])
    
Particles=[]

def process(line, nm):
    global Particles
    w = line.split()
    #
    #print(w)
    x, y, z = crack(w[0])
    vx, vy, vz = crack(w[1])
    ax, ay, az = crack(w[2])
    Particles.append(Particle(x, y, z, vx, vy, vz, ax, ay, az, nm))

k = 0
for line in open('data.txt'):
    process(line, k + 1)
    k += 1

#
# assume after 100000 moves, the closest to origin
# will remain closest to origin
#
def part1():
    d = []
    N = 100000
    for p in Particles:
        p.moven(N)
        d.append(p.dist())
                
    best_index = d.index(min(d))
    return best_index

        
#print("Part 1: particle closest to origin is: ", part1())

def commutative():
    p = Particles[492]
    q = Particles[496]
    t, n = p.collides(q)
    print(t, n)
    p.moven(n)
    p.out()
    q.moven(n)
    q.out()
    t, n = q.collides(p)
    print(t, n)
    p.moven(n)
    p.out()
    q.moven(n)
    q.out()
    exit(1)

    commutative()
    exit()

def part2():
    for i, p in enumerate(Particles):
        for j, q in enumerate(Particles):
            if i <= j: continue
            #print("Comparing ", p.name, " with ", q.name)
            t, n = p.collides(q)
            if t:
                print("FOUND: ", i+1, j+1, n)
                tt, nn = q.collides(p)
                if not tt:
                    print("PROBLEM: i,j: ", i+1, j+1)
                    q.out()
                    p.out()
                p.moven(n)
                q.moven(n)
                if not p.equal(q):
                    print("ERROR")
                    p.out()
                    q.out()
                # else:
                    # print("GOOD")
                    # p.out()
                    # q.out()            #p.out()
                #q.out()
                #print()
count = 0
#
# Need to find out why the above only comes up with 507 - meaning
# there are 5 more collisions when we do it brute force
#
pairs={}
for n in range(1, 50):
    for p in Particles: p.move()
    for i, p in enumerate(Particles):
        #if p.collided : continue
        for j, q in enumerate(Particles):
            if j <= i : continue
            #if q.collided : continue
            if p.equal(q):
                print("Found two intersections at time: ", n, " Particles: ", i+1, j+1)
                p.remove(n)
                q.remove(n)
                pairs[(i, j)] = n

count = 0
for p in Particles:
    if not p.collided: count += 1

print("Part 2: number of non-colliding particles: ", count)
# 863 is too high
# 746 is too high
# 507 is too high
#print(pairs)
def part2():
    for (i,j) in pairs:
        #print(i, j, pairs[(i,j)]) 
        #p.out()
        t, n = Particles[j].collides(Particles[i])
        if n != pairs[(i,j)]:
            print("Error at indexes: ", i, j, " found ", n, "  should be ", pairs[(i,j)])

