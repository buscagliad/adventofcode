
tilenumber = 0
upperLeftTile = None
centerTile = None
tileList = []
circleList = []

def getnum(t):
	if t == None: return -1
	return t.tile

class Tile:
	def __init__(self):
		global tilenumber
		global tileList
		tilenumber += 1
		self.tile = tilenumber
		self.east = None
		self.northeast = None
		self.northwest = None
		self.west = None
		self.southwest = None
		self.southeast = None
		self.black = False
		tileList.append(self)
		self.part2flip = False
		
	def display(self):
		print(getnum(self.northwest), "      ", getnum(self.northeast))
		print("    \    / ");
		print(getnum(self.west), "--", self.tile, "--", getnum(self.east))
		print("    /    \ ");
		print(getnum(self.southwest), "      ", getnum(self.southeast))
		
	def flip(self, debug=False):
		if self.black:
			self.black = False
			if debug: print(self.tile, " flipping to White")
		else:
			self.black = True
			if debug: print(self.tile, " flipping to Black")

	def neighbors(self):
		c = 0
		if not self.east is None and self.east.black: c += 1
		if not self.west is None and self.west.black: c += 1
		if not self.southeast is None and self.southeast.black: c += 1
		if not self.northeast is None and self.northeast.black: c += 1
		if not self.southwest is None and self.southwest.black: c += 1
		if not self.northwest is None and self.northwest.black: c += 1
		return c

def findTile(tn):
	global tileList
	for t in tileList:
		if t.tile == n:
			return t

def checkNeighbors():
	global tileList
	for t in tileList:
		c = t.neighbors()
		if t.black:
			if c == 0 or c > 2:
				t.part2flip = True
		else:
			if c == 2:
				t.part2flip = True
				
def part2day():
	global tileList
	checkNeighbors()
	for t in tileList:
		if t.part2flip : t.flip()
		t.part2flip = False
				
				
def count():
	global tileList
	c = 0
	for t in tileList:
		if t.black:
			c += 1
	return c
	
def createGrid(n):
	global upperLeftTile 
	global centerTile
	row = 1
	##
	## create first row:
	upperLeftTile = Tile()
	leftMostTile = upperLeftTile
	tt = upperLeftTile
	for i in range(n-1):
		tt.east = Tile()
		tt.east.west = tt
		tt = tt.east

	while row <= n:
		tt = leftMostTile
		#print(tt.tile)
		row += 1
		pt = None
		for i in range(n):
			nt = Tile()
			tt.southeast = nt
			if not tt.east is None: tt.east.southwest = nt
			nt.northwest = tt
			nt.northeast = tt.east
			if pt is None:
				leftMostTile = nt
			else:
				nt.west = pt
				pt.east = nt
			if row == n/2 and i == n/2:
				centerTile = nt
			pt = nt
			tt = tt.east

def process(line, debug = False):
	global centerTile
	ct = centerTile
	carry = ' '
	for a in line:
		if a == '\n': break
		if carry == 's':
			carry = ' '
			if a == 'e':
				if debug: print("Taversing southeast from", ct.tile, "to", ct.southeast.tile)
				ct = ct.southeast
			elif a == 'w':
				if debug: print("Taversing southwest from", ct.tile, "to", ct.southwest.tile)
				ct = ct.southwest
			else:
				print("ERROR at ", a, " in ", line)
				exit(1)
		elif carry == 'n':
			carry = ' '
			if a == 'e':
				if debug: print("Taversing northeast from", ct.tile, "to", ct.northeast.tile)
				ct = ct.northeast
			elif a == 'w':
				if debug: print("Taversing northwest from", ct.tile, "to", ct.northwest.tile)
				ct = ct.northwest
			else:
				print("ERROR at ", a, " in ", line)
				exit(1)
		else:
			if a == 'w': 
				if debug: print("Taversing west from", ct.tile, "to", ct.west.tile)
				ct = ct.west
			elif a == 'e': 
				if debug: print("Taversing east from", ct.tile, "to", ct.east.tile)
				ct = ct.east
			else:
				carry = a
	ct.flip()
			
def renumber(maxnum):
	global centerTile
	global circleList
	tilenumber = 1
	sequence = 0
	centerTile.tilenumber = tilenumber
	tile = centerTile
	done = False
	while tilenumber < maxnum:
		sequence += 1
		tile = centerTile.east
		tilenumber += 1
		tile.tilenumber = tilenumber
		for i in range(6):
			# (nw, w, sw, se, e, ne)
			for j in range(sequence):
				tile = centerTile.northwest
				tilenumber += 1
				tile.tilenumber = tilenumber
			for j in range(sequence):
				tile = centerTile.west
				tilenumber += 1
				tile.tilenumber = tilenumber
			for j in range(sequence):
				tile = centerTile.southwest
				tilenumber += 1
				tile.tilenumber = tilenumber
			for j in range(sequence):
				tile = centerTile.southeast
				tilenumber += 1
				tile.tilenumber = tilenumber
			for j in range(sequence):
				tile = centerTile.east
				tilenumber += 1
				tile.tilenumber = tilenumber
			for j in range(sequence):
				tile = centerTile.northeast
				tilenumber += 1
				tile.tilenumber = tilenumber
				
	
	
createGrid(200)
renumber(100)
centerTile.display()
exit(1)

for line in open("data.txt", "r"):
	process(line)
print("Part 1: Number of black tiles: ", count())

for day in range(1, 101):
	part2day()

print("Part 2: After Day ", day, ", there are ", count(), " black tiles")
