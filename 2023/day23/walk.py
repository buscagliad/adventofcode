import numpy as np
import heapq as heap
import copy
from collections import defaultdict

class Graph:
    def __init__(self, directed = True):
        self.vertices=[]
        self.edges=defaultdict()
        self.vertNames=defaultdict()
        self.directed = directed
        self.debug = False
    def __str__(self):
        self.printGraph()
    def addedge(self, vertA, vertB, dist):
        if not vertA in self.vertices:
            self.vertices.append(vertA)
        if not vertB in self.vertices:
            self.vertices.append(vertB)
        self.edges[vertA, vertB] = dist
        if not self.directed:
            self.edges[vertB, vertA] = dist
    def  print(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    print(v1, " --> ", v2, " : ", self.edges[(v1,v2)])
    def getmindistance(self, start, stop):
        if not start in self.vertices:
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if not stop in self.vertices:
            print("ERROR - End point ", stop, " is not a vertex")
            return -1
        visited = [False] * len(self.vertices)
        # don't have an Inf for integers - going to assume 1 trillion is large enough
        distance = defaultdict()
        q = []
        for v in self.vertices:
            distance[v] = 1000000000000
            heap.heappush(q, v)
        distance[start] = 0
        while q:
            current = q.pop()
            if (self.debug) : print(current, " ", distance[current])
            visited.append(current)
            for adjNode in self.vertices:
                #if adjNode in visited: continue
                if not (current, adjNode) in self.edges: continue
                newDist = distance[current] + self.edges[current, adjNode]
                if distance[adjNode] > newDist:
                    distance[adjNode] = newDist
                    if (self.debug) : print("***", current, " -> ", adjNode, " == ", newDist)
                    heap.heappush(q, adjNode)
        return distance[stop]
                
    def getmaxdistance(self, start, stop):
        if not start in self.vertices:
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if not stop in self.vertices:
            print("ERROR - End point ", stop, " is not a vertex")
            return -1
        visited = [False] * len(self.vertices)
        distance = defaultdict()
        q = []
        for v in self.vertices:
            distance[v] = 0
            heap.heappush(q, v)
        distance[start] = 0
        while q:
            current = q.pop()
            if (self.debug) : print(current, " ", distance[current])
            visited.append(current)
            for adjNode in self.vertices:
                #if adjNode in visited: continue
                if not (current, adjNode) in self.edges: continue
                newDist = distance[current] + self.edges[current, adjNode]
                if distance[adjNode] < newDist:
                    distance[adjNode] = newDist
                    if (self.debug) : print("***", current, " -> ", adjNode, " == ", newDist)
                    heap.heappush(q, adjNode)
        return distance[stop]  
        
grid = np.zeros([200,200], dtype = int)
gridCol = 0
gridRow = 0

##
#             RIGHT    DOWN     LEFT    UP       NO-OP    
DIRlist  = [ ( 0, 1), (1, 0), (0, -1), (-1, 0), ( 0, 0)  ]
DIRname = [ "RIGHT", "DOWN", "LEFT", "UP", "NO-OP" ]

START = -1
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
NOOP = 4
'''
def connected(a, b):
    if a == b: return True
    return False

class Node:
    def __init__(self, start, stop, steps, endNode = False):
        self.connected = []
        self.visited = []
        self.start = start
        self.stop = stop
        self.hash = start[0] + 100 * start[1] + 10000 * stop[0] + 1000000 * stop[1]
        self.steps = steps
        self.nodemin = steps
        self.nodemax = steps
        self.dist = steps
        self.endNode = endNode

    def __eq__(self, other):
        return (self.hash == other.hash)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.hash < other.hash)

    def __gt__(self, other):
        return (self.hash > other.hash)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)
        
    def getqueue(self, q):
        if not self in q:
            print("GETQ: ", self.start, self.stop, self.steps)
            q.append(self)
        if not self.connected: return
        for a in self.connected:
            a.getqueue(q)


    def search(self):
        visited = set()
        q = []
        nodeCosts = defaultdict(lambda: 0)
        startingNode = self
        heap.heappush(q, (0, startingNode))
        #self.getqueue(q)
        nodeCosts[startingNode.hash] = self.steps

        while q:
            total, s = heap.heappop(q)
            visited.add(s.hash)
            if s.stop == (gridRow-1, gridCol-2):
                return total
            for adjNode in s.connected:
            #print (adjNode.start, adjNode.stop, adjNode.steps, " --> ", nodeCosts[adjNode.hash])
                if adjNode.hash in visited: continue
                sm = nodeCosts[s.hash] + adjNode.steps + 1
                if nodeCosts[adjNode.hash] < sm :
                    nodeCosts[adjNode.hash] = sm
                    print("Appending ", adjNode.hash, adjNode.start, adjNode.stop, 
                        adjNode.steps, " --> ", sm)
                    heap.heappush(q, (sm, adjNode))

        # This hike contains 94 steps. (The other possible hikes you 
        # could have taken were 90, 86, 82, 82, and 74 steps long.)


    def PrintTree(self):
        print(self.start, self.stop, self.steps, " --> ", self.dist)
        if not self.connected: return
        for c in self.connected:
            c.PrintTree()

    def insert(self, start, stop, steps, endNode = False):
        #print("INSERT:: Comparing ", self.stop, " to ", start)
        if connected(self.stop, start):
            #print("APPENDING::  ", start, " to ", self.stop)
            self.connected.append(Node(start, stop, steps, endNode))
            self.visited.append(False)
            return True
        # Compare the new value with the parent node
        if not self.connected:
            return False
        tv = False
        for c in self.connected:
            tv = tv or c.insert(start, stop, steps, endNode)
        return tv

    def sum(self, s = 0):
        global pathMin
        global pathMax
        s += self.steps
        print("sum-", s)
        if self.connected:
            for c in self.connected:
                s = c.sum(s)
                if s > self.nodemax:
                    self.nodemax = s
                elif s < self.nodemin:
                    self.nodemin = s
        return s
'''
def process(line):
    global gridRow
    global gridCol
    j = 0
    gridCol = len(line) - 1
    for a in line.strip():
        if a == '#':
            grid[gridRow][j] = -1
        elif a == '>':
            grid[gridRow][j] = RIGHT
        elif a == '<':
            grid[gridRow][j] = LEFT
        elif a == '^':
            grid[gridRow][j] = UP
        elif a == 'v':
            grid[gridRow][j] = DOWN
        elif a == '.':
            grid[gridRow][j] = NOOP
        j += 1
    gridRow += 1

'''
def getVal(g, s, d):
    i = s[0] + DIRlist[d][0]
    j = s[1] + DIRlist[d][1]
    #print("getval: ", i, j,"  v: ",grid[i][j])
    return g[i][j]
'''
def nextSteps(c, d):
    steps = []
    endpath = False
    for nd in [RIGHT, DOWN, LEFT, UP]:
        if d == (nd + 2) % 4: continue  # cannot go backwards
        i = c[0] + DIRlist[nd][0]
        j = c[1] + DIRlist[nd][1]
        if i < 0 or i >= gridRow: continue
        if j < 0 or j >= gridCol: continue
        if grid[i][j] == -1: continue
        if grid[i][j] == NOOP: 
            endpath = False
            steps.append([(i,j), nd])
            break
        else:
            steps.append([(i,j), nd])
            endpath = True
            break
    return endpath, steps

def moveStep(s, d):
    i = s[0] + DIRlist[d][0]
    j = s[1] + DIRlist[d][1]
    if i < 0 or i >= gridRow: return
    if j < 0 or j >= gridCol: return
    return (i,j)

seen = set()
paths = []
def getTree(start, d):
    global seen

    starters = [[start, d]]
    finalStep = (gridRow-1, gridCol-2)
    trueStart = True
  #if (start,d) in seen: return
    while starters:
        start, d = starters.pop()
        npt = (start[0] + DIRlist[d][0], start[1] + DIRlist[d][1])
        if not trueStart and not d == grid[npt]:
            #print("Rejected")
            continue
        trueStart = False
        curStep = start
        lastStep = curStep
        curStep = moveStep(curStep, d)
        steps = 1
        done = False
        lastDir = d
    
        while not done:
            endpath, s = nextSteps(curStep, d)
            #print("Next step: ", s)
            if len(s) == 0: break
            steps += 1
            if steps == 1: endpath = False
            curStep = s[0][0]
            d = s[0][1]
            #print("nextSteps: ", endpath, curStep)
            if curStep == finalStep:
                if not ((start, s[0][0])) in seen:
                    paths.append([start, s[0][0], steps])
                    seen.add((start, s[0][0]))
                done = True
            if endpath:
                a, b = nextSteps(curStep, d)
                if not ((start, b[0][0])) in seen:
                    paths.append([start, b[0][0], steps])
                    seen.add((start, b[0][0]))
                #print("End of path: ", s, "  a: ", a, "  b: ", b)
                for n in [RIGHT, DOWN, LEFT, UP]:
                    if n == (b[0][1] + 2) % 4: continue ## cannot reverse direction
                    starters.append([b[0][0], n])
                    #print("Pushed on queue Next: ", b[0][0], n, DIRname[n])
                done = True


for line in open('data.txt', 'r'):
    process(line)

getTree((0,1), DOWN)

'''
tr = Node(paths[0][0], paths[0][1], paths[0][2])
used = [0]*len(paths)
used[0] = 1
done = False
for p in paths:
    print(p[0], p[1], p[2])


while not done:
    found = False
    for i, p in enumerate(paths):
        if used[i] == 1: continue
        #print("Looking to insert: ", p[0], p[1], p[2])
        last = (p[1] == (gridRow-1,gridCol-2))
        #if (last) : print("LAST")
        if tr.insert(p[0], p[1], p[2], last): 
            used[i] = 1
            #print("Inserted: ", p[0], p[1], p[2], " total: ", sum(used))
            found = True
            break
    done = (sum(used) == len(paths)) or (not found)
'''
endPoint = (gridRow-1,gridCol-2)

def getGraph(p):
    g = Graph()
    for p in paths:
        if p[1] == endPoint: one = 0
        else: one = 1
        g.addedge(p[0],p[1],p[2]+one)
    return g

g = getGraph(paths)

# print(verts)
# print(edges)
# print(tr.sum())
# print(tr.nodemin, tr.nodemax)
# print(tr.search())
#tr.PrintTree()

print("Get min distance: ", g.getmindistance((0, 1), endPoint))
print("Get max distance: ", g.getmaxdistance((0, 1), endPoint))

    
# for i, p in enumerate(paths):
  # if used[i] == 1: continue
  # print("NOT able to insert: ", p[0], p[1], p[2])
