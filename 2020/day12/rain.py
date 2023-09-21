from enum import Enum

class Dir(Enum):
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3

class Ship:
	def __init__(self, fname):
		self.heading = 1
		self.east = 0
		self.north = 0
		for lines in open(fname, 'r') :
			ins = lines[0]
			dist = int(lines[1:])
			if ins == 'N' : self.north += dist
			elif ins == 'S' : self.north -= dist
			elif ins == 'E' : self.east += dist
			elif ins == 'W' : self.east -= dist
			elif ins == 'L' : 
				self.heading -= (dist/90) + 24
				self.heading %= 4
				
			elif ins == 'R' :
				self.heading += (dist/90) + 24
				self.heading %= 4
				
			elif ins == 'F' :
				if self.heading == 0 : self.north += dist
				elif self.heading == 1 : self.east += dist
				elif self.heading == 2 : self.north -= dist
				elif self.heading == 3 : self.east -= dist

	def manhattan(self) :
		return abs(self.north) + abs(self.east)

class WPShip:
	def __init__(self, fname):
		self.east = 0
		self.north = 0
		self.wpEast = 10
		self.wpNorth = 1
		for lines in open(fname, 'r') :
			ins = lines[0]
			dist = int(lines[1:])
			if ins == 'N' : self.wpNorth += dist
			elif ins == 'S' : self.wpNorth -= dist
			elif ins == 'E' : self.wpEast += dist
			elif ins == 'W' : self.wpEast -= dist
			elif ins == 'L' : 
				hdg = int(dist/90) % 4
				for flip in range(hdg) :
					save = self.wpEast
					self.wpEast = -self.wpNorth
					self.wpNorth = save

			elif ins == 'R' :
				hdg = int(dist/90) % 4
				for flip in range(hdg) :
					save = self.wpEast
					self.wpEast = self.wpNorth
					self.wpNorth = -save

			elif ins == 'F' :
				self.north += dist * self.wpNorth
				self.east += dist * self.wpEast

	def manhattan(self) :
		return abs(self.north) + abs(self.east)

ship = Ship("data.txt")
print("Part1 - Ship's Manhattan distance is ", ship.manhattan())

ship = WPShip("data.txt")
print("Part2 - Ship's Manhattan distance is ", ship.manhattan())

