'''

--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?

Your puzzle answer was 2297.
--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

Your puzzle answer was 1745.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

xmas = []
YHIGH = 0
XWIDE = 0
for l in open('data.txt'):
    YHIGH += 1
    XWIDE = max(XWIDE, len(l.strip()))
    xmas.append(l.strip())

def cnt(i, j):
    if xmas[i][j] != 'X': return 0
    good = [1,1,1,1,1,1,1,1]
    g = 0
    for lets in ['M', 'A', 'S']:
        g += 1
        for n, d in enumerate([(0, -1),(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]):
            k = i + g * d[0]
            l = j + g * d[1]
            if not good[n]: continue
            if k < 0 or l < 0: 
                good[n] = 0
                continue
            elif k >= XWIDE or l >= YHIGH: 
                good[n] = 0
                continue
            # print(k, l, xmas[k][l], lets)
            if xmas[k][l] != lets: 
                good[n] = 0
    #print(good)
    return sum(good)

def MS2(L):
    mx = 0
    for a in L:
        if a == ['M', 'S'] or a == ['S', 'M']: mx += 1
    if mx == 2:
        return True
    return False

def mas(i, j):
    if xmas[i][j] != 'A': return 0
    if i == 0 or j == 0: return 0
    if i >= XWIDE - 1 or j >= YHIGH - 1: return 0
    L = [[xmas[i-1][j-1], xmas[i+1][j+1]], [xmas[i-1][j+1], xmas[i+1][j-1]]]
    if MS2(L): 
        return 1
    return 0

s = 0
for i in range(XWIDE):
    for j in range(YHIGH):
        s += cnt(i, j)
print("Part 1: total XMAS's: ", s)

s = 0
for i in range(XWIDE):
    for j in range(YHIGH):
        s += mas(i, j)
print("Part 2: total X-MAS's: ", s)
# 1967 is too high
# 1854 is too high
# 1811 is not correct
