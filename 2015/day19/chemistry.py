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

def rem(chem, f, to):
	r = 0
	n = 0
	i = 0
	d = len(f)
	newch = copy.deepcopy(chem)
	while i < len(chem) - 1:
		i = newch.find(f)
		if (i < 0) : break
		print("Found ", f, " at ", i, " replaced with ", t)
		n += 1
		print("old chem: ", newch)
		newch = ''.join([newch[:i], to, newch[i+d:]])
		print("new chem: ", newch)
	#print("retset is ", retset)
	return newch, n

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

def getatoms(s):
	atoms=[]
	for t, f in s:
		if "Rn" in f:
			atoms.append([t,f])
	print(atoms)
	return atoms

atoms = getatoms(steps)
print(basechem)

def ARsplit(s):
	spaces = ""
	rndepth = -1
	rl = -1
	rr = -1
	returnl = -1
	returnr = -1
	rdepth = 0
	for i in range(len(s)-1):
		if s[i:i+2] == "Rn":
			if rr < 0: rdepth += 1
			print("  "*rdepth, "Rn found at ", i)
			rl = i - 2
			rr = -1
		if s[i:i+2] == "Ar":
			if rndepth < rdepth:
				rndepth = rdepth
				returnl = rl 
				returnr = i + 2
			if rr > 0: 			
				rdepth -= 1
			print("  "*rdepth, "Ar found at ", i)
			rr = i + 2
	print("ARsplit returning ", returnl, returnr)
	return returnl, returnr

if "Bi" in basechem:
	print("Bi found 1")
	exit(1)
	
done = False
while not basechem == "e" and not done:
	done = True
	for t,f in atoms:
		basechem, k = rem(basechem, f, t)
		numsteps += k
		if k > 0: done = False
		print(f, "  appears: ", k, " times.", " total: ", numsteps, flush=True)
		if "Bi" in basechem:
			print("Bi found 2", t, f, numsteps)
			exit(1)
#
# grab xxRn...Ar molecules as see what they have inside them
#
def grabRn(s, nAr = 1):
	r = s.find("Ar") + 2
	for j in range(nAr):
		l = s.find("Rn")
	ll = l
	while ll < r:
		ll = s.find("Rn", l + 1)
		if ll < r: l = ll
	if s[l-1].islower(): l -= 2
	else: l -= 1
	print(l, r)
	print(s[:l], s[l:r], s[r:], sep="")
	return s[l:r], s[:l], s[r:]

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
	 
print (basechem)

rn, l, r = grabRn(basechem)
n = 1
nAr = 1
while len(rn) and n > 0:
	s, n = reduct(rn)
	print("grabRn: ", rn)
	print("Reduced to ", s, n)
	basechem = ''.join([l, s, r])
	print("NAMES: ", "|", l, "|", s, "|", r, "|", sep="")
	print (basechem)
	if "Bi" in basechem:
		print("Bi found 3", s, n, numsteps)
		exit(1)
	numsteps += n
	if n == 0: 
		nAr += 1
		n = 1 # keep look going
		print("Increased nAr to: ", nAr)
	rn, l, r = grabRn(basechem, nAr)
exit(1)

def chsplit(s):
	l = s.find("Rn") - 1
	r = s.find("Ar") + 2
	a = s[l]
	if a.islower(): l -= 1
	m = s[l:r]
	return ''.join([s[:l], s[r:]]), m
	
done = False
ARsplit(basechem)

exit(1)

while not done:
	basechem, molecule = chsplit(basechem)
	print(molecule, flush=True)

print ("Part2: creating \"e\" took", numsteps, "steps")

