'''
--- Day 24: Electromagnetic Moat ---

The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from the side of the building at regular intervals and descend down into the void. There's no way to cross, but you need to get inside.

No way, of course, other than building a bridge out of the magnetic components strewn about nearby.

Each component has two ports, one on each end. The ports come in all different types, and only matching types can be connected. You take an inventory of the components by their port types (your puzzle input). Each port is identified by the number of pins it uses; more pins mean a stronger connection for your bridge. A 3/7 component, for example, has a type-3 port on one side, and a type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic, zero-pin port. Because of this, the first port you use must be of type 0. It doesn't matter what type of port you end with; your goal is just to make the bridge as strong as possible.

The strength of a bridge is the sum of the port types in each component. For example, if your bridge is made of components 0/3, 3/7, and 7/4, your bridge has a strength of 0+3 + 3+7 + 7+4 = 24.

For example, suppose you had the following components:

0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10

With them, you could make the following valid bridges:

    0/1
    0/1--10/1
    0/1--10/1--9/10
    0/2
    0/2--2/3
    0/2--2/3--3/4
    0/2--2/3--3/5
    0/2--2/2
    0/2--2/2--2/3
    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

(Note how, as shown by 10/1, order of ports within a component doesn't matter. However, you may only use each port on a component once.)

Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength of 0+1 + 1+10 + 10+9 = 31.

What is the strength of the strongest bridge you can make with the components you have available?

Your puzzle answer was 2006.
--- Part Two ---

The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

Of them, the one which uses the 3/5 component is stronger; its strength is 0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick the strongest one.

Your puzzle answer was 1994.

Both parts of this puzzle are complete! They provide two gold stars: **
'''
import copy

comps = []

def process(line):
    global comps
    w = line.strip().split('/')
    #print(w)
    p1 = int(w[0])
    p2 = int(w[1])
    comps.append((p1,p2))

def init(fn):
    global comps
    comps.clear()
    for line in open(fn):
        process(line)

def find(n, k): # find next component at or after k with the value n
    for i, (a, b) in enumerate(comps[k:]):
        if a == n or b == n:
            return k + i, a + b
    return -1, -1

def findx(tf, key):
    global comps
    z = []
    for i, a in enumerate(comps):
        if tf[i]: continue
        
        if key == a[0] or key == a[1]:
            z.append(i)
    return z
            
    

#for i, p in enumerate(comps):
#    print(i, p, sum(p))
    
def test1():
    for n in range(5):
        i = 0
        ix = 0
        print("n = ", n)
        while ix >= 0:
            ix, s = find(n, ix)
            if ix >= 0:
                print(ix, comps[ix], s)
            else:
                break
            ix += 1

def total(n):
    return sum(comps[n])

def getlist(n):
    i = 0
    ix = 0
    l = []
    while ix >= 0:
        ix, s = find(n, ix)
        if ix >= 0:
            l.append(ix)
        else:
            break
        ix += 1
    return l

maxtotal = 0
longlength = 0
longstrength = 0

def grow(tf, total, n):
    global maxtotal, longstrength, longlength
    g = findx(tf, n)
    if len(g) == 0:
        if total > maxtotal: maxtotal = total
        length = sum(tf)
        if length > longlength:
            longlength = length
            longstrength = total
        elif length == longlength:
            if total > longstrength:
                longstrength = total

    else:
        for i in g:
            ntf = copy.deepcopy(tf)
            ntf[i] = True
            if n == comps[i][0]:
                nn = comps[i][1]
            elif n == comps[i][1]:
                nn = comps[i][0]
            else:
                print("ERROR in grow")
                exit(1)
            grow(ntf, total + sum(comps[i]), nn)

         
init('data.txt')
   
start = []
    
for i in getlist(0):
    tf = [False] * len(comps)
    tf[i] = True
    start.append([tf, sum(comps[i]), max(comps[i])])

for t in start:
    #print(t)
    grow(t[0], t[1], t[2])
    
print("Part 1: strongest bridge is: ", maxtotal)
print("Part 2: longest strongest bridge is: ", longlength, " in length, and strength: ", longstrength)
