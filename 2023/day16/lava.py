
import numpy as np

grid = np.zeros([120,120],dtype=int)
xgrid = 0
ygrid = 0

ANGLE_RIGHT_MIRROR = 1	# /
ANGLE_LEFT_MIRROR = 2	# \
HORZ_SPLITTER = 3		# -
VERT_SPLITTER = 4		# |
SPACE = 0				# .

GRID_ITEMS = ["SPACE", "ANGLE RIGHT MIRROR", "ANGLE LEFT MIRROR", "HORIZONTAL SPLITTER", "VERTICAL SPLITTER"]

UP = 1
LEFT = 2
DOWN = 3
RIGHT = 4

DIRECTIONS = ["", "UP", "LEFT", "DOWN", "RIGHT"]

# Adding 100 to the above will 'energize' the grid element

def set_state(s, d):
	return s | 1 << d

def didalready(s, d):
	if s & (1 << d) == 0: return False
	return True
	


MARKS=['.', '/', chr(92), '-', '|']

#
# read in file:
#
def init():
	global xgrid
	global ygrid
	global grid
	xgrid = 0
	ygrid = 0
	for line in open("data.txt", "r"):
		i = 0
		if len(line) < 3: break
		for a in line:
			if   a == '.': grid[i][ygrid] = SPACE
			elif a == '/': grid[i][ygrid] = ANGLE_RIGHT_MIRROR
			elif a == chr(92) : grid[i][ygrid] = ANGLE_LEFT_MIRROR
			elif a == '-': grid[i][ygrid] = HORZ_SPLITTER
			elif a == '|': grid[i][ygrid] = VERT_SPLITTER
			if not a == '\n': i += 1
		ygrid += 1
		xgrid = i
	
def energized():
	count = 0
	for i in range(xgrid):
		for j in range(ygrid):
			if grid[i][j] >= 100: count += 1
	return count

def doit(i, j, d):
	state = np.zeros([120,120],dtype=int)
	init()
	last_energized = 0
	loop_count = 0
	paths = []
	paths.append([i, j, d])

	while paths:
		i, j, direction = paths.pop()
		if didalready(state[i][j], direction): continue
		state[i][j] = set_state(state[i][j], direction)
		#print("i j direction", i, j, direction)
		if i < 0 or i >= xgrid: continue
		if j < 0 or j >= ygrid: continue
		loop_count += 1
		t = grid[i][j] % 100
		grid[i][j] = t + 100
		#print (i, j, DIRECTIONS[direction], GRID_ITEMS[t])

		if t == ANGLE_RIGHT_MIRROR:
			if direction == UP:
				paths.append([ i+1, j, RIGHT])
			elif direction == LEFT:
				paths.append([ i, j+1, DOWN])
			elif direction == RIGHT:
				paths.append([ i, j-1, UP])
			elif direction == DOWN:
				paths.append([ i-1, j, LEFT])

		elif t == ANGLE_LEFT_MIRROR:
			if direction == UP:
				paths.append([ i-1, j, LEFT])
			elif direction == RIGHT:
				paths.append([ i, j+1, DOWN])
			elif direction == LEFT:
				paths.append([ i, j-1, UP])
			elif direction == DOWN:
				paths.append([ i+1, j, RIGHT])

		elif t == HORZ_SPLITTER:
			if direction == LEFT:
				paths.append([i-1, j, LEFT])			
			elif direction == RIGHT:
				paths.append([i+1, j, RIGHT])
			elif direction == UP:
				paths.append([i-1, j, LEFT])
				paths.append([i+1, j, RIGHT])
			elif direction == DOWN:
				paths.append([i-1, j, LEFT])
				paths.append([i+1, j, RIGHT])

		elif t == VERT_SPLITTER:
			if direction == DOWN:
				paths.append([i, j+1, DOWN])			
			elif direction == UP:
				paths.append([i, j-1, UP])
			elif direction == RIGHT or direction == LEFT:
				paths.append([i, j-1, UP])
				paths.append([i, j+1, DOWN])

		else:  # Space
			if direction == UP:
				paths.append([ i, j-1, UP])
			elif direction == LEFT:
				paths.append([ i-1, j, LEFT])
			elif direction == RIGHT:
				paths.append([ i+1, j, RIGHT])
			elif direction == DOWN:
				paths.append([ i, j+1, DOWN])
				
	return energized()
	
print("Part 1: Number of energized squares is: ", doit(0, 0, RIGHT))

'''
for i in range(xgrid):
	for j in range(ygrid):
		if grid[j][i] > 99: print("#", end="")
		elif grid[j][i] > 0: print("?", end="")
		else: print(".", end="")
	print()
	
for i in range(xgrid):
	for j in range(ygrid):
		t = grid[j][i] % 100
		print(MARKS[t], end="")
	print()
'''
#
# Part II
#

maxenergy = 0
enti = 0
entj = 0

for i in range(xgrid):
	e = doit(i,0,DOWN)
	if e > maxenergy: 
		maxenergy = e
		enti = i
		entj = 0
	e = doit(i,ygrid-1,UP)
	if e > maxenergy: 
		enti = i
		entj = ygrid-1
		maxenergy = e
	
for j in range(ygrid):
	e = doit(0,j,RIGHT)
	if e > maxenergy: 
		enti = 0
		entj = j
		maxenergy = e
	e = doit(xgrid-1,j,LEFT)
	if e > maxenergy: 
		enti = xgrid-1
		entj = j
		maxenergy = e
	
print("Part II: entry point at ", enti, entj, " for a max energy of: ", maxenergy)
