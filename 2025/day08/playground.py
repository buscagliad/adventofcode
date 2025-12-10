
import numpy as np

nodes = np.zeros((1000, 4), dtype=int)
dists = np.zeros((1000, 1000), dtype=int)
compare = np.zeros((1000, 1000), dtype=bool)
# nodes = [[0]*4]*1000
# dists = [[0]*1000]*1000
nodecount = 0

def countcon():
    global nodes, nodecount
    for i in range(nodecount):
        if nodes[i][3] == 0: return False
    return True

def xvals():
    global nodes, nodecount
    for i in range(nodecount):
        print(nodes[i,3])
            
def pvals():
    global nodes, nodecount
    for i in range(nodecount):
        print(i, nodes[i])


#
# nodes = 0,1,2 are the xyz coordinates, 3 is the group (circuit) it is associated with.
#
def init(fname):
    global nodes, nodecount
    nodecount = 0
    for l in open(fname, 'r'):
        if len(l) < 3: break
        m = l.strip().split(',')
        for i, a in enumerate(m):
            #print(nodecount, i, a)
            nodes[nodecount,i] = int(a)
        #print(nodes[nodecount])
        nodecount += 1
    #pvals()


def pcircs(nc, prnt = False):
    global nodes, nodecount  
    vv = [0] * circid
    for i in range(nodecount):
        vv[nodes[i,3]] += 1
    if prnt: print(vv)
    return vv

def dist(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

def compdists():
    global nodes, nodecount, dists
    for i in range(nodecount):
        for j in range(nodecount):
            dists[i,j] = dist(nodes[i], nodes[j])

def getjunction():
    global nodes, nodecount, dists
    mindist = 1000000000000000000
    n1 = -1
    n2 = -1
    for i in range(nodecount):
        if nodes[i][3] > 0: continue
        for j in range(nodecount):
            if j == i: continue
            d = dists[i,j]
            if d > 0 and d < mindist:
                n1 = i
                n2 = j
                mindist = d
    if n1 >= 0 and n2 >= 0:
        dists[n1,n2] = 0
        dists[n2,n1] = 0
    return n1, n2

init('test.txt')
n1 = 0
n2 = 0
compdists()
circid = 1
allconnected = False
#while not allconnected:
for q in range(10):
    n1, n2 = getjunction()
    if (n1 < 0): break
    ## merge nodes use node n1 and the merger
    if nodes[n1,3] > 0 and nodes[n2,3] > 0:
        if nodes[n1,3] == nodes[n2,3]:
            print("Ignoring node ", nodes[n2], " to node ", nodes[n1])
            continue

        print("Merging node ", nodes[n2,3], n2, " to node ", nodes[n1,3], n1)
        fromnode = nodes[n2,3]
        tonode = nodes[n1,3]
        for i in range(nodecount):
            if nodes[i,3] == fromnode:
                nodes[i,3] = tonode
                #print("XXXX", i, n2, nodes[i,3], nodes[n1,3])
    elif nodes[n1,3] > 0:
        nodes[n2,3] = nodes[n1,3]
        print("Junction node: ", n2, nodes[n2], " added to junction ", n1, nodes[n1])
        
    elif nodes[n2,3] > 0:
        nodes[n1,3] = nodes[n2,3]
        print("Junction node: ", n1, nodes[n1], " added to junction ", n2, nodes[n2])
    #
    # new circuit
    #
    else:
        nodes[n1,3] = circid
        nodes[n2,3] = circid
        print("Junction created: ", circid, " NODES are: ", n1, nodes[n1], " and ", n2, nodes[n2])
        circid += 1
    pcircs(circid, True)
    allconnected = countcon()

    
vv = pcircs(circid)
vv[0] = 0
vv.sort(reverse=True)
print(vv)
print("Part 1: ", vv[1]*vv[2]*vv[0])

