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
	def inc(self):
		self.count += 1
	def display(self):
		print(self.name)
		for i in range(len(self.ing)):
			print("  ", self.ing[i], ":", self.ingcount[i])
	
class Ingredient:
	def __init__(self, name, allergy):
		self.name = name
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
			#print (i)
			self.ing.append(i)
		for a in als:
			#for i in ing:
			#	self.ing.append(Ingredient(i, a))
			self.all.append(a)

	def display(self):
		print("Food item: ", self.id)
		print("   Ingredients: ", [(x) for x in self.ing])
		print("   Allergies: ", [(x) for x in self.all])
		print("")


foods = []
n = 0
for line in open("test.txt", "r"):
	n += 1
	#print(line)
	foods.append(Food(n, line))

print("\n\nFoods:\n")
for f in foods:
	f.display()

def find(s, n):
	for i in range(len(s)):
		if s[i].name == n : return i
	return -1

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
	#f.display()
	#print ("Food: ", f.id)
	for i in f.ing:
		#print("     Ingredient: ", i)
		n = find(ing, i)
		if (n < 0):
			newing = True
		for a in f.all:
			#print("        allergy: ", a)
			if newing :
				newing = False
				#print("          Adding new allergy: ", a, "   to  ", i)
				ing.append(Ingredient(i, a))
			else:
				ing[n].add(a)

print("\n\nIngredients:\n")

for i in ing:
	i.display()
	
print("\n\nAllergens:\n")
for a in alg:
	a.display()
