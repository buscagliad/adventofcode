
import numpy as np

import copy

grid = np.zeros([200,200], dtype = int)
gridCol = 0
gridRow = 0

def numeves(g, n = 1000000000000000):
  count = 0
  for i in range(gridRow):
    for j in range(gridCol):
      if g[i][j] > 0 and g[i][j] % 2 == 0 and g[i][j] <= n:
        count += 1
  return count
  
def numodds(g, n = 1000000000000000):
  count = 0
  for i in range(gridRow):
    for j in range(gridCol):
      if g[i][j] > 0 and g[i][j] % 2 == 1 and g[i][j] <= n:
        count += 1
  return count
  
def nummults(g, n):
  count = 0
  for i in range(gridRow):
    for j in range(gridCol):
      if g[i][j] > 0 and g[i][j] % n == 0:
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
sgrid = copy.copy(grid)

def pgrid(g, gRow, gCol, n = 0, flat = True):
  count = 0
  for i in range(gRow):
    for j in range(gCol):
      if flat:
        if g[i][j] > 1 and g[i][j] %2 == 0: 
          print("O", end="")
          count += 1
        elif g[i][j] < 0: print("#", end="")
        else: print(".", end="")
      else:
        print("%3d " % g[i][j], end="")
        if g[i][j] == n: count += 1
    print()
  print("Count of ", n, " is ", count)

#pgrid()
#print()
def zout(g):
  for i in range(gridCol):
    for j in range(gridRow):
      if g[i][j] >= 0: g[i][j] = 0

## 26501365 = 5 * 11 * 481843
def newGrid(urdl):
  g = copy.copy(sgrid)
  zout(g)
  stps = []
  if urdl == RIGHT:
    for i in range(gridCol):
      g[i][gridCol-1] = 1
      steps.append([i, gridCol-1, 1])
  elif urdl == LEFT:
    for i in range(gridCol):
      g[i][0] = 1
      stps.append([i, 0, 1])
  elif urdl == UP:
    for i in range(gridRow):
      g[0][i] = 1
      stps.append([0, i, 1])
  elif urdl == DOWN:
    for i in range(gridRow):
      g[gridRow-1][i] = 1
      stps.append([gridRow-1, i, 1])
  """ Function doc """
  pgrid(g, gridRow, gridCol, 0, False)
  done = False
  while stps:
    #print(stps)
    x, y, d = stps.pop()
    for dx, dy in [[-1,0], [1,0], [0, -1], [0, 1] ]:
      nx = x + dx
      ny = y + dy
      if nx < 0 or nx >= gridRow: continue
      if ny < 0 or ny >= gridCol: continue
      #print(nx, ny, d)
      if g[nx][ny] < 0 : continue
      #
      # check if we've been to this point before - ignore if on even days
      g[nx][ny] = d
      stps.append([nx, ny, d+1])
  return g

#ng = newGrid(LEFT)
#pgrid(ng, gridRow, gridCol, 0, False)
#exit(2)

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
      # grid[nx][ny] = NSTEPS
    #if d > 8: done = True

print("Part 1: Number of gardens visited is: ", numeves(grid))


## also note that the grid is 131 x 131, 131 is a prime number!

## So, all garden spots that are 5 or 11 or 481843 steps away can be counted,
## as you can go there (1 - then return back to home and return as many times 
## as needed since these are all ODD numbers. Meaning all garden spots that are 
## an odd number of spots away can be ultimately landed on.


NSTEPS = 100000
NDUPS = 9

GMUL = NDUPS//2
# row       col     step  
nsteps=[[startrow+GMUL*gridRow, startcol+GMUL*gridCol, 0]]
steps = copy.copy(nsteps)

# make grid2
grid2 = np.zeros([NDUPS*gridRow, NDUPS*gridCol],dtype=int)
for i in range(gridRow):
  for j in range(gridCol):
    v = sgrid[i][j]
    for ki in range(NDUPS):
      for kj in range(NDUPS):
        grid2[i + ki * gridRow][j + kj * gridCol] = v
gridRow *= NDUPS
gridCol *= NDUPS

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
      if nx < 0 or nx >= gridRow: continue
      if ny < 0 or ny >= gridCol: continue
      #print(nx, ny, d)
      if grid2[nx][ny] < 0 : continue
      #
      # check if we've been to this point before - ignore if on even days
      if d % 2 == 0 and grid2[nx][ny] > 0 and grid2[nx][ny] % 2 == 0 :  #ignore
        pass
      else:
        if grid2[nx][ny] == 0: grid2[nx][ny] = d
        #print("grid[",nx,",",ny,"] step: ", d)
        nsteps.append([nx, ny, d])


def gridout():
  for i in range(gridCol):
    print(grid2[i][0], end="")
    for j in range(1, gridRow):
      print(",",grid2[i][j], end="")
    print()

##
## Clue - there is a 65 diamond in the input grid
##        and 26501365 mod 131 = 65
##        and 26501365 = 202300 * 131 + 65
##
## Have no idea what to do with this - but - it is something
##
## Also, from the 'S' there are no '#'s up/down or left/right to it
## I'm guessing the '#'s are not so grouped to prevent a 65 to
## this center diamond
##
## I'm going to assume as the path's go out infinitely, we'll see a diamond of 65 * 2, the 65 * 3 ... 
## all the way up to 202300 * 65 - going to test this
##
## NO - the pattern is there is a diamond at 65 + 131 * N (for N = 0,...)
##
##
## So, we have that all steps up to 202300 are contained in a diamond
##
## I'm going to assume that there exists a function F(k) = A K^2 + B K + C
## Where F(k) represents the number of odd steps contained in the diamond 
## centered at S and radiating out to 65 + 131 * k
##
## I will compute F(0), F(1) and F(2) and find A, B and C
## BTW - i have no justification for this - but - if this problem does not
## have a solution of this nature - I have no idea what to make of it
## I tried several things (see notes below), i assumed there was an odd
## solution for F and an even (e.g., for k = 2*n) solution, and this is what
## the F's at even k's were from my input.
##
## F(0) = 3606
## F(2) = 89460
## F(4) = 289514
##
## Solving for A, B and C yields:
##
## I'm actually going to do the math for this inside my Python code:
##
K = np.array((0, 2, 4))
#Soln = np.zeros(3)


M = np.array([[0,0,1],[4,2,1],[16,4,1]]) # This is the polynomial matrix for k = 0, 2, and 4
b = np.array([numodds(grid2, 65), numodds(grid2, 65 + 2 * 131), numodds(grid2, 65 + 4 * 131)])
Soln = np.linalg.solve(M, b)
A = int(Soln[0])
B = int(Soln[1])
C = int(Soln[2])

##
## We need to compute F(202300)
##
## 596857212809306 was the answer - it ways it is too HIGH :(
##
## 563135273933257 is new number - guess what - it's too LOW :(
##
## At least i know the bounds
##
def part2(k):
  return A * k * k + B * k + C
  
print("Part 2: Number of plots visited in 26501365 steps: ", part2(202300))

'''
Part 1: Number of gardens visited is:  3503
Part 2: Number of gardens visited is:  EVEN:  106   ODD:  90
Part 2: Number of gardens visited for k =  0  is:  ODDS:  3606
Part 2: Number of gardens visited for k =  1  is:  ODDS:  31949
Part 2: Number of gardens visited for k =  2  is:  ODDS:  89460
Part 2: Number of gardens visited for k =  3  is:  ODDS:  174491
Part2:  596857212809306
Part2: F(0)  3606
Part2: F(1)  31949
Part2: F(2)  89460
Part2: F(3)  176139
Row:  917   Col:  917

It appears my polynomial is over estimating by 176139 - 174491 = 1648

Is there something special about k = 0??
I'm going to solve for F(1), F(2) and F(3)

Part 1: Number of gardens visited is:  3503
Part 2: Number of gardens visited is:  EVEN:  106   ODD:  90
Part 2: Number of gardens visited for k =  0  is:  ODDS:  3606
Part 2: Number of gardens visited for k =  1  is:  ODDS:  31949
Part 2: Number of gardens visited for k =  2  is:  ODDS:  89460
Part 2: Number of gardens visited for k =  3  is:  ODDS:  174491
Part2:  596857212809306
Part2: F(0)  3606
Part2: F(1)  31949
Part2: F(2)  89460
Part2: F(3)  176139
Row:  917   Col:  917
917 = 

Is there a different formulat for k = EVEN vs. k = ODD?

Going to get F(4) and compute that polynomial


Part 1: Number of gardens visited is:  3503
Part 2: Number of gardens visited is:  EVEN:  106   ODD:  90
Part 2: Number of gardens visited for k =  0  is:  ODDS:  3606
Part 2: Number of gardens visited for k =  1  is:  ODDS:  31949
Part 2: Number of gardens visited for k =  2  is:  ODDS:  89460
Part 2: Number of gardens visited for k =  3  is:  ODDS:  174491
Part 2: Number of gardens visited for k =  4  is:  ODDS:  289514
Part 2: Number of gardens visited for k =  5  is:  ODDS:  402891
Part2:  596857212809306
Part2: F(0)  3606
Part2: F(1)  31949
Part2: F(2)  89460
Part2: F(3)  176139
Row:  1179   Col:  1179


'''
