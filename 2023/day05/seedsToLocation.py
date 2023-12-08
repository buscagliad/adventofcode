
G_FNAME = "data.txt"

class cmap():
	def __init__(self, name):
		self.name = name
		self.ranges = []

	def addRange(self, start_to, start_from, length):
		self.ranges.append([start_from, start_to, length-1])
		self.ranges.sort(key=lambda tup: tup[1])
	def getTo(self, num):
		for from_min, to_min, length in self.ranges:
			if from_min <= num and num <= from_min + length:
				return to_min + (num - from_min)
		return num
	def backTo(self, num):
		for from_min, to_min, length in self.ranges:
			if to_min <= num and num <= to_min + length:
				return from_min + (num - to_min)
		return num
	def getRanges(self):
		min_r = self.ranges[0][1]
		min_i = 0
		for i in range(len(self.ranges)):
			if self.ranges[i][1] <= min_r:
					min_r = self.ranges[i][1]
					min_i = i
		print(self.name, "  From Range: ", self.ranges[min_i][0], 
			self.ranges[min_i][0] + self.ranges[min_i][2],
			self.ranges[min_i][1], 
			self.ranges[min_i][1] + self.ranges[min_i][2])
		return self.ranges[min_i]
	def out(self):
		print(self.name)
		for from_min, to_min, length in self.ranges:
			print("From ranges: ", from_min, from_min + length, "   To: ", 
				to_min, to_min + length)

def create_cmap(key):
	global G_FNAME
	process = False
	c = cmap(key)
	for line in open(G_FNAME, "r"):
		if process:
			if len(line) < 3: break
			w = line.split()
			c.addRange(int(w[0]), int(w[1]), int(w[2]))
		elif line[:len(key)] == key:
			process = True;
	return c
	
def get_seeds():
	global G_FNAME
	process = False
	seeds = []
	for line in open(G_FNAME, "r"):
		w = line.split()
		if w[0] == "seeds:":
			for a in w[1:] :
				seeds.append(int(a))
			break
	return seeds
		
seed_to_soil = create_cmap ("seed-to-soil")
soil_to_fertilize = create_cmap ("soil-to-fertilize")
fertilizer_to_water = create_cmap("fertilizer-to-water")
water_to_light = create_cmap("water-to-light")
light_to_temperature = create_cmap("light-to-temperature")
temperature_to_humidity = create_cmap("temperature-to-humidity")
humidity_to_location = create_cmap("humidity-to-location")


# seed_to_soil.out()
# soil_to_fertilize.out()
# fertilizer_to_water.out()
# water_to_light.out()
# light_to_temperature.out()
# temperature_to_humidity.out()
# humidity_to_location.out()

seeds = get_seeds()

def in_seed(t):
	global seeds
	for i in range(0, len(seeds), 2):
		g = t - seeds[i]
		if g >= 0 and g < seeds[i+1]: return True
	return False

#print(seeds)
def getLoc(s):
	global seed_to_soil
	global soil_to_fertilize
	global fertilizer_to_water
	global water_to_light
	global light_to_temperature
	global temperature_to_humidity
	global humidity_to_location
	a = seed_to_soil.getTo(s)
	b = soil_to_fertilize.getTo(a)
	c = fertilizer_to_water.getTo(b)
	d = water_to_light.getTo(c)
	e = light_to_temperature.getTo(d)
	f = temperature_to_humidity.getTo(e)
	g = humidity_to_location.getTo(f)
	return g
	
def getSeed(l):
	global seed_to_soil
	global soil_to_fertilize
	global fertilizer_to_water
	global water_to_light
	global light_to_temperature
	global temperature_to_humidity
	global humidity_to_location
	a = humidity_to_location.backTo(l)
	b = temperature_to_humidity.backTo(a)
	c = light_to_temperature.backTo(b)
	d = water_to_light.backTo(c)
	e = fertilizer_to_water.backTo(d)
	f = soil_to_fertilize.backTo(e)
	g = seed_to_soil.backTo(f)
	return g
	
	
#print(seeds)
def outIntervals():
	global seed_to_soil
	global soil_to_fertilize
	global fertilizer_to_water
	global water_to_light
	global light_to_temperature
	global temperature_to_humidity
	global humidity_to_location
	for d in range(7):
		print("Depth: ", d)
		lasta = -1
		firsts = -1
		for s in range(100):
			print(s, ' -> ', end="")
			a = seed_to_soil.getTo(s)
			print(a, end="")
			if (d > 0) : 
				a = soil_to_fertilize.getTo(a)
				print(' -> ', a, end="")
			if (d > 1) : 
				a = fertilizer_to_water.getTo(a)
				print(' -> ', a, end="")
			if (d > 2) : 
				a = water_to_light.getTo(a)
				print(' -> ', a, end="")
			if (d > 3) : 
				a = light_to_temperature.getTo(a)
				print(' -> ', a, end="")
			if (d > 4) : 
				a = temperature_to_humidity.getTo(a)
				print(' -> ', a, end="")
			if (d > 5) : 
				a = humidity_to_location.getTo(a)
				print(' -> ', a, end="")
			print()
			if firsts == -1:
				firsts = s
				delta = a - s
			elif not a == lasta + 1:
				print("[", firsts, ", ", s - 1, "]  -> ", delta)
				firsts = s
				delta = a - s
			lasta = a
		print("[", firsts, ", ", 99, " -> ", delta)

low_seed = 1000000000000000
for s in seeds:
	g = getLoc(s)
	#print("Seed ", a, " to location ", g)
	if g < low_seed: low_seed = g
# outIntervals()

print("Part 1: lowest seed location is: ", low_seed)

##
## part 2 - sees are in ranges
##
low_seed = 1000000000000000

for l in range(2**31):
	s = getSeed(l)
	if in_seed(s):
		print("Part 2: ", l)
		break

#
#		if g < low_seed: low_seed = g
#print("Part 2: lowest sequence seed is: ", low_seed)

