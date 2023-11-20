import numpy as np
import re
import copy

gridsize = 100
lights = np.zeros((100,100), dtype=np.int32)
lightsp2 = np.zeros((100,100), dtype=np.int32)

def count(lights):
	global gridsize
	on = 0
	for i in range(gridsize):
		for j in range(gridsize):
			if lights[i][j]: on += 1
	return on


def cnt(lights, i, j):
	global gridsize
	c = 0
	for k in range(-1, 2):
		x = i + k
		if x < 0 or x >= gridsize: continue
		for m in range(-1, 2):
			y = j + m
			if y < 0 or y >= gridsize: continue
			if k==0 and m==0: continue
			if lights[x][y] : c += 1
	return c

def step(lights):
	global gridsize
	rlights = copy.deepcopy(lights)
	#print("Turning off: ", ul, " thru ", br)
	for i in range(gridsize):
		for j in range(gridsize):
			n = cnt(lights, i, j)
			#print(i, j, " - ", n)
			if lights[i][j]:
				if n < 2 or n > 3:
					rlights[i][j] = 0
			else:
				if n == 3:
					rlights[i][j] = 1
	return rlights	


def pgrid(lights):
	global gridsize
	for i in range(gridsize):
		for j in range(gridsize):
			if lights[i][j]: print('#', sep="", end="")
			else: print('.', sep="", end="")
		print()
	print()

'''
turn off 199,133 through 461,193
toggle 322,558 through 977,958
turn on 226,196 through 599,390
'''
def do_line(line, n):
	global lights
	global lightsp2
	i = 0
	for a in line:
		if a == '#':
			lights[n][i] = 1
			lightsp2[n][i] = 1
		i += 1
			
n = 0
for line in open("data.txt", "r"):
	gridsize = len(line)-1
	do_line(line, n)
	n += 1


for i in range(100):
	lights = step(lights)

print("Part 1: there are ", count(lights), "lights on")


# Part 2

n = 0


for i in range(100):
	lightsp2 = step(lightsp2)
	lightsp2[0][0] = 1
	lightsp2[gridsize-1][0] = 1
	lightsp2[0][gridsize-1] = 1
	lightsp2[gridsize-1][gridsize-1] = 1
	
print("Part 2: there are ", count(lightsp2), "lights on")
