
chems={}
basechem=""
steps=[]

def chemicals(chem, f, to):
	global chems
	r = 0
	d = len(f)
	while True:
		i = chem.find(f, r)
		if (i < 0) : break
		newch = ''.join([chem[:i], to, chem[i+d:]])
		chems.add(newch)
		r = i + 1

def rem(chem, f, to):
	r = 0
	d = len(f)
	retset={}
	while True:
		i = chem.find(f, r)
		if (i < 0) : break
		newch = ''.join([chem[:i], to, chem[i+d:]])
		if len(retset) == 0: retset={newch}
		else: retset.add(newch)
		r = i + 1
	#print("retset is ", retset)
	return retset

fromto = True

for line in open("data.txt", "r"):
	line = line.strip()
	if fromto:
		i = line.find(" => ")
		if (i < 0): 
			fromto = False
			continue
		#print(line, i)

		f = line[:i]
		to = line[i+4:]
		steps.append([f,to])
	else: 
		basechem = line
		chems={basechem}
		#print("Base chem:", basechem)

def calibrate(molecule):
	global steps
	n = 0
	for f,t in steps:
		n += 1
		chemicals(molecule, f, t)

calibrate(basechem)

print ("Part1: number of chemicals that can be created is: ", len(chems) - 1)


print(steps)
chems.clear()
chems={basechem}
numsteps = 0
done = False
while not done:
	numsteps += 1
	newset = {}
	cc = 0
	for c in chems:
		for t,f in steps:
			cc += c.count(f)
	print("Number of chems: ", len(chems), " number of t.f steps: ", len(steps), " new number of chems expected:", cc)
	for c in chems:
		for t,f in steps:
			if f in c:
				s = rem(c, f, t)
				#print("REM: ", s)
				if len(newset) == 0:
					newset = s
				else:
					newset = newset.union(s)
		#print("...Step: ", numsteps, " adding: ", len(s), " total: ", len(newset), flush=True)
	#print("NEWSET::", newset)
	chems.clear()
	chems=newset
	#print("CHEMS:", chems)
	print("Step: ", numsteps, " chems: ", len(chems), flush=True)
	if "e" in chems: done = True
	if (len(chems) == 0) : done = True

print ("Part2: creating \"e\" took", numsteps, "steps")
#chems.clear{}
#while basechem not in chems:
	
