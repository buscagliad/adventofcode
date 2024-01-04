
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

LEFT=1
UP=2
RIGHT=3
DOWN=4

NOT_SET = -1

minloss = 10000

def mindval(g, s, nx, ny, x, y):
	rv = False;
	sumv = 0;
	if not (s[x][y] == NOT_SET):
		if (x - 1 >= 0): #  LEFT
			sumv = s[x][y] + g[x-1][y]
			if (sumv < s[x-1][y]) or s[x-1][y] == NOT_SET:
				s[x-1][y] = sumv
				rv = True

		if (x + 1 < nx): # RIGHT
			sumv = s[x][y] + g[x+1][y]
			if (sumv < s[x+1][y]) or (s[x+1][y] == NOT_SET) :
				s[x+1][y] = sumv
				rv = True
				
		if (y - 1 >= 0) : # ABOVE
			sumv = s[x][y] + g[x][y-1]
			if ( (sumv < s[x][y-1]) or (s[x][y-1] == NOT_SET) ) :
				s[x][y-1] = sumv
				rv = True

		if (y + 1 < ny) : #  BELOW
			sumv = s[x][y] + g[x][y+1]
			if ( (sumv < s[x][y+1]) or (s[x][y+1] == NOT_SET) ) :
				s[x][y+1] = sumv
				rv = True
	return rv


#state = [i, j, total, dir, numd]
def route(g, s, nx, ny):
	save_first = g[0][0]
	g[0][0] = 0
	s[0][0] = 0
	done = False
	while (not done):
		done = True
		for x in range(nx):
			for y in range(ny):
				if (mindval(g, s, nx, ny, x, y)):
					done = False
	return s[nx-1][ny-1]


def zerodata(): 
	global grid
	global sgrid
	for i in range(MAXX):
		for j in range(MAXY): 
			grid[i][j] = 0
			sgrid[i][j] = NOT_SET
	

'''
bool mindval(int g[MAXX][MAXY], int s[MAXX][MAXY], int nx, int ny, int x, int y)
{
	bool	rv = false;
	int	sumv = 0;
	if (s[x][y] != NOT_SET)
	{
        if (x - 1 >= 0) // LEFT
        {
            sumv = s[x][y] + g[x-1][y];
            if ( (sumv < s[x-1][y]) || (s[x-1][y] == NOT_SET) )
            {
                s[x-1][y] = sumv;
                rv = true;
            }
        }
        if (x + 1 < nx) // RIGHT
        {
            sumv = s[x][y] + g[x+1][y];
            if ( (sumv < s[x+1][y]) || (s[x+1][y] == NOT_SET) )
            {
                s[x+1][y] = sumv;
                rv = true;
            }
        }
        if (y - 1 >= 0) // ABOVE
        {
            sumv = s[x][y] + g[x][y-1];
            if ( (sumv < s[x][y-1]) || (s[x][y-1] == NOT_SET) )
            {
                s[x][y-1] = sumv;
                rv = true;
            }
        }
        if (y + 1 < ny) // BELOW
        {
            sumv = s[x][y] + g[x][y+1];
            if ( (sumv < s[x][y+1]) || (s[x][y+1] == NOT_SET) )
            {
                s[x][y+1] = sumv;
                rv = true;
            }
        }
	}
	return rv;
}

int route(int g[MAXX][MAXY], int s[MAXX][MAXY], int nx, int ny)
{
	save_first = g[0][0];
	g[0][0] = 0;
	s[0][0] = 0;
	bool done = false;
	while (!done)
	{
		done = true;
		for (int x = 0; x < nx; x++)
		{
			for (int y = 0; y < ny; y++)
			{
				if (mindval(g, s, nx, ny, x, y))
				    done = false;
			}
			//outgrid(g, nx, ny);
		}
	}
	return s[nx-1][ny-1];
}

void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    for(int j = 0; j < MAXY; j++)
	    {
			g_grid[i][j] = 0;
			s_grid[i][j] = NOT_SET;	// set the sum-path to not be set
		}
	xpts = 0;
	ypts = 0;
	
}
'''

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
		#if left > 3: continue
		#if right > 3: continue
		#if up > 3: continue
		#if down > 3: continue
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
for l in open("test.txt"):
	line = l.strip()
	if len(line) < 2: break
	gridCol = len(line)
	i = 0
	for d in line:
		if d.isdigit():
			grid[gridRow][i] = int(d)
			i += 1
	gridRow += 1

c = crucible()

print("Part 1: crucible min path is: ", c)
