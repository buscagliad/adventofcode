'''
--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls and related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that have been routed through the HVAC system. If you can direct it to each of those locations, you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant locations marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other numbers are (in no particular order) the locations the robot needs to visit at least once each. Walls are marked as #, and open passages are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps (in the above example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every non-0 number marked on the map at least once?

Your puzzle answer was 462.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and then return to 0?



Your puzzle answer was 462.
--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and then return to 0?

Your puzzle answer was 676.

Both parts of this puzzle are complete! They provide two gold stars: **

'''


import numpy as np
import heapq
from collections import deque
from itertools import permutations 

WALL = -1
PATH = 0

#grid = np.zero((200,200), dtype = int
grid = []
nodes = {}

numrows = 0
numcols = 0
start = None
UP = (-1,0)
RIGHT = (0,1)
DOWN = (1, 0)
LEFT = (-1, 0)


def did_visit(n, two):
    return (n & (1 << two)) != 0

def is_visiting(n, v):
    return n + (1 << v)

#
# create grid and list of nodes
def process(line):
    global grid, numrows, numcols, nodes
    if len(line) < 3: return
    thisrow = list(line.strip())
    numcols = len(thisrow)
    row = numrows
    col = 0
    for i, a in enumerate(thisrow):
        if a == '#' or a == '.':
            pass
        else:
            n = int(a)
            nodes[n] = (row,col)
            #print("Node: ", n, "  found at ", row, col)
            thisrow[i] = '.'
        col += 1
    grid.append(thisrow)
    numrows += 1


for line in open("data.txt", "r"):
    process(line)
#
# given a current location and the last visited location,
# look in all four directions to see if there is NO wall
# ignore the previous location's direction (UNLESS you are
# currently on a number fo the first time
#

def shortest_distance(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    
    # Define directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Queue for BFS
    queue = deque([(start, 0)])
    
    # Set to track visited cells
    visited = set([start])
    
    # BFS
    while queue:
        (x, y), distance = queue.popleft()
        
        if (x, y) == end:
            return distance
        
        # Explore neighbors
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == '.' and (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), distance + 1))
                visited.add((new_x, new_y))
    
    # If no path found
    return -1

dist={}
for i in range(len(nodes)):
    for j in range(len(nodes)):
        if i == j: 
            dist[(i,j)] = 0
            continue
        dist[(i,j)] = shortest_distance(grid, nodes[i], nodes[j])
        #print("From [", i, "]", nodes[i], " to [", j, "]", nodes[j], "  min distance: ", shortest_distance(grid, nodes[i], nodes[j]))

def computeroute(dist, indeces):
    route = 0
    start = 0
    for i, n in enumerate(indeces):
        route += dist[(start, indeces[i])]
        start = indeces[i]
    return route

mindist = 100000000
back2zero = 100000000
for x in permutations([1,2,3,4,5,6,7]):
    rval = computeroute(dist, x)
    #print(x, " --> ", rval)
    mindist = min(mindist, rval)
    b2z = rval + dist[(x[6], 0)]
    back2zero = min(b2z, back2zero)

print("Part 1: smallest number of steps: ", mindist)
print("Part 2: smallest number of steps from 0 and back: ", back2zero)
