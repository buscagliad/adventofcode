
import numpy as np
import copy

def getarray(f):
	arr = []
	line = f.readline()
	if line == '':
		return arr
	while len(line) > 3:
		arr.append(line.strip())
		line = f.readline()
	return arr


def movenorth(z):
	M, N = np.shape(z)
	cnt = 0
	for i in range(M-1):  # for each for - for up the row below
		for j in range(N):
			if z[i+1][j]  > 0 and z[i][j] == 0:
				z[i][j] = z[i+1][j]
				z[i+1][j] = 0
				cnt += 1
	if cnt > 0: movenorth(z)

def movesouth(z):
	M, N = np.shape(z)
	cnt = 0
	for i in range(M-2, -1, -1):  # for each row - move item down
		for j in range(N):
			if z[i][j] > 0 and z[i+1][j] == 0:
				z[i+1][j] = z[i][j]
				z[i][j] = 0
				cnt += 1
	if cnt > 0: movesouth(z)

def movewest(z):
	M, N = np.shape(z)
	cnt = 0
	for j in range(M-1): # for each column - move left
		for i in range(N):  
			if z[i][j] == 0 and z[i][j+1] > 0:
				z[i][j] = z[i][j+1]
				z[i][j+1] = 0
				cnt += 1
	if cnt > 0: movewest(z)

def moveeast(z):
	M, N = np.shape(z)
	cnt = 0
	for j in range(M-1): # for each column - move right
		for i in range(N):  
			if z[i][j+1] == 0 and z[i][j] > 0:
				z[i][j+1] = z[i][j]
				z[i][j] = 0
				cnt += 1
	if cnt > 0: moveeast(z)

def dosum(z):
	s = 0
	M, N = np.shape(z)
	for i in range(M):  # for each for - for up the row below
		for j in range(N):
			if z[i][j] > 0 :
				s += M - i
	return s

class Rock:
	def __init__(self, i, j, ix):
		self.i = i
		self.j = j
		self.ix = ix

def load(gl):
	z = np.zeros([len(gl),len(gl[0])])
	rs = 0
	d = 0
	r = len(gl)
	rocklist=[]
	index = 1
	for i, g in enumerate(gl):
		for j, rock in enumerate(g):
			if rock == 'O':
				rocklist.append(Rock(i, j, index))
				index += 1
				z[i][j] = 1
			elif rock == '#':
				z[i][j] = -1

				
				
	M, N = np.shape(z)
	# for i in range(len(z)):
		# for j in range(
		# if z
	return z

firstCycle = True
def cycle(z, out=False):
	global firstCycle
	movenorth(z)
	if out: pz("After moving North", z)
	if firstCycle:
		print("Part 1: north load is: ", dosum(z))
		firstCycle = False
	movewest(z)
	if out: pz("After moving West", z)
	movesouth(z)
	if out: pz("After moving South", z)
	moveeast(z)
	if out: pz("After moving East", z)

def pz(t, z):
	M, N = np.shape(z)
	print(t)
	for i in range(M): # for each column - move right
		for j in range(N):  
			if z[i][j] == 0 : print(".", end="", sep="")
			elif z[i][j] < 0 : print("#", end="", sep="")
			else: print("O", end="", sep="")
		print()
	print()
	print()


mem = {}
def state(z):
	s = str()
	for i in range(len(z)):
		for j in range(len(z[0])):
			if z[i][j] == 1:
				s += str(i)+str(j)
	return s
				
	
def seen(z, v):
	global mem
	s = state(z)
	if s in mem:
		nv = mem[s]
		cycle = v - nv
		modn = (1000000000 - nv) % cycle
		return modn
	else:
		mem[s] = v
	return 0

	

f = open('data.txt', 'r')

g = getarray(f)

z = load(g)

	

cycleCount = 0
while True:
	cycleCount += 1
	cycle(z)
	n = seen(z, cycleCount)
	if n > 1: 
		for i in range(n):
			cycle(z)
		print("Part 2:  billionth cycle yields a north load of: ", dosum(z))
		break



'''
Each dot must have a pattern as the container rotates
Say each dot that returns to where they started to have a zero cycle
'''
