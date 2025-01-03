'''
--- Day 23: LAN Party ---

As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input).

The network map provides a list of every connection between two computers. For example:

kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn

Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.

LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.

In this example, there are 12 such sets of three inter-connected computers:

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq

If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:

co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn

Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?

Your puzzle answer was 1269.
--- Part Two ---

There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.

Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.

In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:

ka-co
ta-co
de-co
ta-ka
de-ta
ka-de

The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

What is the password to get into the LAN party?

Your puzzle answer was ad,jw,kt,kz,mt,nc,nr,sb,so,tg,vs,wh,yh.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

from collections import Counter
import numpy as np
import copy

NUMLETTERS=26
MAX=NUMLETTERS**2+5
pairs = []
related_pairs = []
tripList = set()
graph=np.zeros([MAX,MAX], dtype = int)


def toint(a):
    d1 = ord(a[0])-ord('a')
    d2 = ord(a[1])-ord('a')
    return d1 * NUMLETTERS + d2 + 1

ta = toint('ta')
tz = toint('tz')

def hast(n):
    if ta <= n and n <= tz: return True

def startWithT(a):
    return hast(a[0]) or hast(a[1])

def fromint(n):
    n -= 1
    a1 = n % NUMLETTERS
    a2 = n // NUMLETTERS
    return chr(a2 + ord('a')) + chr(a1 + ord('a'))
    


def process(line):
    global pairs, computer, graph
    c1 = line[0:2]
    c2 = line[3:5]
    n1 = toint(c1)
    n2 = toint(c2)

    if n1 < n2: pairs.append((n1,n2))
    else: pairs.append((n2,n1))
    graph[n1][n2] = graph[n2][n1] = graph[n1][n1] = graph[n2][n2] = 1
    for nm in [c1, c2]:
        ti = toint(nm)
        fi = fromint(ti)
        if fi != nm:
            print("ERROR: ", i, j)
    
    #computer.addedge(c1, c2, 1)

def commonPairs(r, p):
    global pairs
    # comparing pair p with pair r
    # one of the numbers must match for a matching pair to be found
    #
    a = b = -1
    if   r[0] == p[0]: 
        a = r[1]
        b = p[1]
        c = r[0]
    elif r[0] == p[1]: 
        a = r[1]
        b = p[0]
        c = r[0]
    elif r[1] == p[0]:
        a = r[0]
        b = p[1]
        c = r[1]
    elif r[1] == p[1]:
        a = r[0]
        b = p[0]
        c = r[1]
    if a == -1: return False, [0,0,0]
    if (min(a,b), max(a,b)) in pairs:
        return True, sorted([a, b, c])
    return False, [0,0,0]
                
def part1(fn):
    global tripList
    for l in open(fn):
        process(l)
    tripListWithT = set()
    # create new list from pairs
    for p in pairs:
        related_pairs.append([p])
    # find all pairs that match and append to related_pairs list
    # when adding a pair - if no element starts with t, do not 
    # include
    for i,p in enumerate(pairs):
        found = False
        for j,r in enumerate(pairs):
            if j == i: continue
            found, [a, b, c] = commonPairs(p, r)
            if not found: continue
            swt = startWithT(r) or startWithT(p)
            if swt:
                #print("T Triple: (", fromint(p[0]), fromint(p[1]), ") (", fromint(r[0]), fromint(r[1]), ") ")
            # if found is True
            # (a,b,c) forms a potential triple but ONLY if (b,c) is a
            # pair   p = (p1, p2)   r = (r1, r2)
            # if an element of p matches an element of r, then non-matching
            # elements (b, c) would form a triple if and only if (b,c) is
            # a pair itself
            #print("Appending: ", p, r)
                tripListWithT.add((a,b,c))
            tripList.add((a,b,c))
    count = len(tripListWithT)
    print("Part 1: number of 3-way lans that contain a t in the name: ", count)
    

def verify(cl):
    for a in cl:
        for b in cl:
            if graph[a][b] == 0:
                print("ERROR at ", a, b)
                return False
    return True

def getix(ix, jx):
    for i in range(ix, MAX):
        for j in range(jx, MAX):
            print(i+j)

def isclique(cl, add):
    for a in cl:
        if graph[a][add] == 0: return False
    return True


def buildClique(cl):
    for i in range(MAX):
        if i in cl: continue
        if graph[cl[0]][i] == 1:
            if isclique(cl, i):
                #print("adding ",i, flush=True)
                cl.append(i)
                buildClique(cl)
                verify(cl)



part1("data.txt")
#print("Total pairs: ", sum(sum(graph)), "  number of triples: ", len(tripList))

def outclique(t, clique):
    verify(clique)
    cl = sorted(clique)
    print(t, fromint(cl[0]),end="",sep="")
    for c in cl[1:]:
        print(",",fromint(c),end="",sep="")
    print()


maxc = 0
for i, t in enumerate(tripList):
    #print(" Working on ", i, t, flush=True)
    if i in t: continue
    cl = [t[0],t[1],t[2]]
    # if verify(cl): print("GOOD: ", cl)
    # else: print("BAD: ", cl)
    # continue
    buildClique(cl)
    # outclique("Clique found: ", cl)
    if maxc < len(cl):
        maxc = len(cl)
        maxcl = copy.deepcopy(cl)
 
outclique("Part 2: password is: ", maxcl)


