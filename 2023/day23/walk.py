import numpy as np
import heapq as heap
import copy
from collections import defaultdict
from collections import deque

graph_id = 0

def hash_it(i, j):
    return 100 * j + i
    
class Graph:
    def __init__(self, directed = False):
        self.vertices=[]
        self.edges=defaultdict()
        self.vertIDs=[]
        self.directed = directed
        self.id = []
        self.debug = False
    def __str__(self):
        self.printGraph()
    def addedge(self, vertA, vertB, dist):
        global graph_id
        if not vertA in self.vertices:
            self.vertices.append(vertA)
            self.vertIDs.append(graph_id)
            graph_id += 1
        if not vertB in self.vertices:
            self.vertices.append(vertB)
            self.vertIDs.append(graph_id)
            graph_id += 1
        self.edges[vertA, vertB] = dist
#        if not self.directed:
#            self.edges[vertB, vertA] = dist

    def negate(self):   # negate all edges
       for i1, v1 in enumerate(self.vertices):
            for i2, v2 in enumerate(self.vertices):
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    self.edges[(v1,v2)] *= -1

    # if a vertex has two in and two out, add the 
    # return edge as well
    def part2(self):
        counter = [0] * len(self.vertices)
        for i1, v1 in enumerate(self.vertices):
            for i2, v2 in enumerate(self.vertices):
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    counter[i1] += 1
                    counter[i2] += 1
        for i1, v1 in enumerate(self.vertices):
#            if counter[i1] < 4: continue
            for i2, v2 in enumerate(self.vertices):
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    if (v2,v1) not in self.edges:
                        if counter[i2] >= 3 and counter[i1] >= 3:
                            if counter[i1] == 3 and counter[i2] == 3: continue
                            self.edges[(v2,v1)] = self.edges[(v1,v2)]


    def merge(self):
        elist = []
        for u in self.vertices:
            for v in self.vertices:
                if (u, v) in self.edges:
                    elist.append((self.edges[(u,v)], u, v))
        elist.sort()
        print("******************************")
        for e in elist:
            print(e)
        print("******************************")
        for i, e in enumerate(elist):
            if i >= len(elist) - 1: break 
            if e[0] == elist[i+1][0]:
            #if elist.count(e) > 1:
                print("e: ", e, "  e+1: ", elist[i+1])
                    
    def edgelist(self, start, end):
        elist = []
        for i, u in enumerate(self.vertices):
            for j, v in enumerate(self.vertices):
                if (u, v) in self.edges:
                    si = str(i)
                    sj = str(j)
                    if u == start: si = "S"
                    if v == end: sj = "E"
                    elist.append((si, sj))
        return elist

    def  print(self, edges = True):
        for i1, v1 in enumerate(self.vertices):
            for i2, v2 in enumerate(self.vertices):
                if v1 == v2: continue
                if (v1,v2) in self.edges:
                    if (edges):
                        print(v1, "[", self.vertIDs[i1],"] --> ", 
                              v2, "[", self.vertIDs[i2],"] : ", self.edges[(v1,v2)])
                    else:
                        print("(", i1, ",", i2, ",", self.edges[(v1,v2)], "),")
   
    def isAvert(self, pt):
        return pt in self.vertices

    def getmindistance(self, start, stop):
        if not self.isAvert(start):
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if not self.isAvert(stop):
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

    def getVertID(self, pt):
        for i, vpt in enumerate(self.vertices):
            if vpt == pt: return i
        return -1

    def getmaxdistance(self, start, stop):
        start_id = self.getVertID(start)
        stop_id = self.getVertID(stop)
        
        maxdist = 0
        if start_id < 0:
            print("ERROR - Starting point ", start, " is not a vertex")
            return -1
        if stop_id < 0:
            print("ERROR - End point ", stop, " is not a vertex")
            return -1
        edges = np.zeros((len(self.vertices),len(self.vertices)), dtype = int)
        for i, n in enumerate(self.vertices):
            for j, m in enumerate(self.vertices):
                if (n,m) in self.edges:
                    edges[i][j] = self.edges[(n,m)]

        if self.debug: print(edges)
        vis = [False] * len(self.vertices)
        
        #q = deque()
        use_heap = False
        q = []
        dist = 0
        vis = [False] * len(self.vertices)
           #heap.heappush(q, (i, visc))
        #for j in range(len(self.vertices)):
        v = copy.deepcopy(vis)
        v[start_id] = True
        if (use_heap):
            heap.heappush(q, (start_id, v, 0))
        else:
            q.append((start_id, v, 0))
        self.debug = False
        while q:
            if use_heap:
                current, visited, curdist = heap.heappop(q)
            else:
                current, visited, curdist = q.pop()  
            if current == stop_id:
                if maxdist < curdist:
                    if (self.debug): print("XXXX - maxDist: ", maxdist, "  newDist: ", curdist, len(q))
                    maxdist = curdist
            else:
                if (self.debug) : print("Current index: ", current, " ", curdist)
                for i, adjNode in enumerate(self.vertices):
                    if i == current : continue
                    if visited[i] : continue
                    edge = edges[current][i]
                    if edge == 0: continue
                    if (self.debug) : print(i, adjNode)
                    newDist = curdist + edges[current][i]
                    if (self.debug) : print("***", current, " -> ", adjNode, " == ", newDist)
                    v = copy.deepcopy(visited)
                    v[i] = True
                    if use_heap:
                        heap.heappush(q, (i, v, newDist))
                    else:
                        q.append((i, v, newDist))
        return maxdist

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

def getTree(start, d, directed = True):
    seen = set()
    g = Graph(directed)
    starters = [[start, d]]
    finalStep = (gridRow-1, gridCol-2)
    trueStart = True
    while starters:
        start, d = starters.pop()
        npt = (start[0] + DIRlist[d][0], start[1] + DIRlist[d][1])
        if not trueStart and not d == grid[npt]:
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
            if len(s) == 0: break
            steps += 1
            if steps == 1: endpath = False
            curStep = s[0][0]
            d = s[0][1]
            if curStep == finalStep:
                if not ((start, s[0][0])) in seen:
                    g.addedge(start, s[0][0], steps)
                    seen.add((start, s[0][0]))
                done = True
            if endpath:
                a, b = nextSteps(curStep, d)
                if not ((start, b[0][0])) in seen:
                    g.addedge(start, b[0][0], steps+1)
                    seen.add((start, b[0][0]))
                for n in [RIGHT, DOWN, LEFT, UP]:
                    if n == (b[0][1] + 2) % 4: continue ## cannot reverse direction
                    starters.append([b[0][0], n])
                done = True
    return g

def getGraph(filename, directed):
    global gridRow
    global gridCol    
    gridRow = 0
    gridCol = 0
    
    for line in open(filename, 'r'):
        process(line)
    ng = getTree((0,1), DOWN, directed)
    return ng



ng = getGraph("data.txt", True)
endPoint = (gridRow-1,gridCol-2)

print("Part 1: Longest walk is ", ng.getmaxdistance((0, 1), endPoint))

xg = getGraph("data.txt", True)
endPoint = (gridRow-1,gridCol-2)
xg.part2()

print("Part 2: Longest walk is ", xg.getmaxdistance((0, 1), endPoint))

'''
xg = getGraph("data.txt", True)
endPoint = (gridRow-1,gridCol-2)
xg.part2()
print("Part2; Get max distance: ", xg.getmaxdistance((0, 1), endPoint))
# 5010 is too low
# 6484 is too low - i entered the wrong number

#xg.negate()
#xg.print()
#xg.merge()
#xg.debug = True
#
# test.txt - should be 154
#
#print("Get plus max distance: ", xg.getmindistance((0, 1), endPoint))


import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
edge_vec = xg.edgelist((0,1), endPoint)
new_ev = []

G.add_edges_from(edge_vec)

#val_map = {'A': 1.0,
#           'D': 0.5714285714285714,
#           'H': 0.0}

#values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
# red_edges = [('A', 'C'), ('E', 'C')]
# edge_colours = ['black' if not edge in red_edges else 'red'
#                for edge in G.edges()]
# black_edges = [edge for edge in G.edges()] # if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),  node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=True)
#nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.show()

'''
