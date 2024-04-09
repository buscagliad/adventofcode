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
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a
        self.n = 0
        self.p0 = p
        self.v0 = v
        self.a0 = a
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
        if dp == 0 and dv == 0 and da == 0:
            print("same")
            return False, 0
        if dv == 0 and da == 0:
            print("Bogus")
            return False, 0
            
        #
        # if da == 0 n is 2 dp / (2 dv + da)
        #
        if (da == 0):
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
        if rad < 0 : return False, 0
        radsqrt = isasqr(rad)

        # if rad is not a perfect square return False
        if radsqrt == 0: return False, 0
        d1 = -b + radsqrt
        d2 = -b - radsqrt
        if d1 > 0:
            if d1 % (2 * a) == 0:
                return True, d1//(2 * a)
        if d2 > 0:
            if d2 % (2 * a) == 0:
                return True, d2//(2 * a)
        return False, 0

class Particle:
    def __init__(self, x, y, z, vx, vy, vz, ax, ay, az):
        self.x = Coord(x, vx, ax)
        self.y = Coord(y, vy, ay)
        self.z = Coord(z, vz, az)
        self.collided = False
    def move(self):
        self.x.move()
        self.y.move()
        self.z.move()
    def moven(self, n):
        self.x.moven(n)
        self.y.moven(n)
        self.z.moven(n)
    def remove(self):
        self.collided = True
    def dist(self):
        return self.x.dist() + self.y.dist() + self.z.dist()
    def collides(self, other):
        tx, nx = self.x.collides(other.x)
        if not tx: return False, 0
        ty, ny = self.y.collides(other.y)
        if not ty: return False, 0
        if not ny == nx: return False, 0
        tz, nz = self.z.collides(other.z)
        if not tz: return False, 0
        if not nz == ny: return False, 0
        return True, nz
        
       

def crack(w):

    nl = w[3:w.find('>')]
    v = nl.split(',')
    return int(v[0]), int(v[1]), int(v[2])
    
Particles=[]

def process(line):
    global Particles
    w = line.split()
    #
    #print(w)
    x, y, z = crack(w[0])
    vx, vy, vz = crack(w[1])
    ax, ay, az = crack(w[2])
    Particles.append(Particle(x, y, z, vx, vy, vz, ax, ay, az))

for line in open('data.txt'):
    process(line)

#
# assume after 100000 moves, the closest to origin
# will remain closest to origin
#
d = []
N = 100000
for p in Particles:
    p.moven(N)
    d.append(p.dist())
            
best_index = d.index(min(d))

        
print("Part 1: particle closest to origin is: ", best_index)

for i, p in enumerate(Particles):
    for j, q in enumerate(Particles[i+1:]):
        t, n = p.collides(q)
        if t:
            print(i, i+j+1)
