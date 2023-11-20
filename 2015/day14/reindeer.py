
class Deer():
	def __init__(self, name, speed, gtime, rest):
		self.name = name
		self.speed = speed
		self.cango = gtime
		self.gotime = 0
		self.rest = rest
		self.resttime = 0
		self.clock = 0
		self.distance = 0
		self.resting = False
		self.points = 0
	def out(self):
		print(self.name, " traveled ", self.distance, " after ", self.clock, " state is ", end="")
		if (self.resting):
			print("RESTING")
		else:
			print("TRAVELLING")
		print(self.name, " speed is ", self.speed, " gotime ", self.gotime, " rest time ", self.resttime)
	def tick(self):
		self.clock += 1
		if self.resting:
			self.resttime += 1
			if self.resttime >= self.rest:
				self.resting = False
				self.gotime = 0
				self.resttime = 0
		else:
			self.gotime += 1
			self.distance += self.speed
			if self.gotime >= self.cango:
				self.resting = True
				self.gotime = 0
				self.restime = 0
	def give(self):
		self.points += 1

#Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
#Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
def makedeer(line):
	w = line.split()
	#print(w)
	return Deer(w[0], int(w[3]), int(w[6]), int(w[13]))

deers=[]
for line in open("data.txt", "r"):
	deers.append(makedeer(line))

for t in range(2503):
	m = 0
	for d in deers:
		d.tick()
		if d.distance > m : m = d.distance
	for d in deers:
		if d.distance >= m: d.give()
	
	

winner=deers[0]
for d in deers:
	if d.distance > winner.distance:
		winner = d

print("Part 1: Winner is ", winner.name, " travelling ", winner.distance)

winner=deers[0]
for d in deers:
	if d.points > winner.points:
		winner = d

print("Part 2: Winner is ", winner.name, " with ", winner.points, " points")
