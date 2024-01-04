
import numpy as np

import copy

grid = np.zeros([200,200], dtype = int)
gridCol = 0
gridRow = 0

def numeves():
	count = 0
	for i in range(gridRow):
		for j in range(gridCol):
			if grid[i][j] > 0 and grid[i][j] % 2 == 0:
				count += 1
	return count
	
def nummults(n):
	count = 0
	for i in range(gridRow):
		for j in range(gridCol):
			if grid[i][j] > 0 and grid[i][j] % n == 0:
				count += 1
	return count


LEFT=1
UP=2
RIGHT=3
DOWN=4

row = 0
col = 0
for line in open('data.txt', 'r'):
	if len(line) < 4: break
	col = 0
	for a in line.strip():
		if a == '#':
			grid[row][col] = -1
		if a == 'S':
			startrow = row
			startcol = col
		col += 1
	row += 1
	
gridCol = col
gridRow = row

def pgrid(n = 0, flat = True):
	count = 0
	for i in range(gridRow):
		for j in range(gridCol):
			if flat:
				if grid[i][j] > 1 and grid[i][j] %2 == 0: 
					print("O", end="")
					count += 1
				elif grid[i][j] < 0: print("#", end="")
				else: print(".", end="")
			else:
				print("%3d " % grid[i][j], end="")
				if grid[i][j] == n: count += 1
		print()
	print("Count of ", n, " is ", count)

#pgrid()
#print()

      # row       col     step  
nsteps=[[startrow, startcol, 0]]

done = False
NSTEPS = 64
#while steps and not done:
for d in range(1,NSTEPS+1):
	steps = copy.copy(nsteps)
	nsteps.clear()
	for s in steps:
		x = s[0]
		y = s[1]
		if s[2] > d: continue
		#if d > NSTEPS: continue
		#print()
		#print("[new xy}:", x,y)
		for dx, dy in [[-1,0], [1,0], [0, -1], [0, 1] ]:
			nx = x + dx
			ny = y + dy
			#print(nx, ny, d)
			if grid[nx][ny] < 0 : continue
			#
			# check if we've been to this point before - ignore if on even days
			##
			## if we are on an odd day - we don't need to move to an odd grid number
			## if we are on an even day - we don't need to move to an even grid number
			if d % 2 == 1 and grid[nx][ny] % 2 == 1:  #ignore
				pass
			elif d % 2 == 0 and grid[nx][ny] % 2 == 0 and not (grid[nx][ny] == 0):  #ignore
				pass
			else:
				grid[nx][ny] = d
				#print("grid[",nx,",",ny,"] step: ", d)
				nsteps.append([nx, ny, d])
			#else:
			#	grid[nx][ny] = NSTEPS
		#if d > 8: done = True

print("Part 1: Number of gardens visited is: ", numeves())

## 26501365 = 5 * 11 * 481843


NSTEPS = 55
#while steps and not done:
for d in range(1,NSTEPS+1):
	steps = copy.copy(nsteps)
	nsteps.clear()
	for s in steps:
		x = s[0]
		y = s[1]
		if s[2] > d: continue
		#if d > NSTEPS: continue
		#print()
		#print("[new xy}:", x,y)
		for dx, dy in [[-1,0], [1,0], [0, -1], [0, 1] ]:
			nx = x + dx
			ny = y + dy
			#print(nx, ny, d)
			if grid[nx][ny] < 0 : continue
			#
			# check if we've been to this point before - ignore if on even days
			##
			## if we are on an odd day - we don't need to move to an odd grid number
			## if we are on an even day - we don't need to move to an even grid number
			if d % 5 == 0 and grid[nx][ny] % 5 == 0 and not (grid[nx][ny] == 0):  #ignore
				pass
			elif d % 2 == 0 and grid[nx][ny] % 2 == 0 and not (grid[nx][ny] == 0):  #ignore
				pass
			else:
				grid[nx][ny] = d
				#print("grid[",nx,",",ny,"] step: ", d)
				nsteps.append([nx, ny, d])
			#else:
			#	grid[nx][ny] = NSTEPS
		#if d > 8: done = True
print("Part 1: Number of gardens visited is: ", nummults(5) + nummults(11) + NSTEPS)
