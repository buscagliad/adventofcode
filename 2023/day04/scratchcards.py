def process(line, lineno):
	w = line.split()
	wn = []
	check = False
	rv = 0
	for i in range(2,len(w)):
		if check:
			mn = int(w[i])
			if mn in wn:
				if rv == 0: rv = 1
				else: rv *= 2
			
		elif w[i] == '|':
			check = True
			continue
		
		else:
			mn = int(w[i])
			wn.append(mn)
	return rv
	
def process2(line, lineno):
	w = line.split()
	#print(w)
	wn = []
	check = False
	rv = 0
	cardno = int(w[1][0:-1])
	for i in range(2,len(w)):
		if check:
			mn = int(w[i])
			if mn in wn:
				rv += 1
			
		elif w[i] == '|':
			check = True
			continue
		
		else:
			mn = int(w[i])
			wn.append(mn)

	return [cardno+1, cardno+rv, rv]

i = 0
s = 0
cc = []
mlines = 0
cc.append(0)
for line in open("data.txt", "r"):
	cc.append(1) # number of cards of each type
	s += process(line, i)
	i += 1
	mlines += 1
	
print ("Part 1: number of points in the cards: ", s)

s = 0
for line in open("data.txt", "r"):
	s, e, rv = process2(line, i)
	n = cc[s-1]
	for i in range(s,min(mlines,e)+1):
		cc[i] += n

print("Part 2: number of scratchards is: ", sum(cc))
