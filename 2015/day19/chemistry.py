import copy
import random

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
numsteps = 0

done = False
while not done:
	chem = copy.deepcopy(basechem)
	count = 0
	numsteps = 0
	while  (not chem == "e") and count < 10000:
		[f, t] = random.choice(steps)
		chem, n = rem(chem, t, f)
		numsteps += n
		count += 1
	if chem == "e" : done = True
		
print ("Part2: answer: ", numsteps)
