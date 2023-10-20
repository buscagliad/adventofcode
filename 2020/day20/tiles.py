import math
import numpy as np
import collections


def findedge(tiles, excTile, thisedge):
	#print("findedge: ", thistile.num, " side: ", thisedge)
	for t in tiles:
		if t.num == excTile or t.used:
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
	for i in arr: #rs += chr((ord(i) + c - 65) % 26 + 65)
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
		self.rows = np.zeros(shape=(10,10),dtype="S1")
		for i in range(10):
			for j, r in enumerate(f.readline().strip()):
				self.rows[i][j] = r
		f.readline()
		self.side = []
		self.xside = [False]*4 # initially no matching side found
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
		self.type = 0  # unknown type (4 = interior, 2 = corner, 3 = edge
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
		print("   ", self.side[0])
		row = 0
		for r in self.rows:
			print(self.side[3][row], " ", tostring(r), " ", self.side[1][row])
			row += 1
		print("   ", self.side[2])
		print(" ")

	def block(self):
		print("Tile: ", self.num, "  CW: ", self.cw, "  Flipped: ", self.flipped)
		for r in self.rows[1:9]:
			print(" ", tostring(r)[1:9])
		print(" ")

	def mark(self, tiles):
		count = 0
		excTile = self.num
		for s in range(len(self.side)):
			if findedge(tiles, excTile, self.side[s]): 
				count+= 1
				self.xside[s] = True
			else:
				self.xside[s] = False
		#print("Tile: ", self.num, " sides that have a match ", count, " sides")
		self.type = count	# 2 is corner, 3 is edge, 4 is interior


	def rotate(self, cw):
		self.cw += cw
		self.cw %= 4
		if (cw == 0):
			return
		self.rows = np.rot90(self.rows, k=cw, axes=(1,0))
		for j in range(cw):
			save = self.side[0]
			self.side[0] = self.side[3][::-1]
			self.side[3] = self.side[2]
			self.side[2] = self.side[1][::-1]
			self.side[1] = save
				
	def flip(self, horz = True):
		self.flipped = True;
		if horz : 
			self.rows = np.fliplr(self.rows)
			save = self.side[1]
			self.side[1] = self.side[3]
			self.side[3] = save
			self.side[2] = self.side[2][::-1]
			self.side[0] = self.side[0][::-1]
		else : 
			self.rows = np.flipud(self.rows)
			save = self.side[0]
			self.side[0] = self.side[2]
			self.side[2] = save
			self.side[3] = self.side[3][::-1]
			self.side[1] = self.side[1][::-1]


	def orientToSide(self, side, sno):
		f = False
		found = False
		for flipped in [False, True]:
			for r in range(4):
				if self.side[sno] == side:
					found = True
					break
				self.rotate(1)
			if found : break
			self.flip(True)
		if not found:
			print("ERROR - requested side: ", side, " not in this tile: ", self.num)


	
	def hasSide(self, s, dbg = False):
		found = False
		rot = -1
		flip = False
		for r in range(4):
			if (dbg) : print (r, self.side[r], self.side[r][::-1], s, sep = " ")
			if self.side[r] == s:
				found = True
				rot = r
				flip = False
				break
			if self.side[r][::-1] == s:
				found = True
				flip = True
				rot = r
				break
		if (dbg) : print ("found", found, "rot", rot, "flip", flip, sep = " ")
		return found, rot, flip


##
## addTiles will find a tile that matches two sides
## top, right, bottom and/or left.  Only two of these
## will NOT be None and the found tile will be rotated/
## flipped as required to match, then added to the grid
## 
def addTiles(grid, r, c, t, glo):
	glo.append((t.num, t.cw, t.flipped))
	for i in range(8):
		for j in range(8):
			gc = 8*(c) + i
			gr = 8*(r) + j
			if t.rows[j+1][i+1] == b'#': grid[gr][gc] = 1


def countObjects(grid, obj):
	objx, objy = np.shape(obj)
	numobj = sum(sum(obj))
	gx, gy = np.shape(grid)
	count = 0
	for x in range(gx-objx):
		for y in range(gy-objy):
			#print("sub-grid ", objx, x, objy, y, np.shape(grid[x:objx+x,y:objy+y]))
			do_sum = sum(sum(obj*grid[x:objx+x,y:objy+y]))
			if (do_sum == numobj) : count += 1
			#print (x, y, do_sum)
	return count


tiles = []
f = open("data.txt", "r")
l = f.readline()
while not l == "":
	tiles.append(Tile(f, l))
	l = f.readline()

def	getSides(tiles, n):
	for t in tiles:
		if t.num == n: return t.side
	return None

prod = 1
corners = []
for t in tiles:
	t.mark(tiles)
	if (t.type == 2) : 
		prod *= t.num ## Part 1 corner product
		corners.append(t)
		



print("Part 1: Product is: ", prod)



##
## needed for Part 2
numpixels = math.floor(math.sqrt(len(tiles)) + 0.5)
puzzle = np.zeros((numpixels, numpixels))
c = 0  # first corner

grid = np.zeros((numpixels*8,numpixels*8),dtype=int)
gridLayOut = []


##
## start with the corners:
## -- all corners are type 2
## -- start with the first corner, rotate it until it is
## -- False, True, True, False 
##
## Build Frame, orient first corner at the upper left

##
## Get upper left corner
##
if corners[0].xside == [False, False, True, True]:
	corners[0].rotate(3)
elif corners[0].xside == [True, False, False, True]:
	corners[0].rotate(2)
elif corners[0].xside == [True, True, False, False]:
	corners[0].rotate(1)


row = 0
col = 0
side = corners[0].side[1]
addTiles(grid, row, col, corners[0], gridLayOut)
corners[0].used = True
found = False
snum = 0

def rcnum(r, c, nump):
	return r * nump + c

#
# at this point, we have built the edges of the 'puzzle'
#
for r in range(numpixels):
	if r > 0:
		sides = getSides(tiles, gridLayOut[rcnum(r-1,0,numpixels)][0])
		side = sides[2]
		snum = 3
	for c in range(numpixels):
		if r == 0 and c == 0: continue
		if c == 0:
			snum = 0  # match the top
		else : 
			snum = 3
		for t in tiles:
			if t.used: continue
			found, rot, flip = t.hasSide(side)
			if found:
				t.used = True
				t.orientToSide(side, snum)
				addTiles(grid, r, c, t, gridLayOut)
				side = t.side[1]
				break

monster = np.zeros((3,20),dtype=int)
# 01234567890123456789
#0                  # 
#1#    ##    ##    ###
#2 #  #  #  #  #  #   
monster[0][18] = 1
for j in (0,5,6,11,12,17,18,19) : monster[1][j] = 1
for j in (1,4,7,10,13,16) : monster[2][j] = 1
monsterSize = sum(sum(monster))

totaldots = sum(sum(grid))


for i in range(4):
	m = countObjects(grid, monster)
	if m > 0: numMonsters = m
	monster = np.rot90(monster)

monster = np.rot90(monster)
monster = np.fliplr(monster)
for i in range(4):
	m = countObjects(grid, monster)
	if m > 0: numMonsters = m
	monster = np.rot90(monster)


print("Part 2: Number of non-serpant pixels is: ", totaldots - monsterSize * numMonsters)

