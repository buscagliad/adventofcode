import copy

class grid :
	def __init__(self, fname, part2 = False) :
		self.g = []
		for lines in open(fname, 'r') :
			self.columns = len(lines) - 1   # line feed
			self.g.append(list(lines[:self.columns]))
		self.rows = len(self.g)
		self.u = copy.deepcopy(self.g)
		self.part2 = part2
	
	def get(self, r, c) :
		if (r < 0) or (r >= self.rows) or (c < 0) or (c >= self.columns) : return '.'
		return self.g[r][c]
		
	def inline(self, r, rpm1, c, cpm1):
		r += rpm1
		c += cpm1
		#print("r: ", r, " dr: ", rpm1, "c: ", c, " dc: ", cpm1)
		while r >= 0 and r < self.rows and c >= 0 and c < self.columns :
			thischair = self.get(r, c)
			if thischair == 'L' : return 0
			if thischair == '#' : return 1
			r += rpm1
			c += cpm1
		return 0
			
	def count2(self, r, c) :
		cnt = 0
		for dr in [-1, 0, 1] :
			for dc in [-1, 0, 1] :
				if dr == 0 and dc == 0 : continue
				cnt += self.inline(r, dr, c, dc)
		#print ("@ (", r, c, ") = ", cnt);
		return cnt
					
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
		if self.part2 : neighbor_count = 5
		else : neighbor_count = 4
		for r in range(self.rows) :
			for c in range(self.columns) :
				u = self.g[r][c]
				if u == '.' : neighbors = 0
				else : 
					if self.part2:
						neighbors = self.count2(r, c)
					else :
						neighbors = self.count(r, c)
				if u == 'L' and neighbors == 0 : 
					u = '#'
					num_changes += 1
				elif u == '#' and neighbors  >= neighbor_count : 
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
n = 0

while x > 0 :
	n += 1
	x = g.update()
print("Part 1: Number of occupied seats: ", g.occupied(), " after ", n, " updates")

g = grid("data.txt", True)
x = 1
n = 0

while x > 0 :
	n += 1
	x = g.update()
print("Part 2: Number of occupied seats: ", g.occupied(), " after ", n, " updates")
