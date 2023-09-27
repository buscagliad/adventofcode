
class Entry:
	def __init__(self, fieldName, r1low, r1high, r2low, r2high) :
		self.fieldName = fieldName
		self.r1low = r1low
		self.r1high = r1high
		self.r2low = r2low
		self.r2high = r2high
		self.tindex = -1	## ticket index
		
	def setTicketIndex(self, n) :
		#print (self.fieldName, " index set to ", n, "  from ", self.tindex)
		self.tindex = n

	def valid(self, value) :
		if self.r1low <= value and value <= self.r1high :
			return True
		if self.r2low <= value and value <= self.r2high :
			return True
		return False
	
	def display(self):
		print (self.fieldName, self.tindex, self.r1low, self.r1high, self.r2low, self.r2high)

class Ticket:
	def __init__(self, f):
		l = f.readline()
		self.nums = []
		self.valid = False
		if l == "" or l == "\n" : return
		self.valid = True
		if l[:4] == "your" or l[:4] == "near" : l = f.readline()
		results = l.split(',')
		for r in results:
			if r == "\n" : continue
			self.nums.append(int(r))
		if (len(self.nums) < 2) : self.valid = False
		
	def errorValue(self, eranges):
		ev = 0
		nev = 0
		rv = True
		for n in self.nums:
			nev = n
			lrv = False
			for e in eranges:
				if e.valid(n) : 
					lrv = True
					nev = 0
			ev += nev
			rv &= lrv
		self.valid = (ev == 0)
		return rv, ev
		
	def printValidFields(self, eranges):
		for n in self.nums:
			for e in eranges:
				if e.valid(n) : 
					print("  ", e.fieldName)
		
	def display(self, n):
		print (n, self.nums)

def getEntry(f):
	fields = []
	l = f.readline()
	while len(l) > 2:
		ix = l.index(':')
		fname = l[:ix]
		nl = l[ix:]
		delimiters = [":", "-"]
		for d in delimiters:
			nl = " ".join(nl.split(d))
		result = nl.split()
		#print (result)
		fields.append(Entry(fname, int(result[0]), int(result[1]),
										int(result[3]), int(result[4])))
		l = f.readline()
	return fields

def getRows(field, tix) :
	cnt = [0]*20
	nvt = 0
	for t in tix :
		#if t.valid :
		nvt += 1
		for ix in range(20) :
			n = t.nums[ix]
			if field.valid(n) : cnt[ix] += 1
	# print(nvt)
	for ix in range(20) :
		if cnt[ix] == nvt : cnt[ix] = 1
		else : cnt[ix] = 0
	# print (field.fieldName, " T: ", cnt)
	return cnt
				
def numGoodTickets(tix) :
	cnt = 0
	for t in tix :
		if t.valid : cnt += 1
	return cnt

f = open("data.txt", "r")
fields = getEntry(f)

myTicket = Ticket(f)

f.readline()

nearTickets = []
nTicket = Ticket(f)
scanningErrorRate = 0
line = 0
while nTicket.valid:
	line += 1
	#nTicket.display()
	good, ev = nTicket.errorValue(fields)
	if not good :
		scanningErrorRate += ev
	else :
		nearTickets.append(nTicket)
	nTicket = Ticket(f)


print ("Part 1 - scanning error rate is: ", scanningErrorRate)
scanningErrorRate = 0
n = 1

tvec = []
for f in fields :
	tvec.append(getRows(f, nearTickets))

def findIndex(tlist, tvalue):
	for n in range(len(tlist)) :
		if tlist[n] == tvalue : return n
	return -1

s = 10000

while s > 0 :
	ti = 0
	for tvi in range(len(tvec)) :
		t = tvec[tvi]
		if (sum(t) == 1) :
			ix = findIndex(t, 1);
			for g in tvec : g[ix] = 0
			fields[tvi].setTicketIndex(ix)

	s = 0
	for t in tvec:
		s += sum(t)
	
# print ("Good tickets: ", numGoodTickets(nearTickets))
departureProduct = 1

#
# departure items are 0 .. 5
#
for f in fields :
	if f.fieldName[:9] == "departure" :
		#print (f.fieldName, " index: ", f.tindex, " My TickValue: ", myTicket.nums[f.tindex])
		departureProduct *= myTicket.nums[f.tindex]
print ("Part 2 - departure product rate is: ", departureProduct)
#       X  X                                  X           X      X      X
#       3  0                                  5           4   2  1
# 181,131,61,67,151,59,113,101,79,53,71,193,179,103,149,157,127,97,73,191
