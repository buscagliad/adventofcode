import copy

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

def calibrate(molecule):
	global steps
	n = 0
	for f,t in steps:
		n += 1
		chemicals(molecule, f, t)

def grabRn(chem):
	print(chem)
	print()
	RnL = []
	ArL = []
	nRn = 0
	nAr = 0
	Rni = []
	Ari = []
	for i in range(len(chem)):
		if chem[i:i+2] == "Ar" : 
			ArL.append(i)
			nAr += 1
			nRn -= 1
			Ari.append(nAr)
		if chem[i:i+2] == "Rn" : 
			RnL.append(i)
			nRn += 1
			nAr -= 1
			Rni.append(nRn)
	print("Searching for Ar and Rn")
	print(len(RnL), " -> ", RnL)
	print(len(Ari), " Ari depth: ", Ari)
	print(len(ArL), " -> ", ArL)
	print(len(Rni), " Rni depth: ", Rni)
	maxRi = max(Rni)
	maxI = Rni.index(maxRi)
	maxR = RnL[maxI]
	maxA = 0
	print("Max Rn is: ", maxRi, maxI, maxR)
	for l in ArL:
		if l > maxR:
			maxA = l
			break
	print("Rn, An", maxR, maxA)
	if chem[maxR-1].islower(): maxR -= 2
	else: maxR -= 1
	maxA += 2
	print(maxR, maxA, chem[maxR:maxA])
	#return maxR, maxA, chem[maxR:maxA]
	return chem[maxR:maxA], chem[:maxR], chem[maxA:]
	
def getRnAr(chem):
	print(chem)
	print()
	RnL = []
	ArL = []
	ARlist = []
	for i in range(len(chem)):
		if chem[i:i+2] == "Ar" : 
			ArL.append(i)
		if chem[i:i+2] == "Rn" : 
			RnL.append(i)
	ai = 0
	ri = 0
	igRn = False

	done = False
	#
	# for ARList for RnL and ArL
	# ai is index into ArL and ri for RnL
	#
	rd = 0   # index offset
	i = 0
	if max(RnL) <= min(ArL) : done = True
	print(RnL)
	print(ArL)
	while not done:
		start = i
		while RnL[i+1] - ArL[i] < 3 : i += 1
		ARlist.append([RnL[start], ArL[i]])
		print(start, i, RnL[start], ArL[i])
		i += 1
		if i + 1 >= len(RnL) : done = True
	ARlist.append([RnL[0], ArL[-1]])
	retARlist = []
	print("RnL: ", RnL)
	print("ArL: ", ArL)
	for r, a in ARlist:
		if chem[r-1].islower(): r -= 2
		else: r -= 1
		a += 2
		retARlist.append([r, a])
	print(retARlist)
	return retARlist
	#return maxR, maxA, chem[maxR:maxA]
	#return chem[maxR:maxA], chem[:maxR], chem[maxA:]	
	
def rem(chem, f, to):
	r = 0
	n = 0
	i = 0
	d = len(f)
	newch = copy.deepcopy(chem)
	while i < len(chem) - 1:
		i = newch.find(f)
		if (i < 0) : break
		#print("Found ", f, " at ", i, " replaced with ", to)
		n += 1
		#print("old chem: ", newch)
		newch = ''.join([newch[:i], to, newch[i+d:]])
		#print("new chem: ", newch)
	#print("retset is ", retset)
	return newch, n

def getatoms(s):
	atoms=[]
	natoms=[]
	for t, f in s:
		if "Rn" in f:
			atoms.append([t,f])
		else:
			natoms.append([t,f])
	print(atoms)
	return atoms, natoms


def reduct(s):
	global steps
	num = 0
	done = False
	while not done:
		done = True
		for t, f in steps:
			s, k = rem(s, f, t)
			num += k
			if k > 0: done = False
	return s, num

########### MAIN ###############3

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


calibrate(basechem)

print ("Part1: number of chemicals that can be created is: ", len(chems) - 1)

for i in range(5):
	arList = getRnAr(basechem)
	print(arList)
	arList.reverse()
	for r, a in arList:
		s, n = reduct(basechem[r:a])
		print(r, a, basechem[r:a], s)
		basechem = ''.join([basechem[:r], s, basechem[a:]])
exit(1)


# done = False
# while not done:
	# numrem = 0
	# r, a, nchem = getIndeces(basechem)
	# reduct(nchem)
	# basechem, n = rem(basechem, t, f)
	# numrem += n
	# numsteps += n
	# if n == 0: done = True


print(steps)
chems.clear()
chems={basechem}
numsteps = 0
done = False

atoms, natoms = getatoms(steps)
print(basechem)

done = False
while not done:
	numrem = 0
	for f,t in atoms:
		basechem, n = rem(basechem, t, f)
		numrem += n
		numsteps += n
	if numrem == 0: done = True

print("163:: Removed ", numsteps)
print(basechem)

done = False
print (basechem)

rn, l, r = grabRn(basechem)
n = 1
nAr = 1
while len(rn) and n > 0:
	s, n = reduct(rn)
	print("grabRn: ", rn)
	print("Reduced to ", s, n)
	basechem = ''.join([l, s, r])
	#print("NAMES: ", "|", l, "|", s, "|", r, "|", sep="")
	print (basechem)
	numsteps += n
	if n == 0: 
		break
		nAr += 1
		n = 1 # keep look going
		print("Increased nAr to: ", nAr)
	rn, l, r = grabRn(basechem)
	
print("190: Removed ", numsteps)
print(basechem)

#exit(1)
# done = False
# while not basechem == "e" and not done:
	# done = True
	# for t,f in atoms:
		# basechem, k = rem(basechem, f, t)
		# numsteps += k
		# if k > 0: done = False
		# print(f, "  appears: ", k, " times.", " total: ", numsteps, flush=True)
		# if "Bi" in basechem:
			# print("Bi found 2", t, f, numsteps)
			# exit(1)
#
# grab xxRn...Ar molecules as see what they have inside them
#

print (basechem)

rn, l, r = grabRn(basechem)
n = 1
nAr = 1
while len(rn) and n > 0:
	s, n = reduct(rn)
	print("grabRn: ", rn)
	print("Reduced to ", s, n)
	basechem = ''.join([l, s, r])
	#print("NAMES: ", "|", l, "|", s, "|", r, "|", sep="")
	print (basechem)
	numsteps += n
	rn, l, r = grabRn(basechem)
	
RnL = [i for i, x in enumerate(basechem) if x[i:i+2] == "Rn"]
ArL = [i for i, x in enumerate(basechem) if x[i:i+2] == "Ar"]

i = RnL[0]
if basechem[i-1].islower() : i -= 2
else: i -= 1
j = ArL[-1]+2
rn = basechem[i:j]

s, n = reduct(rn)
print("grabRn: ", rn)
print("Reduced to ", s, n)
basechem = ''.join([basechem[:i], s, basechem[j:]])

RnL = [i for i, x in enumerate(basechem) if x == "R"]
ArL = [i for i, x in enumerate(basechem) if x == "A"]

print("RnL: ", RnL)
print("ArL: ", ArL)

exit(1)

def chsplit(s):
	l = s.find("Rn") - 1
	r = s.find("Ar") + 2
	a = s[l]
	if a.islower(): l -= 1
	m = s[l:r]
	return ''.join([s[:l], s[r:]]), m

exit(1)

while not done:
	basechem, molecule = chsplit(basechem)
	print(molecule, flush=True)

print ("Part2: creating \"e\" took", numsteps, "steps")

