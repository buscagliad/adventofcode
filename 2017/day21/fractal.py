'''

--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3 square by following the corresponding enhancement rule.
    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the square matches the second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

Your puzzle answer was 203.
--- Part Two ---

How many pixels stay on after 18 iterations?

Your puzzle answer was 3342470.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import copy
import numpy as np


Rules3 = {}
Rules2 = {}

#
# For Rules2 the following six are true
#
# ../..   0
# #./..   1,2,4,8
# ##/..   3,5,10,12
# #./.#   9,6
# ##/.#   7,11,13,14
# ##/##   15
#
def rule2(n, p):
    rv = False
    c1 = [1,2,4,8]
    c2 = [3,5,10,12]
    c3 = [9,6]
    c4 = [7,11,13,14]
    if n == 0 and p == 0: rv = True
    elif p in c1 and n in c1: rv = True
    elif p in c2 and n in c2: rv = True
    elif p in c3 and n in c3: rv = True
    elif p in c4 and n in c4: rv = True
    elif p == 15 and n == 15: rv = True
    return rv

def testrule2():
    for n in range(16):
        for k in range(16):
            print(n, k, rule2(n, k))

#
# p is a list of bits - with p[0] the one's digits
# p[1] the two's digit, etc.
#
def bits2int(p):
    out = 0
    pwr2 = 1
    for r in p:
        for j in r:
            if j: out += pwr2
            pwr2 <<= 1
    return out
    
#
# converts an integer into a bit array
# pad requires the returned bit array to have at least pad
# elements
#
def getbits(p, pad = 0):
    bits = []
    while p:
        if p & 1:
            bits.append(1)
        else:
            bits.append(0)
        p >>= 1
    while len(bits) < pad:
        bits.append(0)
    return bits


#
# rotate3 will rotate (clockwise) the passed in
# bit array - the bit array must be of length 9
# or zeros are returned.
#
def rotate3(p):
    rp = np.zeros([3,3], dtype = int)
    for c in range(3):
        for r in range(3):
            rp[c][2-r] = p[r][c]

    return rp
#
# flip3 flips a bit array of  length 9:
# 0 1 2       2 1 0
# 3 4 5  -->  5 4 3
# 6 7 8       8 7 6
#
def flip3(p):
    for r in range(3):
        save = p[r][0]
        p[r][0] = p[r][2]
        p[r][2] = save

def testrot():
    tv = [[1,2,3],[4,5,6],[7,8,9]]
    for i in range(2):
        for _ in range(4):
            print(tv)
            tv = rotate3(tv)
    flip3(tv)

#testrot()
#exit(1)

#
# getswps(n) will return a set of all
#   possible swaps from the passed in 3x3 array
#
def getswps (b):
    nb = copy.deepcopy(b)
    rv = set()
    for _ in range(2):
        for k in range(4):
            rv.add(bits2int(nb))
            nb = rotate3(nb)
            #print(nb)
        flip3(nb)
    #print("getswps: ", nb, rv)
    return rv
    

def test(n):
    bits = getbits(n, 9)
    n2 = bits2int(bits)
    if n == n2:
        print("SUCCESS: ", n, bits, n2)
    else:
        print("ERROR: ", n, bits, n2)


def str2bits(s):
    n = 0
    #print("strbits: ", s)
    match len(s):
        case 5: # 2x2
            n = 2
        case 11: # 3x3
            n = 3
        case 19: # 4x4
            n = 4
        case _:
            print("ERROR s is: ", s)
    p = np.zeros([n,n], dtype = int)
    r = 0
    c = 0
    for a in s:
        if a == '/': 
            r += 1
            c = 0
            continue
        elif a == '#': 
            p[r][c] = 1
        c += 1
    #print(p)
    return p
    
def bits2str(b):
    s = ""
    n = 0
    for r in b:
        for c in r:
            if c == 1:
                s += '#'
            else:
                s += '.'
        s += '/'
    return s
#
# line must be stripped of last <cr>
#
def process(line):
    global Rules2, Rules3
    #print(line)
    ##/.. => ###/#.#/..#
    ###/#.#/##. => ...#/###./..##/.#.#
    ls = line.find(" => ")
    key = str2bits(line[:ls])
    pat = line[ls+4:]
    #
    # find all rotations of key and map to pattern
    #
    pattern = str2bits(pat)

    #print(len(key), key, pattern)
    if len(key) == 2:
        n = bits2int(key)
        #print("HELLO: ", key, "  ", n)
        for a in range(16):
            if rule2(n, a):
                #print("adding ", a, " to ", n)
                Rules2[a] = pattern
    if len(key) == 3:
        #print("key: ", key, bits2int(key), bits2str(key))
        for a in getswps(key):
            if a in Rules3:
                print(a, " is a repeat")
                print("key: ", bits2str(key))
                print("  -> ", getswps(key))
                exit(1)
            Rules3[a] = pattern
            #print(a, getbits(a, 9))
    #print(pattern, p)



def updateGrid(grid):
    ng = []
    for g in grid:
        if len(g) == 4:
            r = Rules2[bits2int(g)]
            #print('2 updateGrid: ', r)
            ng.append(r)
        else:
            r = Rules3[bits2int(g)]
            #print('3 updateGrid: ', r)
            for a in r:
                ng.append(a)
    return ng

def dumpRules():
    for r in Rules3:
        print(getbits(r, 9), r, Rules3[r])
    print(len(Rules3))
    for r in Rules2:
        print(getbits(r,4), r, Rules2[r])
    print(len(Rules2))

def count(grid):
    c = 0
    for g in grid:
        c += sum(g)
    return c

def leng(ng):
    s = 0
    for g in ng:
        s += len(g)
    return s

def outgrid(g):
    for ng in g:
        s = len(ng)
        ss = 1
        for a in range(s//2):
            if ss*ss == s: break
            ss += 1
        index = 0
        print("Len: ", s, "  side: ", ss)
        for i in range(ss):
            for j in range(ss):
                print(index)
                if ng[index]: print("#", end="")
                else: print(".", end="")
                index += 1
            print()
        
def part1():
    ng = Grid
    print(ng)
    print("Round ", 0, " sum is ", count(ng))
    for i in range(6):
        ng = updateGrid(ng)
        #outgrid(ng)
        print("Round ", i+1, " sum is ", count(ng))
        #print(ng)
    


def get3x3from2x2(g, r, c):
    rule = [ [g[r][c], g[r][c+1]], [g[r+1][c], g[r+1][c+1]]]
    index = bits2int(rule)
    return Rules2[index]

def get4x4from3x3(g, r, c):
    rule = [
            [g[r][c],     g[r][c+1],   g[r][c+2]], 
            [g[r+1][c], g[r+1][c+1], g[r+1][c+2]],
            [g[r+2][c], g[r+2][c+1], g[r+2][c+2]]
           ]
    index = bits2int(rule)
    return Rules3[index]

#
# start with n 2x2 grids (n is a perfect square)
#
def upgrid2(g):
    size = len(g[0])
    nsize = size//2 # number of 2x2 on a row
    rg = np.zeros([3*nsize,3*nsize], dtype = int) # each 2x2 will turn into a 3x3
    #print("upgrid2: size: ", size, "  nsize = ", nsize)
    s = 0
    for r in range(nsize):
        t = 0
        for c in range(nsize):  # r,c is index into upper left corner of 2x2
            q = get3x3from2x2(g, 2*r, 2*c)  # q is a 3x3 array
            for m in range(3):
                for n in range(3):
                    rg[m+r*3][n+c*3] = q[m][n]
    return rg
#
# start with n 3x3 grids to produce
#            4n 2x2 grids
#
def upgrid3(g):
    size = len(g[0])
    nsize = size//3 # number of 3x3 in a row
    rg = np.zeros([4*nsize,4*nsize], dtype = int)
    #print("upgrid3: size: ", size, "  nsize = ", nsize)
    s = 0
    for r in range(nsize):
        t = 0
        for c in range(nsize):
            q = get4x4from3x3(g, 3*r, 3*c)
            for m in range(4):
                for n in range(4):
                    rg[m+4*r][n+4*c] = q[m][n]
    return rg
    

def upgrid(g):
    if len(g[0]) % 2 == 0:
        return upgrid2(g)
    return upgrid3(g)


# 119 is too low
# 256 is max possible
# 161 is not correct
# 344 is too high
for line in open('data.txt'):
    process(line.strip())

#dumpRules()

Grid = np.zeros([3,3], dtype = int)

igrid = [0,1,0,0,0,1,1,1,1]  # [".#.","..#","###"]
i = 0
j = 0
for k in range(9):
    Grid[k//3][k%3] = igrid[k]

#print(Grid)

def sumg(g):
    s = 0
    for r in g:
        for c in r:
            if c: s += 1
    return s

g = Grid
for it in range(1, 19):
    g = upgrid(g)
    #print(g)
    #print(sumg(g))
    if (it == 5): print("Part 1: number of lights on after 5 iterations: ", sumg(g), flush=True)
    
print("Part 2: number of lights on after 18 iterations: ", sumg(g), flush=True)
