
def isok(n, v):
	if n is None: return True
	if n == v: 
		return True
	return False

def isoklt(n, v):
	if n is None: return True
	if n < v: 
		return True
	return False
	
def isokgt (n, v):
	if n is None: return True
	if n > v: 
		return True
	return False
		
class Sue:
	def __init__(self, sue, children, cats, samoyeds, pomeranians, akitas, 
		vizslas, goldfish, trees, cars, perfumes):
		self.children = children
		self.cats = cats
		self.samoyeds = samoyeds
		self.pomeranians = pomeranians
		self.akitas = akitas
		self.vizslas = vizslas
		self.goldfish = goldfish
		self.trees = trees
		self.cars = cars
		self.perfumes = perfumes
		self.sue = sue
		self.ok = True
		self.valid()

	def valid(self):
		self.ok = self.ok and isok(self.children, 3) 	# children: 3
		self.ok = self.ok and isok(self.cats, 7)		# cats, 7
		self.ok = self.ok and isok(self.samoyeds, 2)	# samoyeds, 2
		self.ok = self.ok and isok(self.pomeranians, 3)# pomeranians, 3
		self.ok = self.ok and isok(self.akitas, 0)		# akitas, 0
		self.ok = self.ok and isok(self.vizslas, 0)	# vizslas, 0
		self.ok = self.ok and isok(self.goldfish, 5)	# goldfish, 5
		self.ok = self.ok and isok(self.trees, 3)		# trees, 3
		self.ok = self.ok and isok(self.cars, 2)		# cars, 2
		self.ok = self.ok and isok(self.perfumes, 1)	# perfumes, 1
	def out(self):
		print(self.sue, "children", self.children, "cats", self.cats,
				"samoyeds", self.samoyeds,
			"pomeranians", self.pomeranians,"akitas", self.akitas,"vizslas", self.vizslas,
			"goldfish", self.goldfish,"trees", self.trees,"cars", self.cars,"perfumes", self.perfumes)
	def part2(self):
		self.ok = True
		self.ok = self.ok and isok(self.children, 3) 	# children: 3
		self.ok = self.ok and isokgt(self.cats, 7)		# cats, 7
		self.ok = self.ok and isok(self.samoyeds, 2)	# samoyeds, 2
		self.ok = self.ok and isoklt(self.pomeranians, 3)# pomeranians, 3
		self.ok = self.ok and isok(self.akitas, 0)		# akitas, 0
		self.ok = self.ok and isok(self.vizslas, 0)	# vizslas, 0
		self.ok = self.ok and isoklt(self.goldfish, 5)	# goldfish, 5
		self.ok = self.ok and isokgt(self.trees, 3)		# trees, 3
		self.ok = self.ok and isok(self.cars, 2)		# cars, 2
		self.ok = self.ok and isok(self.perfumes, 1)	# perfumes, 1

def pline(line, n):
	ix = line.find(n)
	if ix < 0: return None
	i = ix + len(n) + 2
	v = 0
	for a in line[i:]:
		if a.isdigit():
			v = 10 * v + int(a)
		else:
			return v
	return None


def procline(line):
	sue = None
	children 	= None # children: 3
	cats		= None # cats, 7
	samoyeds	= None # samoyeds, 2
	pomeranians	= None # pomeranians, 3
	akitas		= None # akitas, 0
	vizslas		= None # vizslas, 0
	goldfish	= None # goldfish, 5
	trees		= None # trees, 3
	cars		= None # cars, 2
	perfumes	= None # perfumes, 1
	w = line.split(':')
	#print (w)
	sue = int(w[0][4:])
	children = pline(line, "children")
	cats = pline(line, "cats")
	samoyeds = pline(line, "samoyeds")
	pomeranians = pline(line, "pomeranians")
	akitas = pline(line, "akitas")
	vizslas = pline(line, "vizslas")
	goldfish = pline(line, "goldfish")
	trees = pline(line, "trees")
	cars = pline(line, "cars")
	perfumes = pline(line, "perfumes")
	return Sue(sue, children, cats, samoyeds, pomeranians, akitas, 
		vizslas, goldfish, trees, cars, perfumes)

s = []
for line in open("data.txt", "r"):
	s.append(procline(line))

for k in s:
	if k.ok:
		print("Part 1: Sue ", k.sue, " is the correct Aunt")

for k in s:
	k.part2()
	if k.ok:
		print("Part 2: Sue ", k.sue, " is the correct Aunt")
