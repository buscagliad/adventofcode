from collections import namedtuple
from copy import deepcopy
import numpy as np
from shapely.geometry import Polygon, Point

START='S'
VERT='|'
HORZ='-'
NE='L'
NW='J'
SW='7'
SE='F'
GROUND='.'
mNumRows = 0
mNumCols = 0


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
STAY = 0
dirs=["STAY","NORTH","SOUTH","WEST","EAST"]


def process(f):
	global mNumRows
	global mNumCols
	m = []
	lno = 0
	col = -1
	row = -1
	for line in open(f, "r"):
		m.append(line.strip())
		if col < 0:
			a = line.find(START)
			mNumCols = len(line) - 1
			if a >= 0: 
				col = a
				row = lno
		lno += 1
	mNumRows = lno
		
	return m, row, col

## f is how we got here (WEST, EAST, NORTH or SOUTH)
## t is the type of direction object (HORZ, VERT, NE, NW, SE, SW)
## START='S'
## VERT='|'
## HORZ='-'
## NE='L'
## NW='J'
## SW='7'
## SE='F'

pipetypes={}
pipetypes[START] = 1
pipetypes[VERT] = 2
pipetypes[HORZ] = 3
pipetypes[NE] = 4
pipetypes[NW] = 5
pipetypes[SW] = 6
pipetypes[SE] = 7

def entryExit(entry, pType):
	if entry == WEST:
		if pType == NW: return SOUTH, NORTH
		elif pType == SW: return NORTH, SOUTH
		elif pType == HORZ: return WEST, EAST
		else: print ("ERROR - at ", pType, " going ", dirs[entry])
	elif entry == EAST:
		if pType == NE: return SOUTH, NORTH
		elif pType ==  SE: return NORTH, SOUTH
		elif pType ==  HORZ: return EAST, WEST
		else: print ("ERROR - at ", pType, " going ", dirs[entry])
	elif entry == NORTH:
		if pType == NE: return WEST, EAST
		elif pType ==  NW: return EAST, WEST
		elif pType ==  VERT: return NORTH, SOUTH
		else: print ("ERROR - at ", pType, " going ", dirs[entry])
	elif entry == SOUTH:
		if pType == SW: return EAST, WEST
		elif pType ==  SE: return WEST, EAST
		elif pType ==  VERT: return SOUTH, NORTH
		else: print ("ERROR - at ", pType, " going ", dirs[entry])
	else:
		print ("ERROR - INVALID DIRECTION: ", entry)
	return 0

	
def incPipe(here, direction):
	h = here
	if direction == WEST:	
		h = [ here[0], here[1]-1 ]
	elif direction == EAST: 
		h = [ here[0], here[1]+1 ]
	elif direction == NORTH: 
		h = [ here[0]-1, here[1] ]
	elif direction == SOUTH: 
		h = [ here[0]+1, here[1] ]
	return h

##
## movePipe will move to the next pipe based on where
## the pipe is, the type of pipe, and what side was entered
## it returns moved to location and the exit direction
##
def movePipe(m, here, entered):
	#print("movePipe: here: ", here, " entered: ", entered)
	p = getPipe(m, here)
	d, di = entryExit(entered, p)
	h = incPipe(here, di)
	# print("movePipe: p: ", p, " d: ", d, "  to: ", h)
	if h == here:
		print("ERROR in movePipe - bad-direction", d)
		exit(1)
		
	if h[0] < 0 or h[1] < 0 or h[0] >= mNumRows or h[1] >= mNumCols:
		print("ERROR in movePipe", h)
		exit(1)
	#print (h)
	return h, getPipe(m, h), d

def validPipe(m, h, d):
	if h[0] < 0 or h[1] < 0 or h[0] >= mNumRows or h[1] >= mNumCols:
		return False
	p = getPipe(m, h)
	if d == WEST: return p in [NE, SE, HORZ]
	elif d == EAST: return p in [NW, SW, HORZ]
	elif d == NORTH: return p in [NW, NE, VERT]
	elif d == SOUTH: return p in [SW, SE, VERT]
	print ("ERROR - INVALID DIRECTION: ", f)	

def getPipe(m, here):
	return m[here[0]][here[1]]


m, row, col = process('data.txt')
start = [row,col]
grid = np.zeros([mNumRows, mNumCols], dtype=int)
grid[row][col] = 1

here = start
hered = STAY
#
# fing out which direction to move from 'S'
for fromDirection in [NORTH, SOUTH, WEST, EAST]:
	here = incPipe(start, fromDirection)
	if validPipe(m, here, fromDirection):
		# print("Good to move from ", start, " to ", here, " Direction: ", dirs[fromDirection])
		hered = fromDirection
		# print("A Hered: ", hered)
		break
	#else:
		#print("CANNOT move from ", start, " to ", here)
#print("Start is at ", start, " symbol is: ", getPipe(m, start), " proceeding to ", dirs[hered], " next cell is ", incPipe(start, hered))

#
# get 'from direction:
if hered == EAST: hered = WEST
elif hered == WEST: hered = EAST
elif hered == NORTH: hered = SOUTH
elif hered == SOUTH: hered = NORTH
grid[here[0]][here[1]] = pipetypes[getPipe(m, here)]
poly=[]
poly.append(Point(here[0],here[1]))
steps = 1
while True:
	newhere, p, hered = movePipe(m, here, hered)
	steps += 1
	here = newhere
	grid[here[0]][here[1]] = pipetypes[p]
	poly.append(Point(here[0],here[1]))
	if p == START: break

print("Part 1: number of steps furthest from start: ", steps//2)
	
p = Polygon(poly)
count = 0
numzeros = 0
for i in range(mNumRows):
	for j in range(mNumCols):
		if p.contains(Point(i,j)):
			count+=1


print("Part 2: number of tiles contained in path: ", count);

