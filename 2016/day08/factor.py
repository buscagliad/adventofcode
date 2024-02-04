
import numpy as np

NROW=6
NCOL=50

screen = np.zeros((NROW,NCOL), dtype=int)

def screenprint():
    for r in range(NROW):
        for c in range(NCOL):
            if screen[r][c] : print('#', end = "")
            else: print('.', end = "")
        print()

def rect(C, R):
    global screen
    for c in range(C):
        for r in range(R):
            screen[r][c] = 1


def rotcol(C, n):
    global screen
    col = np.zeros(NROW, dtype=int)
    for i in range(NROW):
        col[i] = screen[i][C]
    f = n
    for t in range(NROW):
        screen[f][C] = col[t]
        f += 1
        f %= NROW
        
def rotrow(R, n):
    global screen
    row = np.zeros(NCOL, dtype=int)
    for i in range(NCOL):
        row[i] = screen[R][i]
    f = n
    for t in range(NCOL):
        screen[R][f] = row[t]
        f += 1
        f %= NCOL

def process(line):
    if "rect" in line:
        w = line[5:].split('x')
        #print("RECT: ", w)
        rect(int(w[0]), int(w[1]))
    elif "row" in line:
        w = line[13:].split(' by ')
        rotrow(int(w[0]), int(w[1]))
        #print("ROW: ", w)
    elif "column" in line:
        w = line[16:].split(' by ')
        rotcol(int(w[0]), int(w[1]))
        #print("COL: ", w)
    #screenprint()
    #print()

for line in open('data.txt'):
    process(line.strip())


print("Part 1: number of pixels is: ", sum(sum(screen)))
screenprint()
