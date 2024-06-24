'''
--- Day 12: Subterranean Sustainability ---

The year 518 is significantly more underground than your history books implied. Either that, or you've arrived in a vast cavern network under the North Pole.

After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right. A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots. Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation. These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

    A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
    A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
    A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.

It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #

For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3     
       0         0         0         0     
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.

The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right. Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34. Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?

Your puzzle answer was 2281.
--- Part Two ---

You realize that 20 generations aren't enough. After all, these plants will need to last another 1500 years to even reach your timeline, not to mention your future.

After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?

Your puzzle answer was 2250000000120.

Both parts of this puzzle are complete! They provide two gold stars: **


'''

import numpy as np
import copy 

class Plant:
    def __init__(self, filename, n):
        self.list = np.zeros([n], dtype=int)
        self.left = 0
        self.right = 0
        self.zero = 0
        self.rulesadd = []
        self.rulesrem = []
        first = True
        for line in open(filename, "r"):
            if first:
                first = False
                self.initplants(line)
            else:
                self.add(line)
    def initplants(self, line):
        self.left = len(self.list) // 2 - (len(line) - 15) // 2 
        self.zero = self.left
        n = self.left
        for a in line[15:]:
            if a == '#': self.list[n] = 1
            n += 1
        self.right = n
    def add(self, line):
        if len(line) < 9: return
        rule = np.zeros([5], dtype = int)
        n = 0
        for a in line[:5]:
            if a == "#":
                rule[n] = 1
            n += 1
        if line[9] == '#':
            self.rulesadd.append(rule)
        else:
            self.rulesrem.append(rule)
    def score(self):
        self.setends()
        s = 0
        for i in range(self.left, self.right+1):
            if self.list[i] == 1:
                s += i - self.zero
        return s
    def state(self):
        print("Score: ", self.score(), "  State: ", self.list[self.left:self.right+1])
    def out(self):
        print("State: ", self.list[self.left:self.right])
        print("Add rules:")
        for r in self.rulesadd:
            print("  ", r)
        print("Remove rules:")
        for r in self.rulesrem:
            print("  ", r)
    def setends(self):
        for i, v in enumerate(self.list):
            if v == 1:
                self.left = i
                break
        for i in range(len(self.list)-1, 0, -1):
            if self.list[i] == 1:
                self.right = i
                break
    def match(self, pattern, index):
        for i, v in enumerate(pattern):
            if self.list[i+index-2] != v: return False
        return True
        
    def play(self):
        newlist = np.zeros([len(self.list)], dtype=int)

        self.setends()
        for i in range(self.left-2, self.right+3):
            for t in self.rulesadd:
                if self.match(t, i):
                    newlist[i] = 1
            for t in self.rulesrem:
                if self.match(t, i):
                    newlist[i] = 0
        self.list = newlist
        #print(self.left, self.right)
        
c = Plant("data.txt", 1000)
#c.state()
for _ in range(20):
    c.play()
    
      
print("Part 1: plant score: ", c.score())

#
# for Part 2, i ran a test of 2000 generations and
# noticed that after some time, the score of the pots  
# each generation increases by a constant number (45)
#
# So, we'll seach for the following:
#    continue to play a generation until
#    three diffences in the scores in a row are the same
#    we'll designate this constant difference as C
#    if this happens at generation G, and the score at 
#    Gth generation is S, then the solution is:
#        S +  (50,000,000,000 - G) * C
#

p2 = Plant('data.txt', 20000)
TotGens = 50000000000
inArow = 0
lastG = 0
lastGdiff = 0
gen = 0
while inArow < 3:
    gen += 1
    p2.play()
    G = p2.score()
    Gdiff = G - lastG
    if Gdiff == lastGdiff:
        inArow += 1
    else:
        inArow = 0
    lastG = G
    lastGdiff = Gdiff

print("Part 2: sum of pot numbers: ", G + (TotGens - gen)*Gdiff)
