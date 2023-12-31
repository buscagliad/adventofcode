import copy


def parttest(tlist, t, val):
	if t[0] == 0 and t[1] == 0 and t[2] == 0:
		return tlist[3]
	#print ("parttest", tlist)
	if t == tlist[0]:
		if tlist[1] == '>':
			#print(tlist[0], " : ", val, " > ", tlist[2], "  ", val>tlist[2])
			if val > tlist[2]:
				#print("parttest Returning ", tlist[3])
				return tlist[3]
		elif tlist[1] == '<':
			#print(tlist[0], " : ", val, " < ", tlist[2], "  ", val<tlist[2])
			if val < tlist[2]:
				#print("parttest Returning ", tlist[3])
				return tlist[3]
	return	# None

# function will remove the quad set rem from quads, 
# splitting it into more sections as needed 
#def intersect(quads, rem):
	

class Work:
	def __init__(self, line):
		s = line.find('{')
		self.name = line[:s]
		tests = line[s+1:].strip().split(',')
		self.tests=[]
		#print (tests)
		for tst in tests:
			tx = tst.split(':')
			t = tx[0]
			#print(tx)
			if '>' == t[1]:
				n = [t[0], t[1], int(t[2:]), tx[1]]
			elif '<' == t[1]:	
				n = [t[0], t[1], int(t[2:]), tx[1]]
			else:
				n = [0, 0, 0, tx[0][:tx[0].find('}')]]
			self.tests.append(n)
	def test(self, t, xmas):
		#print("WF: ", self.name, "  t: ", t, "  xmas: ", xmas)
		for tst in self.tests:
			r = parttest(tst, t, xmas)
			if r : 
				# print("Return from parttest is ", r)
				return r
	def fulltest(self, xmas):
		#print("WF: ", self.name, "  t: ", t, "  xmas: ", xmas)
		for tst in self.tests:
			r = parttest(tst, 'x', xmas[0])
			if not r:
				# r = tst.test('m', xmas[1])
				r = parttest(tst, 'm', xmas[1])
			else:
				return r
			if not r:
				# r = tst.test('a', xmas[2])
				r = parttest(tst, 'a', xmas[2])
			else:
				return r
			if not r:
				# r = tst.test('s', xmas[3])
				r = parttest(tst, 's', xmas[3])
			if r:
				return r
		return self.default()
	def default(self):
		return self.tests[-1][3]
	def out(self):
		print("Workflow: ", self.name)
		for tst in self.tests:
			print(" -- ", tst)
		

def part(line):
	w = line.strip().split(',')
	return int(w[0][3:]), int(w[1][2:]), int(w[2][2:]), int(w[3][2:w[3].find('}')])

def getflow(wf, name):
	for w in wf:
		if w.name == name: return w
	print("ERROR - cannot find workflow: ", name)
	for w in wf:
		w.out()
	
def process(line):
	global flows
	xmas=part(line)
	#print(xmas, sum(xmas))
	done = False
	r = None
	useflow = "in"
	while not done:
		inf = getflow(flows, useflow)
		useflow = inf.fulltest(xmas)
		if useflow == "A": return sum(xmas)
		elif useflow == "R": return 0
		# print("Useflow: ", r)

	

first = True
flows = []
part1 = 0
for line in open('data.txt', 'r'):
	if len(line) < 2:
		first = False
		continue
	if first:
		w = Work(line)
		flows.append(w)
	else:
		xmas=part(line)
		#print(xmas, sum(xmas))
		p = process(line)
		#if p > 0: print("ACCEPT: ", line.strip())
		#else:     print("REJECT: ", line.strip())
		part1 += p

print("Part 1: sum of accepted parts is: ", part1)

class Seg:
	def __init__(self, nm):
		self.a = 1
		self.b = 4000
		self.name = nm
	#
	# l < h always
	# l == 1 or h == 4000 always
	# if l == 1 and h == 4000 - do nothing
	# a <= l <= b segment (a, b) becomes (a, l-1)
	# a <= h <= b segment (a, b) becomes (h-1, b)
	def cut(self, l, h):
		if h < l or l < 1 or h > 4000:
			return 
		#print(self.name, " removing segment: ", l, h)
		a = self.a
		b = self.b
		if h < a or b < l:
			self.a = 0	# empty
			self.b = 0	# empty
			print("ERROR - empty!!", self.name, self.a, self.b)
		elif a < h < b:
			self.b = h
		elif a < l < b:
			self.a = l
		else:
			print("ERROR")

	def length(self):
		return self.b - self.a + 1

	def out(self):
		a = self.a
		b = self.b
		print(self.name, ":  %4d - %4d : %4d" % (a, b, b-a+1))



def doprint(xmas):
	for i in ['x', 'm', 'a', 's']:
		xmas[i].out()

## split returns xmas with 'ch' <= n and 'ch' > n
# lt will have the interval less than or equal to removing [n+1, 4000] from the 'ch' interval
# gt will have the interval greater than n after removing [1,n] from the 'ch' interval
## NOTE: lt union gt is xmas
## NOTE: for x < v, splitgt(xmas, 'x', v) returns x < v as arg 1 and the 'rest' as arg 2
##       for x > v, splitgt(xmas, 'x', v-1) returns x < v+1 as arg 1 and the 'rest' (x > v) as arg 2
		
def splitgt(xmas, ch, n):
	if ch not in ['x', 'm', 'a', 's']:
		print("ERROR in splitgt - bad ch:", ch)
		exit(1)
	lt = copy.deepcopy(xmas)
	gt = copy.deepcopy(xmas)
	lt[ch].cut(n+1, 4000)
	gt[ch].cut(1,n)
	return lt, gt



rejects = []
accepts = []

def doflow(nm, inr, i):
	global rejects
	global accepts
	global flows
	#doprint(inr)
	if nm == 'R': 
		#print("REJECT found")
		#doprint(inr)
		rejects.append(inr)
		return
	elif nm == 'A':
		#print("ACCEPT found")
		#doprint(inr)
		accepts.append(inr)
		return
	w = getflow(flows, nm)
	#print(w)
	#if not w:
	#	print("Failed on ", nm, " i = ", i)
	#if len(w.tests) == 0: return
	if i < len(w.tests):
		t = w.tests[i]
	else:
		print("HELP")
		exit(1)
	ch    = t[0]
	carat = t[1]
	v     = t[2]
	nxt   = t[3]
	#print(ch, carat, v, nxt)
	if ch == 0:
		#print("GETTING next flow, ", nxt)
		doflow(nxt, inr, 0)
	
	if carat == '>':
		nxtu, otr = splitgt(inr, ch, v)
		doflow(nxt, nxtu, 0)
		doflow(nm, otr, i+1)
		
	elif carat == '<':
		otr, nxtu  = splitgt(inr, ch, v-1)
		doflow(nxt, nxtu, 0)
		doflow(nm, otr, i+1)

	else:
		pass
		#print("ERROR  in doflow A", carat)
		#exit(1)
	#doflow(nxt, nxtu, i+1)


def make_xmas():
	xmasF = {}
	xmasF['x'] = Seg('x')
	xmasF['m'] = Seg('m')
	xmasF['a'] = Seg('a')
	xmasF['s'] = Seg('s')
	return xmasF

def prod_xmas(xm):
	prod = 1
	prod *= xm['x'].length()
	prod *= xm['m'].length()
	prod *= xm['a'].length()
	prod *= xm['s'].length()
	return prod

xmasF = make_xmas()
doflow('in', xmasF, 0)

s = 0
for r in accepts:
	s += prod_xmas(r)

print("Part 2: total number of acceptable part numbers is: ", s)


