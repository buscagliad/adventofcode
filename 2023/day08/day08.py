from math import gcd

def LRins(line):
	ind =[]
	for a in line:
		if a == 'R': ind.append(1)
		if a == 'L': ind.append(0)
	return ind
	
def addMap(m, line):
	w = line.split()
	a = w[0]
	l = w[2][1:4]
	r = w[3][:3]
	#print(a, l, r)
	m[a]=[l,r]

firstLine = True
m = {}
for line in open("data.txt", "r"):
	if firstLine:
		ind = LRins(line)
		firstLine = False
		continue
	if len(line) > 2:
		addMap(m, line)

def play(m, a, i):
	return m[a][i]


n = play(m, 'AAA', ind[0])

j = 1
step = 1
while not n == 'ZZZ':
	n = play(m, n, ind[j])
	j += 1
	if j >= len(ind): j = 0
	step += 1

print("Part 1: number of steps to get from AAA to ZZZ", step)

def startNodes(m):
	an = []
	zn = []
	for n in m.keys():
		if n[2] == 'A':
			an.append(n)
		if n[2] == 'Z':
			zn.append(n)
	return an, zn

def solved(a, zn):
	if not a in zn: return False
	return True

an, zn = startNodes(m)

steps = 0
j = 0

runs=[]
for a in an:
	steps = 0
	j = 0
	while not solved(a, zn):
		steps += 1
		a = play(m, a, ind[j])
		# print(a)
		j += 1
		if j >= len(ind): j = 0
		#if (steps % 10000 == 0):
		#	print(steps)
	runs.append(steps)

lcm = 1
for i in runs:
	lcm = lcm * i // gcd(lcm, i)
print("Part 2: number of steps for all z's: ", lcm)
