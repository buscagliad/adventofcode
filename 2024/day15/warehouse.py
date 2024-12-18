'''

--- Day 15: Warehouse Woes ---
You appear back inside your own mini submarine! Each Historian drives their mini submarine in a different direction; maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they seem quite anxious, so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated by robots!

These lanternfish seem so anxious because they have lost control of the robot that operates one of their most important warehouses! It is currently running amok, pushing around boxes in the warehouse with no regard for lanternfish logistics or lanternfish inventory management strategies.

Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they could shut it off. However, if you could anticipate the robot's movements, maybe they could find a safe option.

The lanternfish already have a map of the warehouse and a list of movements the robot will attempt to make (your puzzle input). The problem is that the movements will sometimes fail as boxes are shifted around, making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes. However, if this action would cause the robot or a box to move into a wall (#), nothing moves instead, including the robot. The initial positions of these are shown on the map at the top of the document the lanternfish gave you.

The rest of the document describes the moves (^ for up, v for down, < for left, > for right) that the robot will attempt to make, in order. (The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########
The larger example has many more moves; after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
The lanternfish use their own custom Goods Positioning System (GPS for short) to track the locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map. (This process does not stop at wall tiles; measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......
The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes' GPS coordinates?

Your puzzle answer was 1463715.

The first half of this puzzle is complete! It provides one gold star: *

'''


EMPTY='.'
EID=0
BOXES='O'
BID=1
ROBOT='@'
RID=2
WALL='#'
WID=3

def chid(c):
    if c == EMPTY: return EID
    if c == BOXES: return BID
    if c == ROBOT: return RID
    if c == WALL: return WID
    return -1

def idch(c):
    if c == EID : return EMPTY
    if c == BID : return BOXES
    if c == RID : return ROBOT
    if c == WID : return WALL
    return -1

UP='^'
DOWN='v'
LEFT='<'
RIGHT='>'

deltas={}
deltas[UP] = [0,-1]
deltas[DOWN] = [0,1]
deltas[LEFT] = [-1,0]
deltas[RIGHT] = [1, 0]

Rpos = [0,0]

import numpy as np

grid = np.zeros([150,150], dtype = int)

ymax = 0
xmax = 0

def valid(x,y):
    if x < 0 or x >= xmax: return False
    if y < 0 or y >= ymax: return False
    return True

def processGrid(line):
    global grid, xmax, ymax, Rpos

    xmax = max(xmax, len(line.strip()))
    for i, a in enumerate(line.strip()):
        h = chid(a)
        if h == RID:
            grid[i][ymax] = RID
            Rpos = [i, ymax]
            # print(Rpos)
        else:
            grid[i][ymax] = h
 
    ymax += 1

def posadd(p, d):
    return [p[0]+d[0], p[1]+d[1]]
    
def possub(p, d):
    return [p[0]-d[0], p[1]-d[1]]
    
def moveboxes(r, d):
    global grid
    cboxes = 0
    p = posadd(r, d)
    sp = p
    while grid[p[0]][p[1]] == BID:
        cboxes += 1
        p = posadd(p,d)
    # print("cboxes: ", cboxes, " Pos: ", p, "  grid: ", grid[p[0]][p[1]])
    if grid[p[0]][p[1]] == EID:
        grid[p[0]][p[1]] = BID
        grid[sp[0]][sp[1]] = RID
        grid[r[0]][r[1]] = EID
        return True
    return False


def moveRobot(a):
    global Rpos, grid
    delta = deltas[a]
    npos = posadd(Rpos, delta)
    # print(a," Robot moves from: ", Rpos, " To: ", npos, "  Delta: ", delta, " Grid: ", grid[npos[0]][npos[1]])
    if grid[npos[0]][npos[1]] == EID:
        grid[Rpos[0]][Rpos[1]] = EID
        Rpos = npos
        grid[Rpos[0]][Rpos[1]] = RID
    elif grid[npos[0]][npos[1]] == BID:
        if moveboxes(Rpos, delta):
            Rpos[0] = npos[0]
            Rpos[1] = npos[1]
    

def processMoves(line):
    for a in line.strip():
        moveRobot(a)
        # pgrid()

def pgrid():
    global grid, ymax, xmax
    for y in range(ymax):
        for x in range(xmax):
            if (x,y) == Rpos: print('@', end="")
            else: print(idch(grid[x][y]), end="")
        print()
        
Pgrid = True
for l in open('data.txt'):
    if len(l) < 3: Pgrid = False
    if Pgrid:
        processGrid(l)
    else:
        # print("Rpos: ", Rpos)
        processMoves(l)

def gps():
    global grid, xmax, ymax
    gsum = 0
    for y in range(ymax):
        for x in range(xmax):
            if grid[x][y] == BID:
                gsum += 100 * y + x
    return gsum

#pgrid()

print("Part1: gps coord sum: ", gps())
