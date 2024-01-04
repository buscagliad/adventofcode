
import numpy as np
import copy

import sys
from functools import lru_cache
import collections

sys.setrecursionlimit(150000)

MAXX=200
MAXY=200

grid = np.zeros([MAXX,MAXY], dtype = int)
gridCol = 0
gridRow = 0
sgrid = np.zeros([MAXX,MAXY], dtype = int)
sdir = np.zeros([MAXX,MAXY], dtype = int)
scnt = np.zeros([MAXX,MAXY], dtype = int)

LEFT=1
UP=2
RIGHT=4
DOWN=8

HORZ = LEFT | RIGHT
VERT = UP | DOWN

ALLDIR = LEFT | RIGHT | UP | DOWN

def dirset(d, b):
	return d | b

def dirclear(d, b):
	return d & ~b

def dircheck(d, b):
	return d & b


MAX_MOVES = 3

NOT_SET = -1

minloss = 10000

##
## rdir is one of LEFT, UP, RIGHT or DOWN
## rcnt is number of steps already made in that direction
##
def mindval(g, s, sdir, scnt, nx, ny, x, y):
	rv = False;
	sumv = 0;
	if not (s[x][y] == NOT_SET):
		if (x - 1 >= 0): #  LEFT
			if sdir[x-1][y] & HORZ:	# I can move left or right
				sumv = s[x][y] + g[x-1][y]
				if (sumv < s[x-1][y]) or s[x-1][y] == NOT_SET:
					if scnt[x][y] > MAX_MOVES and sdir[x][y] & LEFT:
						sdir[x-1][y] &= ~HORZ	# disable getting adjacent
						print("WHAT???", sdir[x-1][y] )
					else:
						if sdir[x][y] & LEFT:
							scnt[x-1][y] = 1 + scnt[x][y]
						else:
							scnt[x-1][y] = 1	
						s[x-1][y] = sumv
						rv = True

		if (x + 1 < nx):  # RIGHT
			if sdir[x-1][y] & HORZ:	# I can move left or right
				sumv = s[x][y] + g[x+1][y]
				if (sumv < s[x+1][y]) or (s[x+1][y] == NOT_SET) :
					if scnt[x][y] > MAX_MOVES and sdir[x][y] & RIGHT:
						sdir[x+1][y] &= ~HORZ	# disable getting adjacent
						print("WHAT???", sdir[x+1][y] )
					else:
						if sdir[x][y] & RIGHT:
							scnt[x+1][y] = 1 + scnt[x][y]
						else:
							scnt[x+1][y] = 1	
						s[x+1][y] = sumv
						rv = True
					
		if (y - 1 >= 0):# UP
			if sdir[x][y-1] & VERT:	# I can move up or down
				sumv = s[x][y] + g[x][y-1]
				if ( (sumv < s[x][y-1]) or (s[x][y-1] == NOT_SET) ) :
					if scnt[x][y] > MAX_MOVES and sdir[x][y] & UP:
						sdir[x][y-1] &= ~VERT
						print("WHAT???", sdir[x][y-1] )
					else:
						if sdir[x][y] & UP:
							scnt[x][y-1] = 1 + scnt[x][y]
						else:
							scnt[x][y-1] = 1	
						s[x][y-1] = sumv
						rv = True

		if (y + 1 < ny): #  DOWN
			if sdir[x][y+1] & VERT:	# I can move up or down
				sumv = s[x][y] + g[x][y+1]
				if ( (sumv < s[x][y+1]) or (s[x][y+1] == NOT_SET) ) :
					if scnt[x][y] > MAX_MOVES and sdir[x][y] & DOWN:
						sdir[x][y+1] &= ~VERT
						print("WHAT???", sdir[x][y-1] )
					else:
						if sdir[x][y] & DOWN:
							scnt[x][y+1] = 1 + scnt[x][y]
						else:
							scnt[x][y+1] = 1	
						s[x][y+1] = sumv
						rv = True
	return rv


#state = [i, j, total, dir, numd]
def route(g, s, sdir, scnt, nx, ny):
	save_first = g[0][0]
	g[0][0] = 0
	s[0][0] = 0
	done = False
	while (not done):
		done = True
		for x in range(nx):
			for y in range(ny):
				if mindval(g, s, sdir, scnt, nx, ny, x, y):
					done = False
	return s[nx-1][ny-1]


def zerodata(): 
	global grid
	global sgrid
	global sdir
	for i in range(MAXX):
		for j in range(MAXY): 
			grid[i][j] = 0
			sgrid[i][j] = NOT_SET
			sdir[i][j] = ALLDIR
	

def crucible():
	global minloss
	#global mem
	mem = np.zeros([200,200], dtype = int)
	# i, j, total, left, right, up, down):
	# state = []
	# state.append([0,1,0,0,1,0,0])
	# state.append([1,0,0,0,0,0,1])
	state = collections.deque()
	state.append([0,1,0,0,1,0,0])
	state.append([1,0,0,0,0,0,1])
	while state:
		i, j, total, left, right, up, down = state.pop()
		if left > 3: continue
		if right > 3: continue
		if up > 3: continue
		if down > 3: continue
		if i < 0 or i >= gridCol : continue
		if j < 0 or j >= gridRow : continue
		if mem[i][j] > 0 and total >= mem[i][j] : continue
		t = total + grid[i][j]
		if t +  (gridCol - j + gridRow - i) > minloss: continue
		mem[i][j] = t
		#print("mem[",i,"][",j,"] = ",t)
		#if t == 0: exit(1)
		if minloss > 1 and t >= minloss: continue
		if i == gridRow - 1 and j == gridCol - 1:
			if t < minloss:
				minloss = t
				print ("Current minloss: ", minloss, " queue size: ", len(state))
		#print(i, j)
		## ok to move left (all but right)
		if up > 0 or down > 0 or left > 0:
			state.append([i, j-1, t, left+1, 0, 0, 0])
		## ok to move right (all but left)
		if up > 0 or down > 0 or right > 0:
			state.append([i, j+1, t, 0, right+1, 0, 0])
		## ok to move up (all but down)
		if up > 0 or left > 0 or right > 0:
			state.append([i-1, j, t, 0, 0, up+1, 0])
		## ok to move down (all but up)
		if left > 0 or down > 0 or right > 0:
			state.append([i+1, j, t, 0, 0, 0, down+1])
	return minloss

gridRow = 0
zerodata()
for l in open("test2.txt"):
	line = l.strip()
	if len(line) < 2: break
	gridCol = len(line)
	print(l)
	i = 0
	for d in line:
		if d.isdigit():
			grid[gridRow][i] = int(d)
			i += 1
	gridRow += 1

c = route(grid, sgrid, sdir, scnt, gridRow, gridCol)
#c = crucible()
print(gridCol, gridRow)

print("Part 1: crucible min path is: ", c)


for i in range(gridRow):
	for j in range(gridCol):
		print("%4d" % (grid[i][j]), " ", end = "")
	print()
print()
for i in range(gridRow):
	for j in range(gridCol):
		print("%4d" % (scnt[i][j]), " ", end = "")
	print()
print()
for i in range(gridRow):
	for j in range(gridCol):
		print("%4d" % (sdir[i][j]), " ", end = "")
	print()
for i in range(gridRow):
	for j in range(gridCol):
		print("%4d" % (sgrid[i][j]), " ", end = "")
	print()
print()
