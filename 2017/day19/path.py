'''

--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

Your puzzle answer was PVBSCMEQHY.
--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |          
     |  +--+    
     A  |  C    
 F---|--|-E---+ 
     |  |  |  D 
     +B-+  +--+ 

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

Your puzzle answer was 17736.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

expected_chars=[]
letters = []
path = []
DOWN = 1
UP = -1
LEFT = 2
RIGHT = -2

ccol = 0
crow = 0
# pad grid with a space at 0 and end for each line
# and a initial and final row of spaces

for line in open('data.txt'):
    nl = ''.join([' ', line[:len(line)-1], ' '])
    # print(nl)
    if crow == 0:
        sprow = ' '*(len(nl) + 2)
        path.append(sprow)
        ccol = nl.find('|')
    path.append(nl)
    for a in nl:
        if a.isalpha():
            expected_chars.append(a)
    crow += 1
sprow = ' '*(len(nl) + 2)
path.append(sprow)


def setdir(path, r, c, d):
    nc = ' '
    if d == DOWN or d == UP:
        
        right_char = path[r][c+1]
        left_char = path[r][c-1]

        if not left_char == ' ' :
            d = LEFT
        elif not right_char == ' ' : 
            d = RIGHT
    elif d == RIGHT or d == LEFT:
        down_char = path[r+1][c]
        up_char = path[r-1][c]

        if not down_char == ' ' :
            d = DOWN
        elif not up_char == ' ' :
            d = UP
    return d

def getnext(p, r, c, d):
    global letters
    #print(p)
    cc = p[r][c]
    #print("getnext: ", r, c, cc)
    if cc == ' ':
        print("ERROR")
    if cc == "+":
        d = setdir(p, r, c, d)
        #print("Found + at ", r, c, d)
    
    if d == DOWN:
        r += 1
    elif d == UP:
        r -= 1
    elif d == RIGHT:
        c += 1
    elif d == LEFT:
        c -= 1
    #print(r,c)
    cc = p[r][c]
    #print(cc, r, c, d)
    # if cc in expected_chars:
        # letters.append(cc)
    # elif cc == '+':
        # d = setdir(path, r, c, d)
    return p[r][c], r, c, d

cdir = DOWN
crow = 1
done = False
count = 0
while not done:
    count += 1
    nc, crow, ccol, cdir = getnext(path, crow, ccol, cdir)
    if nc in expected_chars:
        letters.append(nc)
    if len(letters) == len(expected_chars): done = True
    
print("Part 1: letters encountered in this order: ", ''.join(letters))
print("Part 2: total number of steps is: ", count+1)
