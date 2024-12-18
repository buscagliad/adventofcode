'''
--- Day 18: RAM Run ---

You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0

Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....

You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO

Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?

Your puzzle answer was 338.
--- Part Two ---

The Historians aren't as used to moving around in this pixelated universe as you are. You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.

To determine how fast everyone needs to go, you need to determine the first byte that will cut off the path to the exit.

In the above example, after the byte at 1,1 falls, there is still a path to the exit:

O..#OOO
O##OO#O
O#OO#OO
OOO#OO#
###OO##
.##O###
#.#OOOO

However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

...#...
.##..##
.#..#..
...#..#
###..##
.##.###
#.#....

So, in this example, the coordinates of the first byte that prevents the exit from being reachable are 6,1.

Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates of the first byte that will prevent the exit from being reachable from your starting position? (Provide the answer as two integers separated by a comma with no other characters.)

Your puzzle answer was 20,44.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import numpy as np
import heapq as heap

grid = np.zeros([71,71], dtype = int)
xmax = 70
ymax = 70
fbytes=[]

def valid(x, y):
    global grid
    if x < 0 or y < 0: return False
    if x > xmax or y > ymax: return False
    if grid[x][y] == -1: return False
    return True
    
def process(fn):
    global grid, xmax, ymax
    lc = 0
    for l in open(fn):
        lc += 1
        w = l.strip().split(",")
        x = int(w[0])
        y = int(w[1])
        fbytes.append((x,y))

def fillgrid(n):
    global grid
    for i in range(n):
        (x,y) = fbytes[i]
        grid[x][y] = -1

def addgrid(n):
    global grid
    (x,y) = fbytes[n]
    grid[x][y] = -1

def pgrid():
    global grid, xmax, xmin
    for y in range(0, ymax+1):
        for x in range(0, xmax+1):
            if grid[x][y] == -1: print('#', end = "")
            else: print('.', end = "")
        print()

def test():
    global grid, xmax, ymax
    xmax = 6
    ymax = 6
    process('test.txt', 12)
    pgrid()


def part1():
    global grid, xmax, ymax
    xmax = 70
    ymax = 70
    process('data.txt')
    fillgrid(1024)
    return travel((xmax,ymax))

def travel(stop):
    visited = np.zeros([71,71], dtype = int)
    q = []
    q.append((0,1,1))
    q.append((1,0,1))
    minsteps = 1000000000
    while q:
        (x,y,steps) = q.pop()
        if (x,y) == stop: 
            #print((x,y), stop, "  steps: ", steps)
            minsteps = min(steps, minsteps)
        if not valid(x,y): continue
        if visited[x][y] == 0:
            visited[x][y] = 1
        elif visited[x][y] <= steps: continue
        visited[x][y] = steps
        q.append((x-1,y,steps+1))
        q.append((x+1,y,steps+1))
        q.append((x,y-1,steps+1))
        q.append((x,y+1,steps+1))
    if minsteps > 10000: return -1
    return minsteps


def clear():
    global grid, xmax, ymax
    for x in range(xmax+1):
        for y in range(ymax+1):
            grid[x][y] = 0

print("Part 1: minimum number of steps: ", part1())

process('data.txt')

for n in range(len(fbytes), 1024, -1):
    clear()
    fillgrid(n)
    steps = travel((70,70))
    if steps > 0:
        # then n was the byte that forced things to be stuck
        print("Part 2: byte that gummed it up: ", fbytes[n], " took: ", steps)
        break
