
floor = 0
position = 0
neg1position = 0


class House:
	def __init__(self, x, y):
		self.hash = x * 10000 + y
		self.presents = 1

class Path:
	def __init__(self, gdict=False):
		global global_dict
		h = House(0, 0)
		self.hdict = {}
		self.hdict[h.hash] = h

	def add(self, x, y):
		h = House(x, y)
		if h.hash in self.hdict:
			self.hdict[h.hash].presents += 1
		else:
			self.hdict[h.hash] = h
	def count(self):
		return len(self.hdict)

spath = Path()
s1path = Path(True)
s2path = Path(True)
n = 0
for line in open("data.txt"):
	x = 0
	y = 0
	x1 = 0
	x2 = 0
	y1 = 0
	y2 = 0
	for p in line:
		dx = 0
		dy = 0
		if p == '\n':
			continue
		if p == '^': 
			dy = 1
		if p == 'v': 
			dy = -1
		if p == '>': 
			dx = 1
		if p == '<': 
			dx = -1
		x += dx
		y += dy
		spath.add(x,y)
		n += 1
		if n % 2 == 0:
			x1 += dx
			y1 += dy
			s1path.add(x1, y1)
		else:
			x2 += dx
			y2 += dy
			s1path.add(x2, y2)



print("Part 1::  number of houses visited at least once is ", spath.count())
print("Part 2::  number of houses getting robo presents is ", s1path.count())
