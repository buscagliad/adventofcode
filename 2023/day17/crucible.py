
import numpy as np
from collections import defaultdict
import heapq as heap

MAXX=200
MAXY=200

grid = np.zeros([MAXX,MAXY], dtype = int)
gridCol = 0
gridRow = 0

def badDir(rdir, lastdir):
	if lastdir == rdir: return True
	if lastdir == (rdir + 2) % 4: return True
	return False


##
## for this problem, we need to define a 'node'
##
## a node will be and x,y index, and the direction used
## from that node - only left/right will be allowed
## as we will be inserting all maxp nodes in the same direction
## (both for right and left)
##
#            RIGHT    DOWN     LEFT    UP    
DIRlist  = [( 0, 1), (1, 0), (0, -1), (-1, 0) ]


START = -1
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def getDir(d):
	return DIRlist[d]

#
# only add paths for minp thru maxp 
# in the chosen direction
#
def getNodes(node, grid, minp, maxp):
	i = node[0]
	j = node[1]
	d = node[2] 
	# new direction must be left or right of d
	# if d == UP or DOWN, nd is RIGHT or LEFT
	# if d == LEFT or RIGHT, nd is UP or DOWN
	rnodes = []
	for nd in range(4):
		if badDir(nd, d): continue
		ud, lr = getDir(nd)
		delta = 0	# will be sum of grid points in the chosen direction
		ni = i
		nj = j
		for path in range(1, maxp + 1):
			ni += ud
			if ni < 0 or ni >= gridRow: continue
			nj += lr
			if nj < 0 or nj >= gridCol: continue
			delta += grid[ni][nj]
			if path >= minp:
				#print("Adding node: ", ni, nj, nd)
				rnodes.append(((ni, nj, nd), delta))
	return rnodes

#
# stole this dijkstra implementation from here:
#  https://levelup.gitconnected.com/dijkstra-algorithm-in-python-8f0e75e3f16e
#
def dijkstra(G, minp, maxp):
	visited = set()
	pq = []   # the queue
	nodeCosts = defaultdict(lambda: float('inf'))
	startingNode = (0, 0, UP)	# This will queue a left/right progression
	heap.heappush(pq, (0, startingNode))
	nodeCosts[startingNode] = 0
	startingNode = (0, 0, RIGHT)	# This will queue an up/down progression
	heap.heappush(pq, (0, startingNode))
	nodeCosts[startingNode] = 0
	 
	while pq:
		# go greedily by always extending the shorter cost nodes first
		total, node = heap.heappop(pq)
		visited.add(node)
		if (node[0] ==  gridRow-1)  and (node[1] == gridCol-1) :
			return total
		for adjNode, weight in getNodes(node, grid, minp, maxp):
			if adjNode in visited:	continue
				
			newCost = nodeCosts[node] + weight
			if nodeCosts[adjNode] > newCost:
				#print("New cost for node: ", adjNode, " -> ", newCost)
				nodeCosts[adjNode] = newCost
				heap.heappush(pq, (newCost, adjNode))
		

gridRow = 0
for l in open("data.txt"):
	line = l.strip()
	if len(line) < 2: break
	gridCol = len(line)
	#print(l)
	i = 0
	for d in line:
		if d.isdigit():
			grid[gridRow][i] = int(d)
			i += 1
	gridRow += 1


print("Part 1: crucible min path is: ", dijkstra(grid, 1, 3))
print("Part 2: crucible min path is: ", dijkstra(grid, 4, 10))
