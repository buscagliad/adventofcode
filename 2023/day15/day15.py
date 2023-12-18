

hashes=[]
hval=0

f = open("data.txt", "r")
line = f.read()
#line="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
num = 1
label = ""
eq = False
lens = -1
hval = 0
lval = 0
for a in line:
	if a == ',':
		num += 1
		done = True
	elif a == '\n':
		done = True
	else:
		if a == '=':
			eq = True
		elif eq:
			lens = int(a)
		if a == '-' or a == '=':
			lval = hval
		elif not a.isdigit():
			label = ''.join([label, a])
		hval  += ord(a)
		hval  *= 17
		hval  =  hval % 256
		done = False
	if done:
		done = False
		hashes.append([label, eq, lens, lval, hval])
		# if (eq):
			# print("Label: ", label, " lens: ", lens, "  BOX: ", lval)
		# else:
			# print("Label: ", label, " -  HASH: ", hval)
		label = ""
		eq = False
		lens = -1
		hval = 0
		lval = 0
Box = []
for i in range(256):
	Box.append([])

s = 0
for l, e, lens, b, h in hashes:
	s += h

print("Part 1 - sum of hashes is: ", s)

for l, e, lens, b, h in hashes:
	if e:
		found = False
		for bx in Box[b]:
			if bx[0] == l:
				bx[1] = lens
				found = True
		if not found:
			Box[b].append([l, lens])
	else:
		found = False
		for bx in Box[b]:
			if bx[0] == l:
				Box[b].remove(bx)
				break

s = 0
for h in range(256):
	if len(Box[h]) > 0:
		bn = 1
		for bx in Box[h]:
			#print("Box: ", h, bx)
			s += (h+1) * bn * bx[1]
			bn += 1

print("Part 2: sum of the lens powers is: ", s)

			
