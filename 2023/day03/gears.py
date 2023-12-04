
numbers=[]

def process(line, lineno):
	global numbers
	s = 0
	st = -1
	en = 0
	for i in range(len(line)):
		if line[i].isdigit():
			if st == -1: st = i
			en = i
			d = int(line[i])
			s = 10 * s + d
			# print (i, st, en, d, s)
		else:
			if s > 0:
				numbers.append([s, lineno, st, en, False, 0])
			s = 0
			st = -1
			end = 0

def check(line, lineno):
	global numbers

	for i in range(len(line)):
		if line[i].isdigit() or line[i] == '.' or line[i] == '\n': continue
		# print(line[i], i, lineno)
		idx = 1000*lineno+i
		for n in numbers:
			if n[1] == lineno or n[1] == lineno + 1 or n[1] == lineno - 1:
				if i >= n[2] - 1  and i <= n[3] + 1:
					n[4] = True
					if line[i] == "*":
						n[5] = idx
						
def compgear():
	global numbers
	gp = 0
	gidxCount = 0
	gpsum = 0
	
	for i in range(len(numbers)):
		n = numbers[i]
		if n[5] == 0: continue
		gp = n[0]
		gidx = n[5]
		gidxCount = 1
		for j in range(i+1, len(numbers)):
			n = numbers[j]
			if n[5] == gidx:
				gp *= n[0]
				gidxCount += 1
		if gidxCount == 2:
			#print(gp)
			gpsum += gp
	return gpsum
		

def sumnum():
	global numbers
	s = 0
	for n in numbers:
		if n[4]: s += n[0]
	return s

i = 0
for line in open("data.txt", "r"):
	process(line, i)
	i += 1

i = 0
for line in open("data.txt", "r"):
	check(line, i)
	i += 1

print ("Part 1: sum of parts is: ", sumnum())

print("Part 2: sum of gear ratios is: ", compgear())
