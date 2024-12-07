'''
--- Day 6: Guard Gallivant ---

The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

Your puzzle answer was 4663.
--- Part Two ---

While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

Your puzzle answer was 1530.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import numpy as np
import copy as cp
grid = np.zeros([1000,1000], dtype = int)
ymax = 0
xmax = 0

EMPTY = 0
VISITED = 1
VISITED_UP = 0x01
VISITED_RIGHT = 0x02
VISITED_DOWN = 0x04
VISITED_LEFT = 0x08
VISITS=[VISITED_UP, VISITED_RIGHT, VISITED_DOWN, VISITED_LEFT]
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

WALL = 0x10
GUARD = 0x20
V = ['.', 'X', '#', 'G']
UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIR = [UP, RIGHT, DOWN, LEFT]
DC = ['^', '>', 'v', '<']
gdir = -1
gpos = [0,0]
GUARD_START_X = 0
GUARD_START_Y = 0
GUARD_DIR = 0

blocks=[]

def pgrid():
    for y in range(ymax):
        for x in range(xmax):
            g = grid[x][y]
            if g == EMPTY: c = '.'
            elif g == VISITED_UP: c = '^'
            elif g == VISITED_RIGHT: c = '>'
            elif g == VISITED_DOWN: c = 'v'
            elif g == VISITED_LEFT: c = '<'
            elif g == WALL: c = '#'
            elif g == GUARD: c = '*'
            print(c, end="")
        print()
def isout():
    global gpos
    if gpos[0] < 0 or gpos[1] < 0: return True
    if gpos[0] >= xmax or gpos[1] >= ymax: return True
    return False

def process(line):
    global grid, xmax, ymax, gdur, gpos, gdir
    global GUARD_START_X, GUARD_START_Y, GUARD_DIR

    xmax = max(xmax, len(line.strip()))
    for i, a in enumerate(line.strip()):
        if a == '.': grid[i][ymax] = EMPTY
        elif a == '#': grid[i][ymax] = WALL
        else:   # ^v<>
            gdir = DC.index(a)
            gpos[0] = i
            gpos[1] = ymax
            GUARD_START_X = i
            GUARD_START_Y = ymax
            GUARD_DIR = gdir
            #print(gdir, gpos, a)
            grid[i][ymax] = VISITS[gdir]
    ymax += 1

for line in open('data.txt'):
    process(line)
    
saveg = cp.deepcopy(grid)

def viscount():
    c = 0
    for i in range(xmax):
        for j in range(ymax):
            if 0 < grid[i][j] < WALL: c += 1
    return c
    

def inc(p, a):
    x = DIR[a][0]
    y = DIR[a][1]
    n=[p[0]+x, p[1]+y]
    #print("INC", a, x, y, n)
    return n

def valid(x, y):
    if x < 0 or y < 0: return False
    if x >= xmax or y >= ymax: return False
    return True


#
def finddir(g, x, y, dx, dy, dirval):
    # if x+dx == GUARD_START_X and y+dy == GUARD_START_Y: 
   # print(x, dx, y, dy, "GUARD START", dirval)
        # return False    
    while valid(x,y):
        #
        # we get here if x,y is valid, then we hit a wall
        # which we will rotate right - the that direction matches
        # the direction already seen at this xy - then we have
        # a loop path
        #
        if g[x][y] == WALL:
            dirval = (dirval + 1) % 4
            x -= dx
            y -= dy
            dx = DIR[dirval][0]
            dy = DIR[dirval][1] 
        else:
            if g[x][y] & VISITS[dirval]: 
                return True
            g[x][y] |= VISITS[dirval]
            # print(x,y,dx,dy,dirval)
            # if g[x][y] != WALL:
            x += dx
            y += dy

    #print("RETURNING FALSE")
    return False

#p2_count = 0
while not isout():
    npos = inc(gpos, gdir)
    #print(npos)
    if grid[npos[0]][npos[1]] == WALL:
        gdir = (gdir + 1)% 4
        #print("Turning at ", npos)
        continue
    gpos = npos
    grid[gpos[0]][gpos[1]] |= VISITS[gdir]
    pg = grid[gpos[0]][gpos[1]]
    pr = False
    nnpos = inc(gpos, gdir)
    if nnpos == [GUARD_START_X, GUARD_START_Y]: 
        print("HEY", nnpos)
        continue

print("Part 1: total positions visited: ", viscount())

part2_count = 0
gsx = GUARD_START_X + DIR[GUARD_DIR][0]
gsy = GUARD_START_Y + DIR[GUARD_DIR][1]
for x in range(xmax):
    for y in range(ymax):
        p2 = cp.deepcopy(saveg)
        if p2[x][y] == WALL: continue
        if x == GUARD_START_X and y == GUARD_START_Y: continue
        p2[x][y] = WALL
        if finddir(p2, gsx, gsy, DIR[GUARD_DIR][0], DIR[GUARD_DIR][1], GUARD_DIR): part2_count += 1

print("Part 2: number of road blocks: ", part2_count, len(blocks))
# 339 is too low
# 471 is too low
# 1665 is too high
# 1664 is not correct
# 1605 is not correct
