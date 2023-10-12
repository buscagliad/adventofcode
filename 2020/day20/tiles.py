import math
import numpy as np
import collections

def hasedge(edge, edges):
	for e in edges:
		if edge == e: return True
		if edge == e[::-1]: return True
	return False

def findtiles(side, tiles):
	tlist = []
	if side == None: return tlist
	for t in tiles:
		if hasedge(side, t.side) : tlist.append(t.num)
	return tlist

def findedge(thistile, s, tiles):
	thisedge = thistile.side[s]
	#print("findedge: ", thistile.num, " side: ", thisedge)
	for t in tiles:
		if thistile.num == t.num: 
			#print("findedge skipping for ", t.num)
			continue
		for e in t.side:
			if thisedge == e[::-1]: 
				#print("Tile: ", t.num, " matches with ~edge: ", e)
				return True
			if thisedge == e: 
				#print("Tile: ", t.num, " matches with edge: ", e)
				return True
	return False

def displaytiles(tiles):
	for s in range(len(tiles)):
		tiles[s].displayedges()

def tostring(arr):
	rs = ""
	for i in arr:
		if i == b'#':
			rs += '#'
		else:
			rs += '.'
	return rs

class Tile:
	def __init__(self, f, tline):
		line = tline.split(" ")
		#print(line)
		self.num = int(line[1].strip(":\n"))
		#print("Number: ", self.num)
		self.rows = np.zeros(shape=(10,10),dtype=np.character)
		for i in range(10):
			for j, r in enumerate(f.readline().strip()):
				self.rows[i][j] = r
		f.readline()
		self.side = []
		self.xside = [False]*4
		top = ""
		right = ""
		bottom = ""
		left = ""
		for i in range(10):
			if self.rows[0][i] == b'#':
				top += '#'
			else:
				top += '.'
			if self.rows[i][9] == b'#':
				right += '#'
			else:
				right += '.'
			if self.rows[9][i] == b'#':
				bottom += '#'
			else:
				bottom += '.'
			if self.rows[i][0] == b'#':
				left += '#'
			else:
				left += '.'
		self.side.append(top)
		self.side.append(right)
		self.side.append(bottom)
		self.side.append(left)
		#print(self.side)
		self.type = 0  # unknown type
		self.rrows = self.rows.copy()
		self.used = False
		self.flipped = False # Not flipped
		self.cw = 0		# Not rotated

	def displayedges(self):
		print("Tile: ", self.num)
		print("  Left:", self.side[0], "   ~Left:", self.side[0][::-1])
		print("   Top:", self.side[1], "    ~Top:", self.side[1][::-1])
		print("Bottom:", self.side[2], " ~Bottom:", self.side[2][::-1])
		print(" Right:", self.side[3], "  ~Right:", self.side[3][::-1])

	def display(self):
		print("Tile: ", self.num, "  CW: ", self.cw, "  Flipped: ", self.flipped)
		for r in self.rows:
			print(tostring(r))
		print(" ")

	def mark(self, tiles):
		count = 0
		for s in range(len(t.side)):
			if findedge(self, s, tiles): 
				count+= 1
				self.xside[s] = True
			else:
				self.xside[s] = False
		#print("Tile: ", self.num, " sides that have a match ", count, " sides")
		self.type = count	# 2 is corner, 3 is edge, 4 is interior
	
	def swap(self, x1, y1, x2, y2):
		save = self.rows[x1][y1]
		self.rows[x1][y1] = self.rows[x2][y2]
		self.rows[x2][y2] = save

	def rotate(self, cw, firstcall = True):
		if firstcall : self.cw = cw
		if (cw == 0): return
		cw -= 1
		n = len(self.rows[0])
		for i in range(n):
			for j in range(i+1,n):
				self.swap(i, j, n-j, i)
		self.rotate(cw, False)
				
	def rotcount(self, tside):
		for cw in range(4):
			if tside == self.xside: return cw
			tside = tside[-1]+tside[0:3]
				
	def flip(self, horz = True):
		self.flipped = True;
		n = len(self.rows[0])
		for r in range(n):
			for c in range(n):
				if horz: self.rrows[i][j] = self.rows[n-i-1][j]
				else: self.rrows[i][j] = self.rows[i][n-j-1]
		return self.rrows
				
def findPiece(tiles, top, right, bottom, left):
	tlist = []
	needed = 0
	c = collections.Counter()
	if not top == None:
		t = findtiles(top, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not right == None:
		t = findtiles(right, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not bottom == None:
		t = findtiles(bottom, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not left == None:	
		t = findtiles(left, tiles)
		for i in t: c[i] += 1
		needed += 1
	
	for i in tlist:
		print(i)
		#c[i] += 1
	tn = c.most_common(1)[0][0]
	if tn == needed:
		print("Found tile: ", tn)
	print(c)


		
tiles = []
f = open("data.txt", "r")
l = f.readline()
while not l == "":
	tiles.append(Tile(f, l))
	l = f.readline()


#exit(1)

prod = 1

for t in tiles:
	t.mark(tiles)
	if (t.type == 2) : 
		prod *= t.num ## Part 1 corner product
		print(t.num, " ", t.xside)
		top = right = bottom = left = None
		if t.xside[0] : top = t.side[0]
		if t.xside[1] : right = t.side[1]
		if t.xside[2] : bottom = t.side[2]
		if t.xside[3] : left = t.side[3]
		findPiece(tiles, top, right, bottom, left)



print("Part 1: Product is: ", prod)


##
## needed for Part 2
numpixels = math.floor(math.sqrt(len(tiles)) + 0.5)
corners = []
corners.append([False,True,True,False])
corners.append([False,False,True,True])
corners.append([True,False,False,True])
corners.append([True,True,False,False])
puzzle = np.zeros((numpixels, numpixels))
c = 0  # first corner

##
## start with the corners:
##
for t in tiles:
	t.mark(tiles)
	if (t.type == 2) : 
		prod *= t.num
		print(t.num, " ", t.xside)


print("Part 2: Number of non-serpant pixels is: ", numpixels)

tiles[0].display()
for i in range(5):
	tiles[0].rotate(1)
	tiles[0].display()

