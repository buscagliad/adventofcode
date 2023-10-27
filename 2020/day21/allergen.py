class Allergen:
	def __init__(self, name):
		self.name = name
		self.count = 1
		self.ing = []
		self.ingcount = []
	def add(self, ingredient):
		for i in range(len(self.ing)):
			if self.ing[i] == ingredient: 
				self.ingcount[i] += 1
				return
		self.ing.append(ingredient)
		self.ingcount.append(1)
	def ingnum(self, ing):
		for n in range(len(self.ing)):
			if self.ing[n] == ing:
				return self.ingcount[n]
		return 0
	def inc(self):
		self.count += 1
	def display(self):
		print(self.name)
		for i in range(len(self.ing)):
			print("  ", self.ing[i], ":", self.ingcount[i])
	
class Ingredient:
	def __init__(self, name, allergy):
		self.name = name
		self.set = False
		self.isthisallergen = None
		self.count = 1
		self.appears = 1
		self.allergens = []
		self.allergens.append(Allergen(allergy))
	def add(self, alg):
		self.appears += 1
		for a in self.allergens:
			if a.name == alg: 
				a.inc()
				return
		newa = Allergen(alg)
		self.allergens.append(newa)
	def inc(self):
		self.count += 1
	def display(self):
		print(self.name)
		for a in self.allergens:
			print("  ", a.name, ":", a.count)
	def sort(self):
		self.allergens.sort(key=lambda x: x.count, reverse = True)
	def numalg(self):	# returns number of times this ingredient was associated with
		num = 0
		for a in self.allergens:
			num += a.count
		return num
			

def lineparse(line):
	return [x.strip() for x in line.split(',')]
	
class Food:
	def __init__(self, n, line):
		self.id = n
		self.ing = []
		self.all = []
		ing = []
		s = line.find('(')
		e = line.find(')')
		als = lineparse(line[s+9:e])
		#print (als)
		for i in line[:s-1].split():
			self.ing.append(i)
		for a in als:
			self.all.append(a)

	def ingcount(self, ingr):
		if ingr in self.ing: return 1
		return 0

	def display(self):
		print("Food item: ", self.id)
		print("   Ingredients: ", [(x) for x in self.ing])
		print("   Allergies: ", [(x) for x in self.all])
		print("")

#
# read in data file into foods list
#
foods = []
n = 0
for line in open("data.txt", "r"):
	n += 1
	foods.append(Food(n, line))

def find(s, n):
	for i in range(len(s)):
		if s[i].name == n : return i
	return -1

#
# create both an ingredient list (mapping to allergens)
#         and an allergen list (mapping to ingredients)
#
ing = []
alg = []
newing = False

#
# create Allergen list
#
for f in foods:
	for na in f.all:
		create = True
		for a in alg:
			if na == a.name:
				create = False
		if create: alg.append(Allergen(na))
#
# add Ingredients to Allergen list
#
for a in alg:
	for f in foods:
		# find the alg[] element for this 
		for na in f.all:
			if a.name == na:
				for i in f.ing:
					a.add(i)
		


for f in foods:
	for i in f.ing:
		n = find(ing, i)
		if (n < 0):
			newing = True
		for a in f.all:
			if newing :
				newing = False
				ing.append(Ingredient(i, a))
			else:
				ing[n].add(a)

def setingalg(ing, ingredient, allergen):
	for ingr in ing:
		if ingr.name == ingredient:
			ingr.set = True
			ingr.isthisallergen = allergen
			for alg in ingr.allergens:
				if alg.name != allergen:
					alg.count = 0
		else:
			for alg in ingr.allergens:
				if alg.name == allergen:
					alg.count = 0


def findmosting(ing, alg):
	i = []
	c = 0
	for ingr in ing:
		if ingr.set : continue
		for allergen in ingr.allergens:
			if allergen.name == alg:
				ni = ingr.name
				nc = allergen.count
				if nc > c:
					i = [ni]
					c = nc
				elif nc == c:
					i.append(ni)
	return i, c
		

for n in range(len(alg)):
	ingredient = None
	allergen = -1
	maxall = 0
	for a in alg:
		i, c = findmosting(ing, a.name)
		if c > maxall and len(i) == 1:
			maxall = c
			ingredient = i[0]
			allergen = a.name
	setingalg(ing, ingredient, allergen)

count = 0
for i in ing:
	if i.set: continue
	for f in foods:
		count += f.ingcount(i.name)

		
print("Part 1: Number of ingredients that have no allergens: ", count)

#
# Need to map ingredients to allergens
#
p2list = []
for i in ing:
	if i.set:
		p2list.append((i.isthisallergen, i.name))
		p2list.sort(key=lambda x: x[0])

k = 0
print ("Part 2: List of ordered ingredients: ", end="")
for i in p2list:
	print(i[1], end="")
	k += 1
	if k < len(p2list): print(",", end="")
print("")

	
