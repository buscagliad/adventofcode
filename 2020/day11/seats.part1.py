import copy

class grid :
	def __init__(self, fname) :
		self.g = []
		for lines in open(fname, 'r') :
			self.columns = len(lines) - 1   # line feed
			self.g.append(list(lines[:self.columns]))
		self.rows = len(self.g)
		self.u = copy.deepcopy(self.g)
	
	def get(self, r, c) :
		if (r < 0) or (r >= self.rows) or (c < 0) or (c >= self.columns) : return '.'
		return self.g[r][c]
		
	def count(self, r, c) :
		cnt = 0
		if self.get(r-1, c-1) == '#' : cnt += 1
		if self.get(r-1, c  ) == '#' : cnt += 1
		if self.get(r-1, c+1) == '#' : cnt += 1
		if self.get(  r, c-1) == '#' : cnt += 1
		if self.get(  r, c+1) == '#' : cnt += 1
		if self.get(r+1, c-1) == '#' : cnt += 1
		if self.get(r+1, c  ) == '#' : cnt += 1
		if self.get(r+1, c+1) == '#' : cnt += 1
		return cnt

	def occupied(self) :
		cnt = 0
		for r in range(self.rows) :
			for c in range(self.columns) :
				if self.get(r, c) == '#' : cnt += 1
		return cnt

	def update(self) :
		num_changes = 0
		for r in range(self.rows) :
			for c in range(self.columns) :
				u = self.g[r][c]
				if u == '.' : neighbors = 0
				else : neighbors = self.count(r, c)
				if u == 'L' and neighbors == 0 : 
					u = '#'
					num_changes += 1
				elif u == '#' and neighbors  >= 4 : 
					u = 'L'
					num_changes += 1
				#print ("r: ", r, " c: ", c, " self.g[r][c]: ", self.g[r][c], " u: ", u, " neighbors: ", neighbors)
				self.u[r][c] = u
		self.g = copy.deepcopy(self.u)
		return num_changes
		
	def output(self) :
		for r in self.g :
			print(r)
		print()
		print("Number of occupied seats: ", self.occupied())

g = grid("data.txt")
#g.output()
x = 1

while x > 0 :
	x = g.update()
	#g.output()
	#print ("Number of changes: ", x)
print("Part 1: Number of occupied seats: ", g.occupied())
