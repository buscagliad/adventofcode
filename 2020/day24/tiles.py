
tilenumber = 0
upperLeftTile = None
centerTile = None
tilelist = []

def getnum(t):
	if t == None: return -1
	return t.tile

class Tile:
	def __init__(self):
		global tilenumber
		global tilelist
		tilenumber += 1
		self.tile = tilenumber
		self.east = None
		self.northeast = None
		self.northwest = None
		self.west = None
		self.southwest = None
		self.southeast = None
		self.black = False
		tilelist.append(self)
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
		


def findTile(tn):
	global tilelist
	for t in tilelist:
		if t.tile == n:
			return t

def count():
	global tilelist
	c = 0
	for t in tilelist:
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
			

createGrid(100)
centerTile.display()

for line in open("data.txt", "r"):
	process(line)
print("Number of black tiles: ", count())
