
import numpy as np

nodes = np.zeros((1000, 4), dtype=int)
dists = np.zeros((1000, 1000), dtype=int)
settrack = set()
nodecount = 0

circuits = []
counter = 0


#
# nodes = 0,1,2 are the xyz coordinates, 3 is the group (circuit) it is associated with.
#
def init(fname):
    global nodes, nodecount, settrack
    nodecount = 0
    for l in open(fname, 'r'):
        if len(l) < 3: break
        settrack.add(nodecount)
        m = l.strip().split(',')
        for i, a in enumerate(m):
            #print(nodecount, i, a)
            nodes[nodecount,i] = int(a)
        #print(nodes[nodecount])
        nodecount += 1


def pcircs():
    global circuits 
    vv = []
    for i, c in enumerate(circuits):
        vv.append(len(c))
    vv.sort(reverse=True)
    return vv

def dist(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

def compdists():
    global nodes, nodecount, dists
    for i in range(nodecount):
        for j in range(nodecount):
            dists[i,j] = dist(nodes[i], nodes[j])


def addpair(n1, n2, debug=False):
    global circuits, counter, settrack
    added = 0
    counter += 1
    csave1 = -1
    csave2 = -1
    if debug: print(counter, "addpair: ", n1, n2)
    settrack.discard(n1)
    settrack.discard(n2)
    for cn, c in enumerate(circuits):
        if n1 in c:
            csave1 = cn
            if debug: print(counter, added, "Added: ", n2, " to ", c)
        if n2 in c:
            csave2 = cn
            if debug: print(counter, added, "Added: ", n1, " to ", c)
    #
    # csave1 and csave2 are None - create new set
    # csave1 is none, but csave2 is not - add n2 to csave2
    # csave1 is NOT none, but csave2 is: add n1 to csave1
    # both csave1 and csave2 are NOT none - merge csave1 and csave2
    # 
    if csave1 >= 0 and csave2 >=0 :
        if csave1 != csave2:
            # we need to merge and remove a a set from circuits
            if debug: print(counter, "Before union: ", circuits[csave1])
            if debug: print(counter, "Union: ", circuits[csave2])
            circuits[csave1] = circuits[csave1].union(circuits[csave2])
            if debug: print(counter, "After union: ", circuits[csave1])
            if debug: print(counter, "Removing: ", circuits[csave2])
            circuits.pop(csave2)
            if debug: print(counter, "Merged to set: ", n1, n2, csave1)
    elif csave1 >= 0:
        circuits[csave1].add(n1)
        circuits[csave1].add(n2)
        if debug: print(counter, "Added to set: ", n1, n2, csave1)
    elif csave2 >= 0:
        circuits[csave2].add(n1)
        circuits[csave2].add(n2)
        if debug: print(counter, "Added to set: ", n1, n2, csave2)
    else:
        c = set()
        c.add(n1)
        c.add(n2)
        if debug: print(counter, "Created set with nodes ", n1, n2, c)
        circuits.append(c)
    
def findclosests():
    global nodes, nodecount, dists
    mindist = 1000000000000000000
    n1 = -1
    n2 = -1
    for i in range(nodecount):
        for j in range(i):
            if j == i: continue
            d = dists[i,j]
            if d > 0 and d < mindist:
                n1 = i
                n2 = j
                mindist = d
    if n1 >= 0 and n2 >= 0:
        dists[n1,n2] = 0
        dists[n2,n1] = 0
        addpair(n1, n2)
        for c in circuits:
            if len(c) == nodecount:
                print("Part 2: ", nodes[n1][0] * nodes[n2][0])
                exit(1)
        return True
    return False

init('data.txt')
LOOP = 1000
n1 = 0
n2 = 0
compdists()
q = 0
done = False
while True:
    q += 1
    findclosests()
    if (q == LOOP):
        vv = pcircs()
        print("Part 1: ", vv[1]*vv[2]*vv[0])
