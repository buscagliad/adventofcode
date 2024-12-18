'''

--- Day 9: Disk Fragmenter ---
Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402
The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222
The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899
The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............
The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)

Your puzzle answer was 6299243228569.

--- Part Two ---
Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?

Your puzzle answer was 6326952672104.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

disk = []
DEBUG = False

def checksum(l):
    i = 0
    s = 0
    bindex = 0
    for d in l:
        fileid = d[0] 
        nblocks = d[1]
        state = d[2]
        for _ in range(nblocks):
            if state == FIXED: 
                s += bindex * fileid
            bindex += 1
    return s

# states
FILE = 1
SPACE = -1
FIXED = 2 # indicates the file is fixed and cannot be moved

def process(line):
    global disk
    disk.clear()
    file = True   # False indicates it is space
    fid = 0
    for a in line:
        if file:
            n = int(a)
            disk.append([fid, n, FILE])
        else:
            sp = int(a)
            disk.append([-1,sp, SPACE])
            fid += 1
        file = not file

def init(filename):
    for l in open(filename, 'r'):
        process(l.strip())

def fileinsert(d): # e, f):
    to_index = 0
    from_index = len(d)-1
    while d[to_index][2] != SPACE: 
        if d[to_index][2] == FILE:
            d[to_index][2] = FIXED
        to_index += 1
    while d[from_index][2] != FILE: 
        from_index -= 1
        if from_index < 1: return False
    if DEBUG: print("fileinsert: ", to_index, ": ", disk[to_index], from_index, ": ", disk[from_index])
    mid, m, mstate = d[from_index]
    nid, n, nstate = d[to_index]
    if m <= n:  # can move ALL symbols (perhaps with leftover)
        d[to_index][0] = mid
        d[to_index][1] = m
        d[to_index][2] = FIXED
        d[from_index][2] = SPACE
        #
        # ins represents the leftover space
        #
        if n > m:
            ins = [-1, n-m, SPACE]
            if DEBUG: print("Insert: ", ins, " at ", to_index+1)
            d.insert(to_index+1, ins)
            from_index += 1

    else: # m > n
        d[to_index][0] = mid # fill in file id and decrement
        d[to_index][2] = FIXED
        d[from_index][1] -= n    # what remains

        # to_index += 1
        # don't modify rid
    return True


def fileinsert2(d): # e, f):
    if DEBUG: print("fileinsert: ", to_index, ": ", disk[to_index], from_index, ": ", disk[from_index])
    done = False
    
    from_index = len(d)-1
    n = 0
    while not done and n < 10:
        n += 1
        # what file will we try to move?
        while d[from_index][2] != FILE: 
            from_index -= 1
            if from_index <= 1: 
                return False
        mid, m, state = d[from_index]
        if DEBUG: print("Trying to move: ", from_index, d[from_index])
        #
        # at this point, the file we will attempt to move is
        # at index from_index - we will cycle through all
        # possible to_index's and if none found, we'll mark 
        # this from_index file as FIXED
        movemade = False
        for to_index in range(0, from_index):
            #
            # mark all files prior to first space as FIXED
            # if d[to_index][2] == FILE and not spacefound:
                # d[to_index][2] = FIXED
            # elif d[to_index][2] == FILE: spacefound = True
            if d[to_index][2] == SPACE:
                nid, n, state = d[to_index]
                if m <= n:
                    movemade = True
                    d[to_index][0] = mid # fill in file id and decrement
                    d[to_index][1] = m
                    d[to_index][2] = FIXED
                    d[from_index][2] = SPACE
                    d[from_index][0] = -1
                    #
                    # ins represents the leftover space
                    #
                    if n > m:
                        # the next entry should be 'space'
                        addholes = n-m
                        if DEBUG: print("Insert: ", ins, " at ", to_index+1)
                        to_index += 1
                        if d[to_index][2] == SPACE:
                            d[to_index][1] += addholes
                        else:
                            ins = [-1, n-m, SPACE]
                            if DEBUG: print("Insert: ", ins, " at ", to_index)
                            d.insert(to_index, ins)
                    break
        if DEBUG: print("After for loop: ", to_index, from_index, movemade, flush=True)
        if not movemade:
            if DEBUG: print("setting ", from_index, " to FIXED")
            d[from_index][2] = FIXED

  

datafile = 'data.txt'
init(datafile)

#
# part 1
#
done = False
s = 0
to_index = 1     # empty index
from_index = len(disk) - 1
#
# Part 1
# 
cont = True
while cont:
    cont = fileinsert(disk)

print("Part 1: checksum of disk file is: ", checksum(disk))

init(datafile) # refresh 'disk'

#
# Part 2
# 

fileinsert2(disk)

print("Part 2: checksum of disk file is: ", checksum(disk))
