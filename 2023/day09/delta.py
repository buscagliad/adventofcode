


def nextnum(line, rev = False):
	#print("INPUT: ", line)
	w = line.split()
	e = []
	l = []
	vv = []
	if rev:
		for i in reversed(w):
			e.append(int(i))
	else:
		for i in w:
			e.append(int(i))
	s = e[-1]	## last number in sequency
	d = e
	#print(d, "[", len(d), "]", d[0])
	#vv.append(e)
	while not (d.count(d[0]) == len(d)):
		nd = []
		for i in range(len(d)-1):
			nd.append(d[i+1]-d[i])
		vv.append(nd)
		d = nd
		#print(d)
	j = None
	for v in reversed(vv):
		if j == None:
			j = v[-1]
			#print("first j set to: ", j)
		else:
			j += v[-1]
			#print("next j is: ", v[-1], " j is now: ", j)
	
	#print(s+j)
	return s+j

s = 0	
for line in open("data.txt"):
	s += nextnum(line)

print("Part 1: sum of next numbers is: ", s)


s = 0	
for line in open("data.txt"):
	s += nextnum(line, True)


print("Part 2: sum of prev numbers is: ", s)
