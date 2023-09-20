Floor = '.'
Seat = 'L'
Occupied = '#'

class grid :
	def __init__(self, fname) :
		self.g = []
		for lines in open(fname, 'r') :
			self.columns = len(lines) - 1   # line feed
			self.g.append(list(lines[:self.columns]))
		self.rows = len(self.g)
		self.u = self.g
	
	def get(self, r, c) :
		if (r < 0) or (r >= self.rows) or (c < 0) or (c >= self.columns) : return '.'
		return self.g[r][c]
		
	def count(self, r, c) :
		c = 0
		if self.get(r-1, c-1) == '#' : c += 1
		if self.get(r-1, c  ) == '#' : c += 1
		if self.get(r-1, c+1) == '#' : c += 1
		if self.get(  r, c-1) == '#' : c += 1
		if self.get(  r, c+1) == '#' : c += 1
		if self.get(r+1, c-1) == '#' : c += 1
		if self.get(r+1, c  ) == '#' : c += 1
		if self.get(r+1, c+1) == '#' : c += 1
		return c

	def update(self) :
		for r in range(self.rows) :
			for c in range(self.columns) :
				u = self.g[r][c]
				if u == 'L' and self.count(r, c) == 0 : u = '#'
				elif u == '#' and self.count(r, c) >= 4 : u = 'L'
				self.u[r][c] = u
		self.g = self.u
		
	def output(self) :
		for r in self.g :
			print(r)
		print()

g = grid("test.txt")
g.output()
g.update()
g.output()	
