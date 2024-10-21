'''
--- Day 20: A Regular Map ---

While you were learning about instruction pointers, the Elves made considerable progress. When you look up, you discover that the North Pole base construction project has completely surrounded you.

The area you are in is made up entirely of rooms and doors. The rooms are arranged in a grid, and rooms only connect to adjacent rooms when a door is present between them.

For example, drawing rooms as ., walls as #, doors as | or -, your current position as X, and where north is up, the area you're in might look like this:

#####
#.|.#
#-###
#.|X#
#####

You get the attention of a passing construction Elf and ask for a map. "I don't have time to draw out a map of this place - it's huge. Instead, I can give you directions to every room in the facility!" He writes down some directions on a piece of parchment and runs off. In the example above, the instructions might have been ^WNE$, a regular expression or "regex" (your puzzle input).

The regex matches routes (like WNE for "west, north, east") that will take you from your current room through various doors in the facility. In aggregate, the routes will take you through every door in the facility at least once; mapping out all of these routes will let you build a proper map and find your way around.

^ and $ are at the beginning and end of your regex; these just mean that the regex doesn't match anything outside the routes it describes. (Specifically, ^ matches the start of the route, and $ matches the end of it.) These characters will not appear elsewhere in the regex.

The rest of the regex matches various sequences of the characters N (north), S (south), E (east), and W (west). In the example above, ^WNE$ matches only one route, WNE, which means you can move west, then north, then east from your current position. Sequences of letters like this always match that exact route in the same order.

Sometimes, the route can branch. A branch is given by a list of options separated by pipes (|) and wrapped in parentheses. So, ^N(E|W)N$ contains a branch: after going north, you must choose to go either east or west before finishing your route by going north again. By tracing out the possible routes after branching, you can determine where the doors are and, therefore, where the rooms are in the facility.

For example, consider this regex: ^ENWWW(NEEE|SSE(EE|N))$

This regex begins with ENWWW, which means that from your current position, all routes must begin by moving east, north, and then west three times, in that order. After this, there is a branch. Before you consider the branch, this is what you know about the map so far, with doors you aren't sure about marked with a ?:

#?#?#?#?#
?.|.|.|.?
#?#?#?#-#
    ?X|.?
    #?#?#

After this point, there is (NEEE|SSE(EE|N)). This gives you exactly two options: NEEE and SSE(EE|N). By following NEEE, the map now looks like this:

#?#?#?#?#
?.|.|.|.?
#-#?#?#?#
?.|.|.|.?
#?#?#?#-#
    ?X|.?
    #?#?#

Now, only SSE(EE|N) remains. Because it is in the same parenthesized group as NEEE, it starts from the same room NEEE started in. It states that starting from that point, there exist doors which will allow you to move south twice, then east; this ends up at another branch. After that, you can either move east twice or north once. This information fills in the rest of the doors:

#?#?#?#?#
?.|.|.|.?
#-#?#?#?#
?.|.|.|.?
#-#?#?#-#
?.?.?X|.?
#-#-#?#?#
?.|.|.|.?
#?#?#?#?#

Once you've followed all possible routes, you know the remaining unknown parts are all walls, producing a finished map of the facility:

#########
#.|.|.|.#
#-#######
#.|.|.|.#
#-#####-#
#.#.#X|.#
#-#-#####
#.|.|.|.#
#########

Sometimes, a list of options can have an empty option, like (NEWS|WNSE|). This means that routes at this point could effectively skip the options in parentheses and move on immediately. For example, consider this regex and the corresponding map:

^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$

###########
#.|.#.|.#.#
#-###-#-#-#
#.|.|.#.#.#
#-#####-#-#
#.#.#X|.#.#
#-#-#####-#
#.#.|.|.|.#
#-###-###-#
#.|.|.#.|.#
###########

This regex has one main route which, at three locations, can optionally include additional detours and be valid: (NEWS|), (WNSE|), and (SWEN|). Regardless of which option is taken, the route continues from the position it is left at after taking those steps. So, for example, this regex matches all of the following routes (and more that aren't listed here):

    ENNWSWWSSSEENEENNN
    ENNWSWWNEWSSSSEENEENNN
    ENNWSWWNEWSSSSEENEESWENNNN
    ENNWSWWSSSEENWNSEEENNN

By following the various routes the regex matches, a full map of all of the doors and rooms in the facility can be assembled.

To get a sense for the size of this facility, you'd like to determine which room is furthest from you: specifically, you would like to find the room for which the shortest path to that room would require passing through the most doors.

    In the first example (^WNE$), this would be the north-east corner 3 doors away.
    In the second example (^ENWWW(NEEE|SSE(EE|N))$), this would be the south-east corner 10 doors away.
    In the third example (^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$), this would be the north-east corner 18 doors away.

Here are a few more examples:

Regex: ^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
Furthest room requires passing 23 doors

#############
#.|.|.|.|.|.#
#-#####-###-#
#.#.|.#.#.#.#
#-#-###-#-#-#
#.#.#.|.#.|.#
#-#-#-#####-#
#.#.#.#X|.#.#
#-#-#-###-#-#
#.|.#.|.#.#.#
###-#-###-#-#
#.|.#.|.|.#.#
#############

Regex: ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
Furthest room requires passing 31 doors

###############
#.|.|.|.#.|.|.#
#-###-###-#-#-#
#.|.#.|.|.#.#.#
#-#########-#-#
#.#.|.|.|.|.#.#
#-#-#########-#
#.#.#.|X#.|.#.#
###-#-###-#-#-#
#.|.#.#.|.#.|.#
#-###-#####-###
#.|.#.|.|.#.#.#
#-#-#####-#-#-#
#.#.|.|.|.#.|.#
###############

What is the largest number of doors you would be required to pass through to reach a room? That is, find the room for which the shortest path from your starting location to that room would require passing through the most doors; what is the fewest doors you can pass through to reach it?



Your puzzle answer was 4432.
--- Part Two ---

Okay, so the facility is big.

How many rooms have a shortest path from your current location that pass through at least 1000 doors?

Your puzzle answer was 8681.

Both parts of this puzzle are complete! They provide two gold stars: **



'''

import numpy as np

MAXD = 1000
centerX = MAXD//2
centerY = MAXD//2
curx = MAXD//2
cury = MAXD//2

grid = np.zeros((MAXD,MAXD), dtype = int)
doors = np.zeros((MAXD,MAXD), dtype = int)
ulx = MAXD//2
uly = MAXD//2
lrx = MAXD//2
lry = MAXD//2

EMPTY = 0
WALL = 1
ROOM = 2
DOOR = 3
DOOR_V = 3
DOOR_H = 4
CUR_LOC = 5

MARKS=[' ', '#', '.', '|', '-', 'X']

def fill():
    global grid, ulx, uly, lrx, lry
    ulx -= 1
    uly -= 1
    lrx += 1
    lry += 1
    for x in range(ulx , lrx + 1):
        for y in range(uly, lry + 1):
            if grid[x][y] == 0: grid[x][y] = WALL

    
def mapit(mp, ix, iy, sn, ndoors):
    global grid, ulx, uly, lrx, lry, doors
    ox = ix
    oy = iy
    odoors = ndoors
    (x,y,n) = (ix,iy,sn)
    #print("mapit: ", x, y, n, mp[sn:])
    while True:
        #print(mp[n], end="", sep="")
        dx = 0
        dy = 0
        if mp[n] == '$':
            return
        elif mp[n] == '^':
            grid[x][y] = CUR_LOC
            n += 1
            continue
        elif mp[n] == '(':
            n += 1
            x, y, n, ndoors = mapit(mp, x, y, n, ndoors)
            continue
        elif mp[n] == ')':
            #print("x/y: ", x, y)
            n += 1
            return ox, oy, n, ndoors
        elif mp[n] == '|':
            #mapit(mp, ox, oy, n+1)
            x = ox
            y = oy
            ndoors = odoors
            n += 1
            continue
        elif mp[n] == 'N':
            dy = -1
        elif mp[n] == 'W':
            dx = -1
        elif mp[n] == 'E':
            dx = 1
        elif mp[n] == 'S':
            dy = 1
        ndoors += 1
        x += dx
        y += dy
        grid[x][y] = DOOR
        x += dx
        y += dy
        grid[x][y] = ROOM
        if doors[x][y] == 0:
            doors[x][y] = ndoors
        elif doors[x][y] > ndoors:
            doors[x][y] = ndoors
            
        ulx = min(x, ulx)
        uly = min(y, uly)
        lrx = max(x, lrx)
        lry = max(y, lry)
        n += 1


def outmap():
    last = 0
    grid[centerX][centerY] = CUR_LOC
    for y in range(uly, lry+1):
        for x in range(ulx, lrx+1):
            cur = grid[x][y]
            if cur == EMPTY: continue
            mark = ' '
            if cur == DOOR:
                if last == WALL:
                    mark = MARKS[DOOR_H]
                else:
                    mark = MARKS[DOOR_V]
            else:
                mark = MARKS[cur]
            print(mark, sep="", end="")
            last = cur
        print()


test1 = "^ENWWW(NEEE|SSE(EE|N))$"     
test2 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
test3 = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
test4 = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

test = test4

#mapit(test, 500, 500, 0, 0)
for t in open("data.txt"):
    mapit(t, 500, 500, 0, 0)
#mapit(test, 500, 500, 0)

fill()

#outmap()

part1 = 0
part2 = 0
for x in range(ulx, lrx):
    for y in range(uly, lry):
        dxy = doors[x][y]
        if dxy > part1:
            part1 = dxy
        if dxy >= 1000:
            part2 += 1
#print(test)
print("Part1:  largest number of doors to pass thru is: ", part1)
print("Part2:  number of rooms requiring at least 1000 doors to pass: ", part2)
