import numpy as np


class cube3:
	def __init__(self, filename):
		z = 0
		y = 0
		do_once = True
		self.cycle = 0
		for line in open(filename, "r") :
			if len(line) < 2 : continue
			#print(line)
			self.xsize = len(line) - 1
			self.ysize = len(line) - 1
			self.zsize = 1
			if do_once:
				do_once = False
				self.arr = np.zeros([self.xsize, self.ysize, self.zsize], np.int8)
			x = 0
			for c in line :
				#print (c)
				if c == '#' : 
					self.arr[x,y,z] = 1
					#print(x, y, z, "  set to 1")
				elif c == '.': 
					self.arr[x,y,z] = 0
					#print(x, y, z, "  set to 0")
				x += 1
			y += 1
	
	def get(self, x, y, z):
		if x < 0 or y < 0 or z < 0 : return 0
		if x >= self.xsize or y >= self.ysize or z >= self.zsize : return 0
		return self.arr[x,y,z]

	def numNeighbors(self, x, y, z):
		numactive = 0
		for dz in [-1, 0, 1]:
			zi = z + dz
			for dy in [-1, 0, 1]:
				yi = y + dy
				for dx in [-1, 0, 1]:
					if dz == 0 and dy == 0 and dx == 0 : continue
					xi = x + dx
					numactive += self.get(xi,yi,zi)
		return numactive
		
	def display(self, do_print = True):
		if do_print: print("Cycle:", self.cycle)
		numactive = 0
		for z in range(self.zsize) :
			if do_print : print ("z = ", z - self.cycle)
			for y in range(self.ysize) :
				line = ""
				for x in range(self.xsize) : 
					if self.arr[x,y,z] == 1 : 
						line += '#'
						numactive += 1
					else : line += '.'
				if do_print : print (line)
		if do_print : print ("Number active is: ", numactive)
		return numactive
	
	def numActive(self) :
		return self.display(False)

	def getState(self, x, y, z):
		numactive = self.numNeighbors(x,y,z)
		if self.get(x,y,z):
			if numactive == 2 or numactive == 3 : return 1
			return 0
		else :
			if numactive == 3 : return 1
			return 0

	def doCycle(self):
		self.cycle += 1
		xsize = self.xsize + 2
		ysize = self.ysize + 2
		zsize = self.zsize + 2

		arr = np.zeros([xsize, ysize, zsize], np.int8) # New array
		for z in range(zsize) :
			for y in range(ysize) :
				for x in range(xsize) :
					arr[x,y,z] = self.getState(x-1, y-1, z-1)
		self.arr = arr
		self.xsize = xsize
		self.ysize = ysize
		self.zsize = zsize


class cube4:
	def __init__(self, filename):
		z = 0
		y = 0
		w = 0
		do_once = True
		self.cycle = 0
		for line in open(filename, "r") :
			if len(line) < 2 : continue
			#print(line)
			self.xsize = len(line) - 1
			self.ysize = len(line) - 1
			self.zsize = 1
			self.wsize = 1
			if do_once:
				do_once = False
				self.arr = np.zeros([self.xsize, self.ysize, self.zsize, self.wsize], np.int8)
			x = 0
			for c in line :
				#print (c)
				if c == '#' : 
					self.arr[x,y,z,w] = 1
					#print(x, y, z, "  set to 1")
				elif c == '.': 
					self.arr[x,y,z,w] = 0
					#print(x, y, z, "  set to 0")
				x += 1
			y += 1
	
	def get(self, x, y, z, w):
		if x < 0 or y < 0 or z < 0 or w < 0: return 0
		if x >= self.xsize or y >= self.ysize or z >= self.zsize  or w >= self.wsize: return 0
		return self.arr[x,y,z,w]

	def numNeighbors(self, x, y, z, w):
		numactive = 0
		for dw in [-1, 0, 1]:
			wi = w + dw
			for dz in [-1, 0, 1]:
				zi = z + dz
				for dy in [-1, 0, 1]:
					yi = y + dy
					for dx in [-1, 0, 1]:
						if dz == 0 and dy == 0 and dx == 0 and dw == 0: continue
						xi = x + dx
						numactive += self.get(xi,yi,zi,wi)
		return numactive
		
	def display(self, do_print = True):
		if do_print: print("Cycle:", self.cycle)
		numactive = 0
		for w in range(self.wsize) :
			for z in range(self.zsize) :
				if do_print : print ("z = ", z - self.cycle, "  w = ", w - self.cycle)
				for y in range(self.ysize) :
					line = ""
					for x in range(self.xsize) : 
						if self.arr[x,y,z,w] == 1 : 
							line += '#'
							numactive += 1
						else : line += '.'
					if do_print : print (line)
		if do_print : print ("Number active is: ", numactive)
		return numactive
	
	def numActive(self) :
		return self.display(False)

	def getState(self, x, y, z, w):
		numactive = self.numNeighbors(x,y,z,w)
		if self.get(x,y,z,w):
			if numactive == 2 or numactive == 3 : return 1
			return 0
		else :
			if numactive == 3 : return 1
			return 0

	def doCycle(self):
		self.cycle += 1
		xsize = self.xsize + 2
		ysize = self.ysize + 2
		zsize = self.zsize + 2
		wsize = self.wsize + 2

		arr = np.zeros([xsize, ysize, zsize, wsize], np.int8) # New array
		for w in range(wsize) :
			for z in range(zsize) :
				for y in range(ysize) :
					for x in range(xsize) :
						arr[x,y,z,w] = self.getState(x-1, y-1, z-1, w-1)
		self.arr = arr
		self.xsize = xsize
		self.ysize = ysize
		self.zsize = zsize
		self.wsize = wsize

c = cube3("data.txt")
for i in range(6) :
	#c.display()
	c.doCycle()
#c.display()
print("Part 1 - Number of active cubes after six cycles: ", c.numActive())


c = cube4("data.txt")
for i in range(6) :
	#c.display()
	c.doCycle()
#c.display()
print("Part 2 - Four-D cubes, number of active cubes after six cycles: ", c.numActive())

