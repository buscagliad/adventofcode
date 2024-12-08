'''

--- Day 8: Resonant Collinearity ---

You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........

Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........

Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........

The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.

Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

Your puzzle answer was 261.
--- Part Two ---

Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?

Your puzzle answer was 898.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import numpy as np
import copy as cp
grid = np.zeros([130,130], dtype = int)
anodes = np.zeros([130,130], dtype = int)
ymax = 0
xmax = 0
ulist = {}

def valid(x, y):
    if x < 0 or y < 0: return False
    if x >= xmax or y >= ymax: return False
    return True

def addanode(node, x,y):
    if not valid(x,y): return
    node[x][y] = 1

def process(line):
    global grid, xmax, ymax

    xmax = max(xmax, len(line.strip()))
    for i, a in enumerate(line.strip()):
        if a == '.': grid[i][ymax] = 0
        else: 
            if a in ulist:
                ulist[a].append([i, ymax])
            else:
                ulist[a] = [[i,ymax]]
    ymax += 1

for line in open('data.txt'):
    process(line)

def dist(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

#print(ulist)
for a in ulist:
    for i, [x1,y1] in enumerate(ulist[a]):
        for x2,y2 in ulist[a][i+1:]:
            dx = (x1 - x2)
            dy = (y1 - y2)
            x0 = x1 + dx
            y0 = y1 + dy
            x3 = x2 - dx
            y3 = y2 - dy
            
            addanode(anodes, x0, y0)
            addanode(anodes, x3, y3)
            
print("Part 1: Number of unique antinodes: ", sum(sum(anodes)))

#
# part 2:
#
bnodes = np.zeros([130,130], dtype = int)

for a in ulist:
    for i, [x1,y1] in enumerate(ulist[a]):
        for x2,y2 in ulist[a][i+1:]:
            dx = (x1 - x2)
            dy = (y1 - y2)
            x = x1
            y = y1
            while valid(x, y):
                addanode(bnodes, x, y)
                x = x + dx
                y = y + dy
            x = x2
            y = y2
            while valid(x, y):
                addanode(bnodes, x, y)
                x = x - dx
                y = y - dy

print("Part 2: Number of unique antinodes: ", sum(sum(bnodes)))
