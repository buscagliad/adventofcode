'''

--- Day 20: Race Condition ---

The Historians are quite pixelated again. This time, a massive, black building looms over you - you're right outside the CPU!

While The Historians get to work, a nearby program sees that you're idle and challenges you to a race. Apparently, you've arrived just in time for the frequently-held race condition festival!

The race takes place on a particularly long and twisting code path; programs compete to see who can finish in the fewest picoseconds. The winner even gets their very own mutex!

They hand you a map of the racetrack (your puzzle input). For example:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

The map consists of track (.) - including the start (S) and end (E) positions (both of which also count as track) - and walls (#).

When a program runs through the racetrack, it starts at the start position. Then, it is allowed to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the end position as quickly as possible. In this example racetrack, the fastest time is 84 picoseconds.

Because there is only a single path from the start to the end and the programs all go the same speed, the races used to be pretty boring. To make things more interesting, they introduced a new rule to the races: programs are allowed to cheat.

The rules for cheating are very strict. Exactly once during a race, a program may disable collision for up to 2 picoseconds. This allows the program to pass through walls as if they were regular track. At the end of the cheat, the program must be back on normal track again; otherwise, it will receive a segmentation fault and get disqualified.

So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...12....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...12..#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

This cheat saves 38 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.####1##.###
#...###.2.#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

This cheat saves 64 picoseconds and takes the program directly to the end:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..21...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Each cheat has a distinct start position (the position where the cheat is activated, just before the first move that is allowed to go through walls) and end position; cheats are uniquely identified by their start position and end position.

In this example, the total number of cheats (grouped by the amount of time they save) are as follows:

    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.

You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible, you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?

Your puzzle answer was 1365.
--- Part Two ---

The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts at most 20 picoseconds.

Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats are possible. This six-picosecond cheat saves 76 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#1#####.#.#.###
#2#####.#.#...#
#3#####.#.###.#
#456.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Because this cheat has the same start and end positions as the one above, it's the same cheat, even though the path taken during the cheat is different:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S12..#.#.#...#
###3###.#.#.###
###4###.#.#...#
###5###.#.###.#
###6.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############

Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track). Any cheat time not used is lost; it can't be saved for another cheat later.

You'll still need a list of the best cheats, but now there are even more to choose between. Here are the quantities of cheats in this example that save 50 picoseconds or more:

    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.

Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?

Your puzzle answer was 986082.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
###
###
import numpy as np
import copy as cp
import heapq
from collections import deque
from collections import Counter

maize = np.zeros([150,150],dtype=int)
paths = np.zeros([150,150],dtype=int)
xmax = 0
ymax = 0
Epos = None
Spos = None

East = (1,0)
South = (0,1)
West = (-1,0)
North = (0,-1)
DELTAS = [East,South,West,North]

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
        if len(l) < 2: continue
        xmax = max(xmax, len(l.strip()))
        for j, a in enumerate(l.strip()):
            if a == 'S':
                Spos = (j, ymax)
            elif a == 'E':
                Epos = (j, ymax)
            elif a == '#':
                maize[j][ymax] = 1
        ymax += 1

        # position, direction, cost
#q = [(Spos, East, 0),(Spos, North, 1000)]
memo = np.zeros([150,150],dtype=int)
def findmin(start, end, pv):
    global memo
    q = deque()
    q.append((start, 0))
    n = 100
    found = False
    bestCost = 10000000000000
    if pv > 0: bestCost = pv
    while q:
        #n = n - 1
        (p, c) = q.popleft()
        #print("p", p, "  d", d, "  c", c, "  Epos", Epos)
        #print(p,d,c)
        if memo[p[0]][p[1]] == 0:
            memo[p[0]][p[1]] = c
        elif c > memo[p[0]][p[1]]: continue
        if p[0] == end[0] and p[1] == end[1]:
            found = True
            bestCost = min(bestCost, c)
            #print("Found path: ", c, flush=True)
            #print(p, c, path)
            continue
        for dirs in DELTAS:
            x = p[0]+dirs[0]
            y = p[1]+dirs[1]
            if not valid((x,y)): 
                #print(p, " is not valid")
                continue
            q.append(((x,y), c+1))
    if not found: return -1
    return bestCost

process("data.txt")

MV = findmin(Epos, Spos, 0)
#print("Shortest path is: ", MV)

x = 1
y = 1
cnt = Counter()
seq = []
for x in range(1,xmax-1):
    for y in range(1,ymax-1):
        if x == Epos[0] and y == Epos[1]: continue
        if maize[x][y] == 1: continue
        # mv = findmin((x,y), 0)
        mv = memo[x][y]
        paths[x][y] = mv
        #print("Min path of ", mv, " at ", x, y, flush=True)
if False:
    for y in range(ymax):
        for x in range(xmax):
            print(paths[x][y],",", end="", sep="")
        print()

def oldcheats():
    for x in range(1,xmax-1):
        for y in range(1,ymax-1):
            here = paths[x][y]
            if here == -1: continue
            if maize[x][y] == 1: 
                msv = 0
                svud = 0
                svlr = 0
                if (maize[x-1][y] == 0 and x-1 > 0 and
                    maize[x+1][y] == 0 and x+1 < xmax ):
                    lp = paths[x-1][y]
                    rp = paths[x+1][y]
                    if lp >= 0 and rp >= 0: svlr = abs(lp-rp)-2
                if (maize[x][y-1] == 0  and y-1 > 0 and 
                    maize[x][y+1] == 0  and y+1 < ymax ):
                    up = paths[x][y-1]
                    dp = paths[x][y+1]
                    if up >= 0 and dp >= 0: svud = abs(up-dp)-2
                msv = max(svud,svlr)
                if msv > 0:
                    seq.append(msv)
                    #print("Cheat found at: ", x+1,y+1, maize[x][y], " saving ", msv)

def cheats(max_cheats):
    cheat_actions=[]
    n_cheat = max_cheats
    for sx in range(1,xmax-1):
        for sy in range(1,ymax-1):
            here = paths[x][y]
            if maize[sx][sy] == 1: continue
            if here == -1: continue

            for dx in range(-n_cheat, n_cheat+1):
                for dy in range(-n_cheat, n_cheat+1):
                    cheat_distance = abs(dx) + abs(dy)
                    if cheat_distance > n_cheat: continue
                    ex = sx + dx
                    ey = sy + dy
                    if ex < 1 or ex > xmax-1: continue
                    if ey < 1 or ey > ymax-1: continue
                    if maize[ex][ey] == 1: continue
                        
                    # we must start and stop on a clean spot (i.e. maize=0)
                    if (maize[sx][sy] == 0 and maize[ex][ey] == 0):
                        scnt = paths[sx][sy]
                        ecnt = paths[ex][ey]
                        if scnt >= 0 and ecnt >= 0: 
                            save = scnt-ecnt-cheat_distance
                            if save >= 100:
                                cheat_actions.append(save)
                                #print("Cheat found from: ", sx,sy, " to ", ex,ey, " saving ", save)
    return cheat_actions

reqd_save = 100
p1seq = cheats(2)
p1cc = Counter(p1seq)
part1 = 0
for (picos, cnt) in sorted(p1cc.items()):
    part1 += cnt
print("Part 1: There are ", part1, " cheats that save ", reqd_save, " picoseconds.")

p2seq = cheats(20)
p2cc = Counter(p2seq)
part2 = 0
for (picos, cnt) in sorted(p2cc.items()):
    part2 += cnt
    #print("There are ", cnt//2, " cheats that save ", picos, " picoseconds.")
   # if picos >= reqd_save: num += cnt
   # mpico = max(picos, mpico)
print("Part 2: There are ", part2, " cheats that save ", reqd_save, " picoseconds.")
#print("Max pico: ", mpico)
