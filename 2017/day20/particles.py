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
        self.v = self.v0 + n * self.a
        self.p = self.p0 + self.v + self.a * (n * n - n) // 2
        
        

c = Coord(2, 4, 3)
c2 = Coord(2, 4, 3)
for n in range(10):
    c.move()
    print(n, end="")
    c.out()
c2.moven(10)
c2.out()
exit(1)

class Particle:
    def __init__(self, x, y, z, vx, vy, vz, ax, ay, az):
        self.x = Coord(x, vx, ax)
        self.y = Coord(y, vy, ay)
        self.z = Coord(z, vz, az)
    def move(self):
        self.x.move()
        self.y.move()
        self.z.move()
    def dist(self):
        return self.x.dist() + self.y.dist() + self.z.dist()

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

d = []
best_index = -1
times = 0
delta = 100
for _ in range(10, 20000, delta):
    for i in range(delta):
        for p in Particles:
            p.move()
        d.clear()
        for p in Particles:
            d.append(p.dist())
        bi = d.index(min(d))
        print(_, bi)
        if bi != best_index:
            best_index = bi
            times = 1
        else:
            best_index = bi
            times += 1
        if times > 4:
            break
        
print("Part 1: particle closes to origin is: ", best_index)


