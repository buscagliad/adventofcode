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
