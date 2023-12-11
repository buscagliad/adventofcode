
from copy import deepcopy
import numpy as np

galaxy = np.zeros([2000,2000], dtype = int)

row_g = 0
col_g = 0
galaxy_id = 0

def process(line):
	global galaxy
	global row_g
	global col_g
	global galaxy_id
	j = 0
	for a in line:
		if a == '#':
			galaxy_id += 1
			galaxy[row_g][j] = galaxy_id
		elif a == '.': pass
		else: break
		if row_g == 0: col_g += 1
		j += 1
	row_g += 1

for line in open('data.txt', 'r'):
	process(line)

def pgal(galaxy, row_g, col_g):
	for i in range(row_g):
		for j in range(col_g):
			g = galaxy[i][j]
			if g > 0:
				print('{:>4}'.format(g), end="")
			else:
				print("    ", end="");
		print()

row_offset = np.zeros(2000, dtype = int)
col_offset = np.zeros(2000, dtype = int)
row_sums = np.zeros(2000, dtype = int)
col_sums = np.zeros(2000, dtype = int)

for i in range(row_g):
	for j in range(col_g):
		row_sums[i] += galaxy[i][j]
		col_sums[j] += galaxy[i][j]
exp = 0
for i in range(row_g):
	if row_sums[i] == 0:
		exp += 1
	row_offset[i] = exp
exp = 0
for i in range(row_g):
	if col_sums[i] == 0:
		exp += 1
	col_offset[i] = exp

egals=[]
for i in range(row_g):
	for j in range(col_g):
		gid = galaxy[i][j]
		if gid > 0:
			egals.append([i + row_offset[i], j + col_offset[j], gid])

dist = 0
for i in range(len(egals)):
	for j in range(i,len(egals)):
		dist += abs(egals[i][0]-egals[j][0]) + abs(egals[i][1]-egals[j][1])

print("Part 1: ", dist)

#
# Part II
#
egals2=[]
GALAXY_EXPANSION = 999999
for i in range(row_g):
	for j in range(col_g):
		gid = galaxy[i][j]
		if gid > 0:
			egals2.append([i + GALAXY_EXPANSION*row_offset[i], 
			               j + GALAXY_EXPANSION*col_offset[j], gid])

dist = 0
for i in range(len(egals2)):
	for j in range(i+1,len(egals2)):
		dist += abs(egals2[i][0]-egals2[j][0]) + abs(egals2[i][1]-egals2[j][1])

print("Part 2: ", dist)
