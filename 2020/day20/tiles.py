import math
import numpy as np
import collections



def hasedge(edge, edges):
	for e in edges:
		if edge == e: return True
		if edge == e[::-1]: return True
	return False

def findTileWithSide(side, tiles):
	tlist = []
	if side == None: return tlist
	for t in tiles:
		if t.used: continue
		if hasedge(side, t.side) : tlist.append(t.num)
	return tlist

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
		self.cw = cw
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

	def orientToSideOld(self, side, sno):
		f = False
		found = False
		for r in range(4):
			if self.side[r] == side:
				found = True
				break
			if self.side[r][::-1] == side:
				found = True
				f = True
				break
		if not found:
			print("ERROR - requested side: ", side, " not in this tile: ", self.num)

		# need to rotate sno - r
		cw = (sno - r + 4 ) % 4
		print("cw: ", cw, " r = ", r)
		self.rotate(cw)
		#self.display()
		if f and sno % 2: 
			print("Vertical flip")
			self.flip(True)
		elif f : 
			print("Horizontal flip")
			self.flip(True)
		#self.display()

	def orientToSide(self, side, sno):
		f = False
		found = False
		for r in range(4):
			if self.side[sno] == side:
				found = True
				break
			if self.side[sno][::-1] == side:
				found = True
				f = True
				break
			self.rotate(1)
		if not found:
			print("ERROR - requested side: ", side, " not in this tile: ", self.num)

		#self.display()
		if f:
			if sno % 2 == 1: 
				print("Vertical flip")
				self.flip(True)
			else: 
				print("Horizontal flip")
				self.flip(True)
		#self.display()
	
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
#
# find a tile with top, right, bottom and/or left matches
# return the tile number most found
#	
def findPiece(tiles, top, right, bottom, left):
	tlist = []
	needed = 0
	c = collections.Counter()
	if not top == None:
		t = findTileWithSide(top, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not right == None:
		t = findTileWithSide(right, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not bottom == None:
		t = findTileWithSide(bottom, tiles)
		for i in t: c[i] += 1
		needed += 1
		
	if not left == None:	
		t = findTileWithSide(left, tiles)
		for i in t: c[i] += 1
		needed += 1
	
	#for i in tlist:
		#print(i)
		#c[i] += 1
	tn, tc = c.most_common(1)[0]
	#tc = c.most_common(1)[0][0]
	#if tc == needed:
	#	print("Found tile: ", tn)
	#print("tn: ", tn, "tc: ", tc, " ", c)
	return tn

		
tiles = []
f = open("data.txt", "r")
l = f.readline()
while not l == "":
	tiles.append(Tile(f, l))
	l = f.readline()


#exit(1)

prod = 1
corners = []
edges = []
others = []
for t in tiles:
	t.mark(tiles)
	if (t.type == 2) : 
		prod *= t.num ## Part 1 corner product
		#print(t)
		corners.append(t)
		
		#print(t.num, " ", t.xside)
	elif (t.type == 3) :
		edges.append(t)
	else:
		others.append(t)


print("Part 1: Product is: ", prod)



##
## needed for Part 2
numpixels = math.floor(math.sqrt(len(tiles)) + 0.5)
print("Numpixels: ", numpixels)
upperLeftCorner = ([False,True,True,False])
upperRightCorner = ([False,False,True,True])
lowerRightCorner = ([True,False,False,True])
lowerLeftCorner = ([True,True,False,False])
puzzle = np.zeros((numpixels, numpixels))
c = 0  # first corner

##
## addTiles will find a tile that matches two sides
## top, right, bottom and/or left.  Only two of these
## will NOT be None and the found tile will be rotated/
## flipped as required to match, then added to the grid
## 
def addTiles(grid, x, y, t, glo):
	glo.append((t.num, t.cw, t.flipped))
	for i in range(1,9):
		for j in range(1,9):
			gx = 8*(x-1) + i
			gy = 8*(y-1) + j
			if t.rows[i][j] == b'#': grid[gx][gy] = 1

##
## builds grid from tiles
##
def createGridFromTiles(grid, tiles, puzzle, numpixels):
	for x in range(numpixels):
		for y in range(numpixels):
			addTiles(grid, x, y, tiles[x*numpixels + y])
##
## add tile to grid\
##
def addTileToGrid(grid, tile, x, y):
	for x in range(numpixels):
		for y in range(numpixels):
			addTiles(grid, x, y, tiles[x*numpixels + y])

##
## start with the corners:
## -- all corners are type 2
## -- start with the first corner, rotate it until it is
## -- False, True, True, False 
##
## Build Frame, orient first corner at the upper left

## corners[0].display()
##
## Get upper left corner
##
if corners[0].xside == [False, False, True, True]:
	corners[0].rotate(3)
elif corners[0].xside == [True, False, False, True]:
	corners[0].rotate(2)
elif corners[0].xside == [True, True, False, False]:
	corners[0].rotate(1)

grid = np.zeros((numpixels*8,numpixels*8),dtype=int)
gridLayOut = []

row = 0
col = 0
side = corners[0].side[2]
addTiles(grid, row, col, corners[0], gridLayOut)
print("Upper left corner: ", corners[0].num, side)
corners[0].display()
corners[0].used = True
found = False
##
## Get left edges, matching side is 2
for n in range(1,numpixels-1):
	for e in edges:
		if e.used: continue
		found, rot, flip = e.hasSide(side)
		if found:
			row += 1
			e.used = True
			e.orientToSide(side, 0)
			addTiles(grid, row, col, e, gridLayOut)
			print("Next left edge: ", e.num)
			e.display()
			side = e.side[2]
			break
found = False
##
## Bottom row, corner
for c in corners:
	if c.used : continue
	found, rot, flip = c.hasSide(side)
	if found:
		row += 1
		c.used = True
		c.orientToSide(side, 0)
		addTiles(grid, row, col, c, gridLayOut)
		side = c.side[1]
		print("Lower left corner: ", c.num)
		c.display()
		break
	
found = False
##
## Get bottom edge
for n in range(1,numpixels-1):
	for e in edges:
		if e.used: continue
		found, rot, flip = e.hasSide(side)
		if found:
			col += 1
			e.used = True
			e.orientToSide(side, 3)
			addTiles(grid, row, col, e, gridLayOut)
			print("Next bottom edge: ", e.num)
			e.display()
			side = e.side[1]
			break

found = False
##
## Get lower right edge corner
for c in corners:
	if c.used : continue
	found, rot, flip = c.hasSide(side, True)
	if found:
		col += 1
		c.used = True
		c.orientToSide(side, 3)
		addTiles(grid, row, col, c, gridLayOut)
		side = c.side[0]
		c.display()
		print("Lower right corner: ", c.num)
		break
		
found = False
##
## Get right edge
for n in range(1,numpixels-1):
	for e in edges:
		if e.used: continue
		found, rot, flip = e.hasSide(side)
		if found:
			row -= 1
			e.used = True
			e.orientToSide(side, 2)
			addTiles(grid, row, col, e, gridLayOut)
			print("Next right edge: ", e.num)
			e.display()
			side = e.side[0]
			break

found = False
##
## Get upper right corder
for c in corners:
	if c.used : continue
	found, rot, flip = c.hasSide(side)
	if found:
		row -= 1
		c.used = True
		c.orientToSide(side, 2)
		addTiles(grid, row, col, c, gridLayOut)
		print("Upper right corner: ", c.num)
		c.display()
		side = c.side[3]
		break
		
found = False
print("*********************************", numpixels)
##
## Get right edge
for n in range(1,numpixels-1):
	for e in edges:
		if e.used: continue
		found, rot, flip = e.hasSide(side)
		if found:
			col -= 1
			e.used = True
			e.orientToSide(side, 1)
			addTiles(grid, row, col, e, gridLayOut)
			print("Next top edge: ", e.num)
			side = e.side[3]
			break

#createGridFromTiles(grid, tiles, puzzle, numpixels)
#addTiles(grid, 0, 0, corner[0])
#for x in range(1,numpixels-1):	# Do left edges

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

monster = np.zeros((3,20),dtype=int)
# 01234567890123456789
#0                  # 
#1#    ##    ##    ###
#2 #  #  #  #  #  #   
monster[0][18] = 1
for j in (0,5,6,11,12,17,18,19) : monster[1][j] = 1
for j in (1,4,7,10,13,16) : monster[2][j] = 1
monsterSize = sum(sum(monster))
#print("Monster size is ", monsterSize)

#print (monster)
#print (grid)
#print(sum(sum(grid)))

for i in range(4):
	n = countObjects(grid, monster)
	monster = np.rot90(monster)
	print ("n = ", n)

monster = np.rot90(monster)
monster = np.fliplr(monster)
for i in range(4):
	n = countObjects(grid, monster)
	monster = np.rot90(monster)
	print ("n = ", n)

print (gridLayOut)

print("Part 2: Number of non-serpant pixels is: ", numpixels)
