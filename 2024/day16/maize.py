'''
--- Day 16: Reindeer Maze ---

It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############

There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:


###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############

Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################

In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################

Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?

Your puzzle answer was 98416.
--- Part Two ---

Now that you know what the best paths look like, you can figure out the best spot to sit.

Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile. While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view, etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit somewhere else, you'd miss all the action!

So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.

In the first example, there are 45 tiles (marked O) that are part of at least one of the various best paths through the maze:

###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############

In the second example, there are 64 tiles that are part of at least one of the best paths:

#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################

Analyze your map further. How many tiles are part of at least one of the best paths through the maze?

Your puzzle answer was 471.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
###
### VERY VERY SLOW TOOK 
###
### 1687.84user 10.11system 28:18.46elapsed 99%CPU (0avgtext+0avgdata 182388maxresident)k
###
###
import numpy as np
import copy as cp
import heapq
from collections import deque

maize = np.zeros([150,150],dtype=int)
xmax = 0
ymax = 0
Epos = None
Spos = None

East = (1,0)
South = (0,1)
West = (-1,0)
North = (0,-1)

def valid(p):
    global maize
    x = p[0]
    y = p[1]
    if x <= 0 or x >= xmax: 
        #print("valid: x = ", x)
        return False
    if y <= 0 or y >= ymax: 
        #print("valid: y = ", y)
        return False
    if maize[x][y] == 1: 
        #print("valid: maize[x][y] = ", maize[x][y])
        return False
    return True


def process(fn):
    global xmax, ymax, Epos, Spos, maize
    xmax = 0
    ymax = 0
    for l in open(fn):
        xmax = max(xmax, len(l.strip()))
        for j, a in enumerate(l.strip()):
            if a == 'S':
                Spos = (j, ymax)
            elif a == 'E':
                Epos = (j, ymax)
            elif a == '#':
                maize[j][ymax] = 1
        ymax += 1

score = set()
        # position, direction, cost
#q = [(Spos, East, 0),(Spos, North, 1000)]
def findmin(fn, pv):
    global score
    process(fn)
    q = deque()
    q.append((Spos, East, 0, [(Spos[0],Spos[1])]))
    track={}
    n = 100
    bestCost = 10000000000000
    if pv > 0: bestCost = pv
    while q:
        #n = n - 1
        (p, d, c, path) = q.popleft()
        if not valid(p): 
            #print(p, " is not valid")
            continue
        #print("p", p, "  d", d, "  c", c, "  Epos", Epos)
        if (p,d) not in track: 
            track[(p,d)] = c
        elif track[(p,d)] >= c: 
            track[(p,d)] = c
        else:
            continue
        
        #print(p,d,c)
        if c > bestCost: continue
        if p[0] == Epos[0] and p[1] == Epos[1]:
            bestCost = min(bestCost, c)
            #print("Found path: ", c)
            #print(p, c, path)
            for (x,y) in path:
                score.add((x,y))
            continue
        for dirs in [East,West,North,South]:
            #pp = cp.deepcopy(path)
            npath = cp.deepcopy(path)
            if dirs == d:
                adder = 1
            else:
                adder = 1001
            x = p[0]+dirs[0]
            y = p[1]+dirs[1]
            npath.append((x,y))
            q.append(((x,y), dirs, c+adder, npath))
    return bestCost

score.clear()
mv = findmin("data.txt", 0)
print("Part 1: minimum cost is: ", mv)
# 99416 is too high
score.clear()
p2 = findmin("data.txt", mv)
print("Part 2:  number of good seats is: ", len(score))
