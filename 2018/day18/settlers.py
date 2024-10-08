'''
--- Day 18: Settlers of The North Pole ---

On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a lumberyard (#). You take a scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely different. In exactly one minute, an open acre can fill with trees, a wooded acre can be converted to a lumberyard, or a lumberyard can be cleared to open ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded, or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent acres; the missing acres aren't counted.)

In particular:

    An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
    An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
    An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.

These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning of the minute and changing to their new form by the end of that same minute. Changes that happen during the minute don't affect each other.

For example, suppose the lumber collection area is instead only 10 by 10 acres with this initial configuration:

Initial state:
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||

After 10 minutes, there are 37 wooded acres and 31 lumberyards. Multiplying the number of wooded acres by the number of lumberyards gives the total resource value after ten minutes: 37 * 31 = 1147.

What will the total resource value of the lumber collection area be after 10 minutes?

Your puzzle answer was 394420.
--- Part Two ---

This important natural resource will need to last for at least thousands of years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?

Your puzzle answer was 174420.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

ACRES = 52  # surrounding edge is GROUND only

GROUND = 0
TREE = 1
YARD = 10

def item(n):
    if n == 0: return '.'
    if n == 1: return '|'
    if n == 10: return '#'
    return '@'
    

def outforest(f, rows, cols):
    for r in range(rows):
        for c in range(cols):
            print(item(f[r+1][c+1]), end="")
        print()
    print()


def countForest(f, rows, cols):
    nt = 0
    ny = 0
    for r in range(rows):
        for c in range(cols):
            if f[r+1][c+1] == TREE: nt += 1
            elif f[r+1][c+1] == YARD: ny += 1
    return nt, ny

import numpy as np

odd  = np.zeros((ACRES,ACRES), dtype = int)

#    An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
#    An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
#    An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.

def acreUpdate(forest, row, col):
    s = -forest[row][col]
    for r in range(row-1,row+2):
        for c in range(col-1, col+2):
            s += forest[r][c]
    num_trees = s % 10
    num_yards = s // 10
    num_ground = 8 - num_trees - num_yards
    #print("At ", row, col, "  Ground: ", num_ground, "   Trees: ", num_trees, "   Yards: ", num_yards)
    if forest[row][col] == GROUND:
        if num_trees >= 3:
            return TREE
        return GROUND
    elif forest[row][col] == TREE:
        if num_yards >= 3:
            return YARD
        return TREE
    elif forest[row][col] == YARD:
        if num_yards > 0 and num_trees > 0:
            return YARD
        return GROUND

def forestUpdate(forest, num_rows, num_cols):
    nf = np.zeros((ACRES,ACRES), dtype = int)
    for r in range(1, num_rows + 1):
        for c in range(1, num_cols + 1):
            nf[r][c] = acreUpdate(forest, r, c)
    return nf

def process(fname):
    even = np.zeros((ACRES,ACRES), dtype = int)
    row = 0
    for l in open(fname, "r"):
        col = 0
        for c in l.strip():
            # ground (.), trees (|), or a lumberyard (#)      
            if   c == '.': even[row+1][col+1] = GROUND
            elif c == '|': even[row+1][col+1] = TREE
            elif c == '#': even[row+1][col+1] = YARD
            else: print("ERROR")
            col += 1
        row += 1
    return row, col, even

num_rows, num_columns, forest = process("data.txt")

SIZE = 1000
res = []
R = 0
for i in range(SIZE):
    abc = forestUpdate(forest, num_rows, num_columns)
    forest = abc
    num_trees, num_yards = countForest(forest, num_rows, num_columns)
    prod = num_trees * num_yards
    if (i+1) == 10:
        p1_trees = num_trees
        p1_yards = num_yards
    if prod in res:
        index = res.index(prod)
        if R + 1 == index:
            # we have our sequence
            # print("Breaking at R: ", R, "  index: ", index, " i: ", i)
            break
        R = index
        #print("Product: ", prod, " at ", i, "  seen at ", R)
        N = i - res.index(prod)
    res.append(prod)

#print(res)

print("Part 1: number of trees: ", p1_trees, "  number of lumber yards: ", p1_yards, "  answer: ", p1_yards * p1_trees)

#
# Find first time the sequence begins to repeat
#   Say it happens at index R, and it goes for a length N
#   To find what value will occur and index Q, the following will be useful
#      K = Q - R
#      Value will be:  the number at R + K mod R
#
        
#    outforest(forest, num_rows, num_columns)
# 
# 179800 is too high
#
Q=1000000000
print("Part 2: Sequence starts at: ", R, " repeats every ", N, " value after ", Q, " minutes is: ", res[R - 1 + (Q - R) % N])
