import numpy as np


class city():
	def __init__(self, name):
		self.name = name
		self.dist = {}
	def add(self, to, dist):
		self.dist[to] = dist
	def out(self):
		for city in self.dist:
			print(self.name, " -> ", city, " ", self.dist[city])

cities = []
dindex = {}
i = 0

for line in open("data.txt", "r"):
	# Dublin to Belfast = 141
	x = line.split()
	t1 = x[0]
	t2 = x[2]
	if not t1 in cities:
		cities.append(t1)
		dindex[t1] = i
		i += 1
	if not t2 in cities:
		cities.append(t2)
		dindex[t2] = i
		i += 1
	d = int(x[4])

paths = np.zeros((len(cities),len(cities)))
for line in open("data.txt", "r"):
	# Dublin to Belfast = 141
	x = line.split()
	t1 = x[0]
	t2 = x[2]
	if not t1 in cities:
		cities.append(t1)
	if not t2 in cities:
		cities.append(t2)
	d = int(x[4])
	i = cities.index(t1)
	j = cities.index(t2)
	paths[i][j] = d
	paths[j][i] = d


		
arr=list(range(len(cities)))
import itertools
permlist = list(itertools.permutations(arr))

maxdist = 0
mindist = 1000000000
perm = None
for p in permlist:
	dist = 0
	for i in range(len(cities) - 1):
		dist += paths[p[i]][p[i+1]]
	if dist < mindist:
		mindist = dist
	if dist > maxdist:
		maxdist = dist

print ("Part 1:  Minimum distance is ", mindist)
print ("Part 2:  Maximum distance is ", maxdist)
