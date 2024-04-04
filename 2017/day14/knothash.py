'''
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle answer was 8214.
--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are present.

How many regions are present given your key string?

Your puzzle answer was 1093.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import numpy as np

def knot_hash(input_string):
    # Step 1: Convert input string to list of ASCII codes
    lengths = [ord(char) for char in input_string.strip()]
    # Step 2: Append standard length suffix values
    lengths.extend([17, 31, 73, 47, 23])

    # Step 3: Initialize variables
    sparse_hash = list(range(256))
    current_position = 0
    skip_size = 0

    # Step 4: Perform 64 rounds
    for _ in range(64):
        for length in lengths:
            # Reverse sublist
            sublist = []
            for i in range(length):
                sublist.append(sparse_hash[(current_position + i) % 256])
            sublist.reverse()
            for i in range(length):
                sparse_hash[(current_position + i) % 256] = sublist[i]
            # Move current position forward
            current_position = (current_position + length + skip_size) % 256
            # Increase skip size
            skip_size += 1

    # Step 5: Calculate dense hash
    dense_hash = []
    for block_start in range(0, 256, 16):
        block = sparse_hash[block_start:block_start + 16]
        dense_hash.append(f"{block[0] ^ block[1] ^ block[2] ^ block[3] ^ block[4] ^ block[5] ^ block[6] ^ block[7] ^ block[8] ^ block[9] ^ block[10] ^ block[11] ^ block[12] ^ block[13] ^ block[14] ^ block[15]:02x}")

    # Step 6: Concatenate hexadecimal values
    knot_hash = ''.join(dense_hash)

    return knot_hash

bitcount = {}
bitcount['0'] = [0,0,0,0]
bitcount['1'] = [0,0,0,1]
bitcount['2'] = [0,0,1,0]
bitcount['3'] = [0,0,1,1]
bitcount['4'] = [0,1,0,0]
bitcount['5'] = [0,1,0,1]
bitcount['6'] = [0,1,1,0]
bitcount['7'] = [0,1,1,1]
bitcount['8'] = [1,0,0,0]
bitcount['9'] = [1,0,0,1]
bitcount['a'] = [1,0,1,0]
bitcount['b'] = [1,0,1,1]
bitcount['c'] = [1,1,0,0]
bitcount['d'] = [1,1,0,1]
bitcount['e'] = [1,1,1,0]
bitcount['f'] = [1,1,1,1]

grid = np.zeros((128,128), dtype=int)

def getbitcount(s):
    global grid
    for row in range(128):
        col = 0
        news = s + "-" + str(row)
        knot = knot_hash(news)
        for k in knot:
            for i, b in enumerate(bitcount[k]):
                grid[row][col+i] = b
            col += 4

def gridsum():
    gs = 0
    row = 0
    for row in range(128):
        sg = sum(grid[row])
        gs += sg
        #print(row, sg)
        row += 1
    return gs

def check(x, y, num):
    global grid
    if x >= 128 or x < 0: return
    if y >= 128 or y < 0: return
    #print("check ", x, y, grid[x][y], num, flush=True)
    if grid[x][y] == 0: 
        #print("--- return on 0")
        return
    elif grid[x][y] == 1: 
        grid[x][y] = num
        #print("--- setting ", x, y, " to ", num)
    else: 
        #print("--- failed tests")
        return
    check(x-1,y,num)
    check(x+1,y,num)
    check(x,y-1,num)
    check(x,y+1,num)

def find():
    global grid
    for x in range(128):
        for y in range(128):
            if grid[x][y] == 1: return x,y
    return -1,-1
   
#print(gridsum())
#exit(1)
s = "hxtvlmkl"
getbitcount(s)
def print8x8():
    for i in range(8):
        for j in range(8):
            if grid[i][j] == 0: print('.', end="")
            else: print('#', end="")
        print()
print("Part 1: Knot has for ", s, " is ", knot_hash(s), " bit count is: ", gridsum())

x = 0
y = 0
gnum = 1
while not x == -1:
    gnum += 1
    x, y = find()
    check(x,y,gnum)
    #print(x, y, gnum, flush=True)

# subtract -1 because we are using 2 as our group starting point
#      and another -1 becuase we 'failed' or 'ended' after the last gnum += 1
print("Part 1: Number of groups ", gnum-2)
