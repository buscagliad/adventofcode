'''

--- Day 15: Beverage Bandits ---

Having perfected their hot chocolate, the Elves have a new problem: the Goblins that live in these caves will do anything to steal it. Looks like they're here for a fight.

You scan the area, generating a map of the walls (#), open cavern (.), and starting position of every Goblin (G) and Elf (E) (your puzzle input).

Combat proceeds in rounds; in each round, each unit that is still alive takes a turn, resolving all of its actions before the next unit's turn begins. On each unit's turn, it tries to move into range of an enemy (if it isn't already) and then attack (if it is in range).

All units are very disciplined and always follow very strict combat rules. Units never move or attack diagonally, as doing so would be dishonorable. When multiple choices are equally valid, ties are broken in reading order: top-to-bottom, then left-to-right. For instance, the order in which units take their turns within a round is the reading order of their starting positions in that round, regardless of the type of unit or whether other units have moved after the round started. For example:

                 would take their
These units:   turns in this order:
  #######           #######
  #.G.E.#           #.1.2.#
  #E.G.E#           #3.4.5#
  #.G.E.#           #.6.7.#
  #######           #######

Each unit begins its turn by identifying all possible targets (enemy units). If no targets remain, combat ends.

Then, the unit identifies all of the open squares (.) that are in range of each target; these are the squares which are adjacent (immediately up, down, left, or right) to any target and which aren't already occupied by a wall or another unit. Alternatively, the unit might already be in range of a target. If the unit is not already in range of a target, and there are no open squares which are in range of a target, the unit ends its turn.

If the unit is already in range of a target, it does not move, but continues its turn with an attack. Otherwise, since it is not in range of a target, it moves.

To move, the unit first considers the squares that are in range and determines which of those squares it could reach in the fewest steps. A step is a single movement to any adjacent (immediately up, down, left, or right) open (.) square. Units cannot move into walls or other units. The unit does this while considering the current positions of units and does not do any prediction about where units will be later. If the unit cannot reach (find an open path to) any of the squares that are in range, it ends its turn. If multiple squares are in range and tied for being reachable in the fewest steps, the square which is first in reading order is chosen. For example:

Targets:      In range:     Reachable:    Nearest:      Chosen:
#######       #######       #######       #######       #######
#E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
#...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
#.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
#######       #######       #######       #######       #######

In the above scenario, the Elf has three targets (the three Goblins):

    Each of the Goblins has open, adjacent squares which are in range (marked with a ? on the map).
    Of those squares, four are reachable (marked @); the other two (on the right) would require moving through a wall or unit to reach.
    Three of these reachable squares are nearest, requiring the fewest steps (only 2) to reach (marked !).
    Of those, the square which is first in reading order is chosen (+).

The unit then takes a single step toward the chosen square along the shortest path to that square. If multiple steps would put the unit equally closer to its destination, the unit chooses the step which is first in reading order. (This requires knowing when there is more than one shortest path so that you can consider the first step of each such path.) For example:

In range:     Nearest:      Chosen:       Distance:     Step:
#######       #######       #######       #######       #######
#.E...#       #.E...#       #.E...#       #4E212#       #..E..#
#...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
#..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
#######       #######       #######       #######       #######

The Elf sees three squares in range of a target (?), two of which are nearest (!), and so the first in reading order is chosen (+). Under "Distance", each open square is marked with its distance from the destination square; the two squares to which the Elf could move on this turn (down and to the right) are both equally good moves and would leave the Elf 2 steps from being in range of the Goblin. Because the step which is first in reading order is chosen, the Elf moves right one square.

Here's a larger example of movement:

Initially:
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

After 1 round:
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########

After 2 rounds:
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########

After 3 rounds:
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########

Once the Goblins and Elf reach the positions above, they all are either in range of a target or cannot find any square in range of a target, and so none of the units can move until a unit dies.

After moving (or if the unit began its turn in range of a target), the unit attacks.

To attack, the unit first determines all of the targets that are in range of it by being immediately adjacent to it. If there are no such targets, the unit ends its turn. Otherwise, the adjacent target with the fewest hit points is selected; in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.

The unit deals damage equal to its attack power to the selected target, reducing its hit points by that amount. If this reduces its hit points to 0 or fewer, the selected target dies: its square becomes . and it takes no further turns.

Each unit, either Goblin or Elf, has 3 attack power and starts with 200 hit points.

For example, suppose the only Elf is about to attack:

       HP:            HP:
G....  9       G....  9  
..G..  4       ..G..  4  
..EG.  2  -->  ..E..     
..G..  2       ..G..  2  
...G.  1       ...G.  1  

The "HP" column shows the hit points of the Goblin to the left in the corresponding row. The Elf is in range of three targets: the Goblin above it (with 4 hit points), the Goblin to its right (with 2 hit points), and the Goblin below it (also with 2 hit points). Because three targets are in range, the ones with the lowest hit points are selected: the two Goblins with 2 hit points each (one to the right of the Elf and one below the Elf). Of those, the Goblin first in reading order (the one to the right of the Elf) is selected. The selected Goblin's hit points (2) are reduced by the Elf's attack power (3), reducing its hit points to -1, killing it.

After attacking, the unit's turn ends. Regardless of how the unit's turn ends, the next unit in the round takes its turn. If all units have taken turns in this round, the round ends, and a new round begins.

The Elves look quite outnumbered. You need to determine the outcome of the battle: the number of full rounds that were completed (not counting the round in which combat ends) multiplied by the sum of the hit points of all remaining units at the moment combat ends. (Combat only ends when a unit finds no targets during its turn.)

Below is an entire sample combat. Next to each map, each row's units' hit points are listed from left to right.

Initially:
#######   
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#   
#######   

After 1 round:
#######   
#..G..#   G(200)
#...EG#   E(197), G(197)
#.#G#G#   G(200), G(197)
#...#E#   E(197)
#.....#   
#######   

After 2 rounds:
#######   
#...G.#   G(200)
#..GEG#   G(200), E(188), G(194)
#.#.#G#   G(194)
#...#E#   E(194)
#.....#   
#######   

Combat ensues; eventually, the top Elf dies:

After 23 rounds:
#######   
#...G.#   G(200)
#..G.G#   G(200), G(131)
#.#.#G#   G(131)
#...#E#   E(131)
#.....#   
#######   

After 24 rounds:
#######   
#..G..#   G(200)
#...G.#   G(131)
#.#G#G#   G(200), G(128)
#...#E#   E(128)
#.....#   
#######   

After 25 rounds:
#######   
#.G...#   G(200)
#..G..#   G(131)
#.#.#G#   G(125)
#..G#E#   G(200), E(125)
#.....#   
#######   

After 26 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(122)
#...#E#   E(122)
#..G..#   G(200)
#######   

After 27 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(119)
#...#E#   E(119)
#...G.#   G(200)
#######   

After 28 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(116)
#...#E#   E(113)
#....G#   G(200)
#######   

More combat ensues; eventually, the bottom Elf dies:

After 47 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(59)
#...#.#   
#....G#   G(200)
#######   

Before the 48th round can finish, the top-left Goblin finds that there are no targets remaining, and so combat ends. So, the number of full rounds that were completed is 47, and the sum of the hit points of all remaining units is 200+131+59+200 = 590. From these, the outcome of the battle is 47 * 590 = 27730.

Here are a few example summarized combats:

#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 982 total hit points left
Outcome: 37 * 982 = 36334

#######       #######   
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#   
#######       #######   

Combat ends after 46 full rounds
Elves win with 859 total hit points left
Outcome: 46 * 859 = 39514

#######       #######   
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#   
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######   

Combat ends after 35 full rounds
Goblins win with 793 total hit points left
Outcome: 35 * 793 = 27755

#######       #######   
#.E...#       #.....#   
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#   
#E#G#G#       #.#.#.#   
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######   

Combat ends after 54 full rounds
Goblins win with 536 total hit points left
Outcome: 54 * 536 = 28944

#########       #########   
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#   
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740

What is the outcome of the combat described in your puzzle input?

Your puzzle answer was 228240.
--- Part Two ---

According to your calculations, the Elves are going to lose badly. Surely, you won't mess up the timeline too much if you give them just a little advanced technology, right?

You need to make sure the Elves not only win, but also suffer no losses: even the death of a single Elf is unacceptable.

However, you can't go too far: larger changes will be more likely to permanently alter spacetime.

So, you need to find the outcome of the battle in which the Elves have the lowest integer attack power (at least 4) that allows them to win without a single death. The Goblins always have an attack power of 3.

In the first summarized example above, the lowest attack power the Elves need to win without losses is 15:

#######       #######
#.G...#       #..E..#   E(158)
#...EG#       #...E.#   E(14)
#.#.#G#  -->  #.#.#.#
#..G#E#       #...#.#
#.....#       #.....#
#######       #######

Combat ends after 29 full rounds
Elves win with 172 total hit points left
Outcome: 29 * 172 = 4988

In the second example above, the Elves need only 4 attack power:

#######       #######
#E..EG#       #.E.E.#   E(200), E(23)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##E#   E(125), E(200)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#
#######       #######

Combat ends after 33 full rounds
Elves win with 948 total hit points left
Outcome: 33 * 948 = 31284

In the third example above, the Elves need 15 attack power:

#######       #######
#E.G#.#       #.E.#.#   E(8)
#.#G..#       #.#E..#   E(86)
#G.#.G#  -->  #..#..#
#G..#.#       #...#.#
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 94 total hit points left
Outcome: 37 * 94 = 3478

In the fourth example above, the Elves need 12 attack power:

#######       #######
#.E...#       #...E.#   E(14)
#.#..G#       #.#..E#   E(152)
#.###.#  -->  #.###.#
#E#G#G#       #.#.#.#
#...#G#       #...#.#
#######       #######

Combat ends after 39 full rounds
Elves win with 166 total hit points left
Outcome: 39 * 166 = 6474

In the last example above, the lone Elf needs 34 attack power:

#########       #########   
#G......#       #.......#   
#.E.#...#       #.E.#...#   E(38)
#..##..G#       #..##...#   
#...##..#  -->  #...##..#   
#...#...#       #...#...#   
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   

Combat ends after 30 full rounds
Elves win with 38 total hit points left
Outcome: 30 * 38 = 1140

After increasing the Elves' attack power until it is just barely enough for them to win without any Elves dying, what is the outcome of the combat described in your puzzle input?

Your puzzle answer was 52626.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import numpy as np
from operator import itemgetter, attrgetter

from collections import deque

DEBUG = False
DEBUG1 = False
##
## globals
##
order = [(0, -1), (-1, 0), (1, 0), (0, 1)]
# attackorder = [(1, 0), (0, 1), (0, -1), (-1, 0)] 
attackorder = order
# test_shortest_path()
# exit()
units = []
field = np.zeros([50,50], dtype = int)
maxx = 0
maxy = 0
numunits = 0
numelf = 0
numgob = 0

def set_elf_attack(n):
    for u in units:
        if u.kind[0] == 'E':
            u.attackPower = n
#
# we modified the shortest path algorithm to return the 
# ending step direction
# that is use it as such:  shortest_pat(grid, end, start)
#
#
def shortest_path(grid, rows, cols, start, end):
    
    xi, yi = start
    xf, yf = end
    # print("shortest_path from: ", start, " to ", end, xi, yi, xf, yf, rows, cols)
    
    # Initialize the BFS queue
    queue = deque([(xi, yi, 0)])  # (x, y, steps)
    visited = set()
    visited.add((xi, yi))
        
    while queue:
        x, y, steps = queue.popleft()
        
        # Check if we have reached the end point
        if (x, y) == (xf, yf):
            return steps
        
        # Explore neighbors
        for dx, dy in order:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0: continue
            if nx >= cols or ny >= rows: continue
            if grid[nx][ny] != -1 and (nx,ny) != end: continue
            # print(nx,ny, steps)
            
            # Check if the neighbor is within bounds and walkable
            # modified to use -1 as a 'walkable' cell
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                queue.append((nx, ny, steps + 1))
                visited.add((nx, ny))
    
    # If we exhaust the queue without finding the end point
    return 0

#
# this function searches for all units of kind that are closest to the
# provided unit
#
def start_dir_w_distance(grid, rows, cols, unit):
    xi, yi = unit.x, unit.y
    kind = unit.kind
    sdx = 0
    sdy = 0
    minsp = -1
    us = getunits()
    for ou in us:
        if ou.kind == kind: continue
        if not ou.alive: continue
        xf = ou.x
        yf = ou.y
        # The actual start will be from one of the four possible starting spots awaya from 
        # start - which is the actual position of the unit
        # 
        for dx, dy in order:
            x = xi + dx
            y = yi + dy
            if x < 0 or y < 0: continue
            if x >= cols or y >= rows: continue
            if grid[x][y] != -1: continue
            sp = shortest_path(grid, maxx, maxy, (x,y), (xf,yf))
            if DEBUG: print("---For unit: ", unit.ID(), " at: (", unit.x, ",",  unit.y, 
                ")  To: (", ou.x, ",",  ou.y, ") sp: ", sp, " step is: ", dx, dy)
            if sp == 0: continue
            if minsp == -1 or sp < minsp:
                sdx = dx
                sdy = dy
                minsp = sp
    if DEBUG: print("For unit: ", unit.ix, " at: ", unit.POS(), "  sp: ", sp, " step is: ", sdx, sdy)
    return sdx, sdy, minsp
    

def test_shortest_path ():    
    # Example usage:
    grid = [
        [-1,  1, -1, -1, -1],
        [-1, -1, -1,  1, -1],
        [-1,  1, -1,  1, -1],
        [-1,  1, -1,  1, -1],
        [-1,  1, -1,  1, -1]
    ]

    start = (0, 0)
    end = (4, 4)
    print(shortest_path(grid, 5, 5, start, end))  # Output should be the number of steps or 0 if no path exists


def getunit(ix):
    global units
    for u in units:
        if u.ix == ix: return u
    return None


def getunits():
    global units, field
    ru = []
    for j in range(maxy):
        for i in range(maxx):
            if field[i][j] < 0: continue
            ru.append(units[field[i][j]])
    return ru
    
    
def gridout():
    global field, maxx, maxy
    for y in range(maxy):
        addtext = "  "
        for x in range(maxx):
            n = field[x][y]
            if n == -2: print("# ", end="")
            elif n == -1: print(". ", end="")
            else: 
                u = getunit(n)
                ch = u.kind[0]
                print(ch, u.ix, sep = "", end="")
                addtext += ch + str(u.ix) + "(" + str(u.hitPoints) + ")  "
        print(addtext)
    print()






class Unit:
    def __init__(self, x, y, t, ix):
        self.hitPoints = 200
        self.attackPower = 3
        self.x = x
        self.y = y
        self.kind = t
        self.alive = True
        self.jump = [0,0]
        self.ix = ix
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y
        

    def attack(self, other):
        global field, numgob, numelf, elves_lost_count
        other.hitPoints -= self.attackPower
        if other.hitPoints <= 0:
            if other.kind == "Gob":
                numgob -= 1
            if other.kind == "Elf":
                elves_lost_count += 1
                numelf -= 1
            if DEBUG1: print(other.ID(), " Killed at position: ", other.POS(), 
                ":: by ", self.ID(), " at ", self.POS())
            field[other.x][other.y] = -1
            
            other.alive = False
            
    def move(self, dx, dy):
        global field
        field[self.x][self.y] = -1
        self.x += dx
        self.y += dy
        field[self.x][self.y] = self.ix
        
    def out(self):
        print(self.kind, " at: ", self.POS(), "  hit points: ", 
                self.hitPoints)
                
    def ishere(self, x, y):
        if self.x == x and self.y == y: return True
        return False
    
    def canattack(self):
        global field, units
        x = self.x
        y = self.y
        at = []
        for (dx,dy) in attackorder:
            n = field[x+dx][y+dy]
            if n < 0: continue
            u = getunit(n)
            if u.kind == self.kind: continue
            at.append(u)
            #print("For ", self.ID(), " near ", u.ID())
        #
        # attack the one with the fewest hit points
        #
        ru = None
        rv = False
        minhp = 999999990
        for a in at:
            rv = True
            if not ru:
                ru = a
                minhp = a.hitPoints
            else:
                if minhp > a.hitPoints:
                    minhp = a.hitPoints
                    ru = a
                #elif minhp == a.hitPoints:
                #   print("ERROR at ", ru.ID())
        return rv, ru
    #
    # canmove will, if possible, move this unit toward its closest 'enemy'
    # however, a check is first made to determine if unit is already in range
    # if it moves, True is returned, if it cannot move, False is returned
    #
    def canmove(self):
        global field, units
        x = self.x
        y = self.y
        #
        # check if any target is nearby
        #
        for dx,dy in order:
            n = field[x+dx][y+dy]
            if n < 0: continue
            if getunit(n).kind != self.kind: 
                if DEBUG: print(self.ID(), " is not moving")
                return False
        dx, dy, dist = start_dir_w_distance(field, maxy, maxx, self)
        if dist > 0:
            if DEBUG1: print(self.ID(), " moves from: ", self.POS(), end="")
            self.move(dx, dy)
            if DEBUG1: print("  to: ", self.POS(), " dist: ", dist)
            return True
        return False
    def ID(self):
        return self.kind[0] +  str(self.ix)
    def POS(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    #
    # play will check first if an attack can be made, if not,
    # False is returned
    #
    def play(self):
        can = self.canmove()
        if can and DEBUG:
            print(self.ID(), " moves to: ", self.POS())
        can, u = self.canattack()
        if can:
            self.attack(u)
            if DEBUG1: print(self.ID(), " attacks: ", u.ID(), " giving it ", u.hitPoints)


def init(fname):
    global field, maxx, maxy, units, numunits, numelf, numgob, elves_lost_count
    
    y = 0
    maxy = 0
    maxx = 0
    units.clear()
    numunits = 0
    numelf = 0
    numgob = 0
    elves_lost_count = 0
    for line in open(fname, "r"):
        x = 0
        maxx = max(maxx, len(line.strip()))
        for c in line.strip():
            if c == '#':
                field[x][y] = -2
            elif c == '.':
                field[x][y] = -1
            elif c == 'E':
                e = Unit(x, y, "Elf", numunits)
                field[x][y] = len(units)
                units.append(e)
                numelf += 1
                numunits += 1
            elif c == 'G':
                g = Unit(x, y, "Gob", numunits)
                field[x][y] = len(units)
                units.append(g)
                numgob += 1
                numunits += 1
            else:
                print("error at ", x, y)
            x += 1
        y += 1
        maxy = y
        
def playround(r):
    global numgob, numelf
    if DEBUG: print("\n\nRound: ", r)
    us = getunits()
    for u in us:
        if numgob == 0 or numelf == 0: return True
        if u.alive:
            u.play()
    if DEBUG: gridout()
    return False

def runfile(fname, tv, p1out = True, part2 = 0):
    global numgob, numelf, elves_lost_count
    
    init(fname)
    if part2 > 0: set_elf_attack(part2)
    if DEBUG1: gridout()

    r = 0
    Done = False
    while not Done:
        if part2 > 0 and elves_lost_count > 0: return False, 0, 0
        r += 1
        if DEBUG1: print("*** Round ", r)
        Done = playround(r)
    r -= 1
    total_hitpoints = 0
    for u in units:
        if u.alive:
            total_hitpoints += u.hitPoints

    if DEBUG1: gridout()
    if not p1out: return True, r, total_hitpoints
    if r * total_hitpoints == tv:
        print("Part 1:  battle ended in round: ", r, "  with remaining hitpoints: ", total_hitpoints, " Outcome: ", r * total_hitpoints)
    else:
        print("Part 1:  ERROR ended in round: ", r, "  with remaining hitpoints: ", total_hitpoints, " Outcome: ", r * total_hitpoints)
    return True, r, total_hitpoints

def part1_tests():
    runfile("test1.txt", 27730)

    runfile("test2.txt", 36334)

    runfile("test3.txt", 39514)

    runfile("test4.txt", 28944)

    runfile("test5.txt", 18740)

#
# Part 1:
#
runfile("data.txt", 228240)

#
# Part 2:
#
## use binary search

def runpart2(fn, lower, upper):
    global elves_lost_count
    uval = upper
    Done = False
    last_tp = 0
    last_r = 0
    for nval in range(lower, upper+1):
        tf, r, tp = runfile(fn, 0, False, nval)
        # print("T/F: ", tf,  " nval: ", nval, "  round: ", r, "  tp: ", tp, " elc: ", elves_lost_count)
        # gridout()
        if elves_lost_count == 0:
            return tp, nval, r

totalhp, new_value, rounds  = runpart2("data.txt", 3, 50)
print("Part 2:  ended in round: ", rounds, "  with remaining hitpoints: ", totalhp, " Outcome: ", rounds * totalhp)
