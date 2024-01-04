
HIGH    = 1
LOW     = 2
NOPULSE = 3

STYPE=["xxx", " -high-> ", " -low-> ", " ->|"]
PTYPE=["xxx", "HIGH", "LOW", "NOPULSE"]

class Sync:
	def __init__(self, nm):
		self.on = False
		self.sendto = []
		self.toSend = NOPULSE
		self.lastSent = NOPULSE
		self.name = nm
	#
	# each tomod connects this module with 'who' it sends to
	#
	def output(self, tomod):
		pass
		
	#
	# this module does not care about who sends it pulses
	#
	def input(self, frommod):
		pass

	#
	# the broadcaster calls this method to inform FlipFlop
	# that it is to receive a pulse of a the given type
	def inpulse(self, fm, ptype):
		pass
	#
	# the broadcaster will then query this module for all
	# modules it will send to, along witht the type of pulse
	#
	def outpulse(self, nm, pt):
		return self.sendto
	def origstate(self):
		return True
	
class FlipFlop:
	def __init__(self, nm):
		self.on = False
		self.sendto = []
		self.toSend = NOPULSE
		self.lastSent = NOPULSE
		self.name = nm
		self.debug = False
		#if nm == "b": self.debug = True
	#
	# each tomod connects this module with 'who' it sends to
	#
	def output(self, tomod):
		self.sendto.append([self.name, tomod, NOPULSE])
		
	#
	# this module does not care about who sends it pulses
	#
	def input(self, frommod):
		pass
		
	#
	# the broadcaster calls this method to inform FlipFlop
	# that it is to receive a pulse of a the given type
	def inpulse(self, fm, ptype):
		if self.debug:
			print(self.name, " inpulse is ", PTYPE[ptype])
		if ptype == NOPULSE:
			self.toSend = NOPULSE
			return # do nothing
		elif ptype == HIGH:
			self.toSend = NOPULSE
			return	# do nothing
		elif ptype == LOW:
			if self.on:
				self.on = False
				self.toSend = LOW
			else:
				self.on = True
				self.toSend = HIGH
	#
	# the broadcaster will then query this module for all
	# modules it will send to, along witht the type of pulse
	#
	def outpulse(self, nm, pt):
		if not (self.toSend == NOPULSE):
			self.lastSent = self.toSend
		else:
			return []
		for s in self.sendto:
			s[2] = self.lastSent
		return self.sendto
	
	def origstate(self):
		if self.on == False: # and self.toSend == NOPULSE:
			return True
		return False

class Conjunction:
	def __init__(self, nm):
		self.toSend = NOPULSE
		self.lastSent = NOPULSE
		self.sendto = []
		self.cares = []
		self.rcvd = {}
		self.name = nm
		self.debug = False
		self.needinput = 0
	#
	# each tomod connects this module with 'who' it sends to
	#
	def output(self, tomod):
		self.sendto.append([self.name, tomod, NOPULSE])
	#
	# this module keeps track of who sends pulses to it
	#
	def input(self, frommod):
		self.needinput += 1
		self.cares.append(frommod)
		#print(self.name, " adding ", frommod.name)
		self.rcvd[frommod.name] = LOW

	#
	# outpulse returns a list of modules and pulse types
	# this Conjuction will send to
	def outpulse(self, f, ptype):
		#if not self.toSend == NOPULSE:
		self.lastSent = self.toSend
		print("Conjuction: ", self.name, " received ", len(self.rcvd), 
			" inputs  GOOD: ", len(self.rcvd) == self.needinput)
		if False and not len(self.rcvd) == self.needinput:
			return []
		tosend = LOW
		for m in self.cares:
			if True or self.debug: print(self.name, " checking ", m.name, " for what it sent: ", m.toSend)
			if self.rcvd[m.name] == LOW:
				tosend = HIGH
		for s in self.sendto:
			s[2] = tosend
		return self.sendto
	#
	# inpulse is called by the broadcaster to inform
	# this module of the type of pulse it is receiving
	# this module looks at each module that is connected to it
	# to see what the last pulse they sent was
	# 
	def inpulse(self, fm, ptype):
		self.rcvd[fm] = ptype
		print("inpulse - from ", fm, " pulse; ", PTYPE[ptype])
		if ptype == NOPULSE:
			self.toSend = NOPULSE
		else:
			tosend = LOW
			for m in self.cares:
				if self.debug: print(self.name, " checking ", m.name, " for what it sent: ", m.toSend)
				if m.lastSent == LOW or m.lastSent == NOPULSE:
					tosend = HIGH
			self.toSend = tosend

	def origstate(self):
		for m in self.cares:
			if m.lastSent == HIGH:
				return False
		return True

class Broadcaster:
	def __init__(self):
		self.on = False
		self.sendto = []
		self.toSend = NOPULSE	
		self.name = "broadcaster"
		self.lowPulsesSent = 0
		self.highPulsesSent = 0
		self.buttonCalls = 0
		self.debug = False

	def output(self, tomod):
		self.sendto.append([self.name, tomod, LOW])

	def send(self):
		slist = self.sendto
		loop = 1
		while slist:
			m = slist.pop()
			##
			## create list of pulses to send
			##
			for m in slist:
				ptype = m[2]
				if self.debug: print(loop, ":: ", m[0], STYPE[ptype], m[1].name)
				m[1].inpulse(m[0], ptype)
				if ptype == HIGH:
					self.highPulsesSent += 1
				elif ptype == LOW:
					self.lowPulsesSent += 1
			
			nlist = []
			##
			## get from each oject the obj,pulse to send out 
			##
			for m in reversed(slist):
				#if m[2] == NOPULSE: continue
				#if m[0] == 'b':
				#	print("b Sending to ", m[1].name, " ", PTYPE[m[2]])
				alist = m[1].outpulse(m[0], m[2])
				for a in alist:
					nlist.append(a)
				
			##
			## nlist has the order list of object and pulses to send
			##
			slist = nlist
			loop += 1
		if self.debug: 
			print(self.name, " sent ", self.lowPulsesSent, " low pulses, and ",
				self.highPulsesSent, " high pulses")

	def retstate(self):
		global modules
		callButtonAgain = True
		for k in modules:
			s = modules[k]
			if not s.origstate():
				if self.debug: print(s.name, " NOT in original state")
				callButtonAgain = False
			else:
				if self.debug: print(s.name, " IS IN original state")
		return callButtonAgain

	def dobutton(self):
		self.toSend = LOW
		self.lowPulsesSent += 1
		self.buttonCalls += 1
		# print(self.buttonCalls, ":: Calling button")
		self.send()
		return

	def button(self, n):
		for i in range(n): 
			self.dobutton()
			if self.retstate():
				print(self.name, " sent ", self.lowPulsesSent, " low pulses, and ",
				self.highPulsesSent, " high pulses")
				print("Returned to original state at: ", i+1)
		print(self.name, " sent ", self.lowPulsesSent, " low pulses, and ",
				self.highPulsesSent, " high pulses")
		return self.lowPulsesSent * self.highPulsesSent
			
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
			print("Creating sync ", tnm)
		modules[nm].output(modules[tnm])
		if inp: modules[tnm].input(modules[nm])
		
bm = modules["broadcaster"]

print("Part 1: low * high pulses after 1000 button presses: ", bm.button(1000))

## 2927575310 is too high
##  788081152
##
## broadcaster orchestrates ALL comms
##
## starts with sending to his associates,
## then asks his associates who they want to sent to
## the broadcaster then tells each of the intended targets which pulse they are to receive,
## then, they in turn tell the broadcaster who to send and what pulses...
## this continues until no pulses are sent
##
