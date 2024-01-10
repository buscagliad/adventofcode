
HIGH    = 1
LOW     = 2
NOPULSE = 3

lowPulsesSent = 0
highPulsesSent = 0

STYPE=["xxx", " -high-> ", " -low-> ", " ->|"]
PTYPE=["xxx", "HIGH", "LOW", "NOPULSE"]

loop = 0

class Module:
	def __init__(self, nm):
		self.sendto = []
		self.sendfrom = []
		self.toSend = NOPULSE
		self.name = nm	
	#
	# each tomod connects this module with 'who' it sends to
	#
	def output(self, tomod):
		self.sendto.append(tomod)

	#
	# only the Conjuction module will require this
	#
	def input(self, frommod):
		self.sendfrom.append(frommod)
	#
	# the send method will count high/low pulses and add to q
	#
	def send(self, q, nm):
		global highPulsesSent 
		global lowPulsesSent 
		if self.toSend == HIGH: highPulsesSent += 1
		elif self.toSend == LOW: lowPulsesSent += 1
		q.append((self.name, nm, self.toSend))
		#print(self.name, STYPE[self.toSend], nm)
	
	def activate(self, q):
		if self.toSend != NOPULSE:
			for tomod in self.sendto:
				self.send(q, tomod)
		self.toSend = NOPULSE
				
	## virtual functions:
	## def inpulse - receives a pulse from a sender
	## def origstate - returns True when at original state
	## def 
		
class Sync(Module):
	def __init__(self, nm):
		super().__init__(nm)
	def inpulse(self, fm, ptype):
		global loop
		if (ptype == LOW):
			print("LOW Loop count is: ", loop)
		
	def outpulse(self, nm, _):
		return self.sendto
	def origstate(self):
		return True
	
class FlipFlop(Module):
	def __init__(self, nm):
		self.on = False
		self.debug = False
		super().__init__(nm)

	#
	# the broadcaster calls this method to inform FlipFlop
	# that it is to receive a pulse of a the given type
	def inpulse(self, fm, ptype):
		if self.debug:
			print(self.name, " inpulse is ", PTYPE[ptype])
		if ptype == LOW:
			if self.on:
				self.on = False
				self.toSend = LOW
			else:
				self.on = True
				self.toSend = HIGH

	def origstate(self):
		if self.on == False: # and self.toSend == NOPULSE:
			return True
		return False

class Conjunction(Module):
	def __init__(self, nm):
		self.sendfrom = []
		self.rcvd = {}
		self.debug = False
		super().__init__(nm)
	#
	# this module keeps track of who sends pulses to it
	#
	def input(self, frommod):
		self.sendfrom.append(frommod)
		#print(self.name, " adding ", frommod.name)
		self.rcvd[frommod] = LOW



	#
	# inpulse is called by the broadcaster to inform
	# this module of the type of pulse it is receiving
	# this module looks at each module that is connected to it
	# to see what the last pulse they sent was
	# 
	def inpulse(self, fm, ptype):
		self.rcvd[fm] = ptype
		# print("inpulse - from ", fm, " pulse; ", PTYPE[ptype])
		tosend = LOW
		for m in self.sendfrom:
			if False: print(self.name, " checking ", fm, " for what it sent: ", self.rcvd[m])
			if self.rcvd[m] == LOW:
				tosend = HIGH
		self.toSend = tosend

	def origstate(self):
		for m in self.sendfrom:
			if m.lastSent == HIGH:
				return False
		return True

class Broadcaster(Module):
	def __init__(self):
		self.buttonCalls = 0
		self.debug = False
		super().__init__("broadcaster")

	def inpulse(self, fm, ptype):
		# print("inpulse - from ", fm, " pulse; ", PTYPE[ptype])
		self.toSend = ptype

	def origstate(self):
		return True
		

#
# first create all of the classes
#
modules = {}
infile = "data.txt"
for line in open(infile, 'r'):
	if line[:11] == "broadcaster":
		modules["broadcaster"] = Broadcaster()
	else:
		ix = line.find(" -> ")
		nm = line[1:ix]
		if line[0] == '%':
			modules[nm] = FlipFlop(nm)
		elif line[0] == "&":
			modules[nm] = Conjunction(nm)
		elif line[0] == "|":
			modules[nm] = Sync(nm)

for line in open(infile, 'r'):
	inp = True
	if line[:11] == "broadcaster":
		nm = "broadcaster"
		inp = False
	else:
		ix = line.find(" -> ")
		nm = line[1:ix]

	nline = line[line.find(" -> ") + 4:]
	tomods = nline.strip().split(",")
	#print(line, "| nm = ", nm, "| nline = ", nline, "| tomods = ", tomods)
	for t in tomods:
		tnm = t.lstrip()
		if not tnm in modules:
			modules[tnm] = Sync(tnm)
			#print("Creating sync ", tnm)
		modules[nm].output(modules[tnm].name)
		if inp: modules[tnm].input(modules[nm].name)
		
bm = modules["broadcaster"]

## who talks to 'rx' ?
## if it is a Conjunction (which it is)
## need to find all the inputs to the Conjuction
##
rx = modules['rx']

m = rx.sendfrom[0]	# module connect to rx

inlist = []
for a in modules:
	mods = modules[a]
	if len(mods.sendto) > 0 and m == mods.sendto[0]:
		inlist.append(a)
		#print(a)
	
loops = []
for a in inlist:
	loops.append([modules[a], 0])


jz = modules["jz"]
jzloop = 0
ft = modules["ft"]
ftloop = 0
ng = modules["ng"]
ngloop = 0
sv = modules["sv"]
svloop = 0
kmstate = False
done = False
for i in range(100000000):
	if done: break
	lowPulsesSent += 1
	bm.inpulse("button", LOW)
	slist = []
	bm.activate(slist)
	#print("    low pulse: ", lowPulsesSent, "  high pulses: ", highPulsesSent)
	loop += 1
	while not done and slist:
		frm, modnm, ptype = slist.pop(0)
			
		##
		## create list of pulses to send
		##
		if False: print(loop, ":: ", frm, STYPE[ptype], modnm)
		tomod = modules[modnm]
		tomod.inpulse(frm, ptype)
		for a in loops:
			if a[1] == 0 and a[0].toSend == HIGH:
				a[1] = loop

		done = True
		for a in loops:
			if a[1] == 0:
				done = False

		tomod.activate(slist)
			
		##
		## nlist has the order list of object and pulses to send
		##
	if (loop == 1000):
		print("Part 1: low * high pulses after 1000 button presses: ", lowPulsesSent * highPulsesSent)


prod = 1
for a in loops:
	prod *= a[1]

print("Part 2: Number of button presses to set rm to HIGH: ", prod)
