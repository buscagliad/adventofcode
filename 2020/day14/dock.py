import copy

def setBit(v, b) :
	m = 1 << b
	return v | m
	
def clearBit(v, b) :
	m = ~(1 << b)
	return v & m

def isBit(v, b) :
	m = 1 << b
	if m & v : return True
	return False

def createBitList(v, maxbits = 36) :
	bl = ['0'] * maxbits
	m = 1 << maxbits - 1
	for n in range(maxbits) :
		if m & v : 
			bl[n] = 1 
		else : 
			bl[n] = 0
		m >>= 1
	return bl

def evalBitList(v):
	n = len(v) - 1
	p2 = 1 << n
	sum = 0
	i = 0
	while i <= n :
		if v[i] == 1 : sum += p2
		p2 >>= 1
		i += 1
	return sum

def indexSearch(v, n) :
	sl = []
	i = 0
	while n in v[i:] :
		i = v.index(n, i)
		# print(i)
		sl.append(i)
		i += 1
	#print(sl)
	return sl

def expandBitList(v) :
	ind = indexSearch(v, 2)
	n2s = len(ind)
	bl = []
	for n in range(2**n2s) :
		cv = copy.deepcopy(v)
		k = 0
		for i in range(len(v)) :
			if v[i] == 2 :
				cv[i] = isBit(n, k)
				k += 1
		bl.append(evalBitList(cv))
	return bl
	
class memman :
	def __init__ (self) :
		self.memlist = []
		self.values = []

	def add(self, mlist, value):
		## mlist is list of memory cells to place value
		for mem in mlist :
			#print ("add: ", mem, mlist)
			if mem in self.memlist:
				ix = self.memlist.index(mem)
				#print("mem ", mem, "ix ", ix, "replace value ", value)
				self.values[ix] = value
			else :
				self.memlist.append(mem)
				self.values.append(value)
				#print("added ", mem, " value ", value)
		#print("Size of memory is ", len(self.memlist), len(self.values))
		
	def sum(self) :
		return sum(self.values)
	
	def dump(self) :
		for i in range(len(self.memlist)) :
			print("i ", i, "  mem: ", self.memlist[i], "  val: ", self.values[i])


class LoadV1 :
	def __init__ (self, fname, memsize):
		self.mem = [0] * memsize
		self.max = memsize
		for line in open(fname, 'r') :
			if line[:4] == "mask" :
				mask = list(line[7:])
			else :
				ix = line.find("[") + 1
				jx = line.find("]") 
				memi = int(line[ix:jx])
				ix = line.find("=") + 1
				value = int(line[ix:])
				# print("line : ", line, "  memi ", memi, "  value: ", value)

				bi = 0
				mi = 35
				while mi >= 0 :
				    if mask[bi] == '1' : value = setBit(value, mi)
				    elif mask[bi] == '0' : value = clearBit(value, mi)
				    mi -= 1
				    bi += 1
				self.mem[memi] = value
			#        333333222222222211111111110000000000
			#        543210987654321098765432109876543210
			# mask = X01X10X11101011X1X0XX010011X0101X001
	def sum(self) :
		return sum(self.mem)


#
class LoadV2 :
	def __init__ (self, fname):
		self.mem = memman()
		for line in open(fname, 'r') :
			if line[:4] == "mask" :
				mask = list(line[7:])
				#print("line : ", line, "  mask ", mask)
			else :
				ix = line.find("[") + 1
				jx = line.find("]") 
				memi = int(line[ix:jx])
				mlist = createBitList(memi)
				ix = line.find("=") + 1
				value = int(line[ix:])
				#print("line : ", line, "  memi ", memi, "  value: ", value)

				bi = 0
				mi = 35
				while mi >= 0 :
					if mask[bi] == '1': 
						mlist[bi] = 1
					elif mask[bi] == 'X' : 
						mlist[bi] = 2
					mi -= 1
					bi += 1
				#
				## at this point, we have a parsed memory location with 2's in it
				#
				bl = expandBitList(mlist)
				self.mem.add(bl, value)
				#print(bl)
				
	def sum(self) :
		return self.mem.sum()

#bl = createBitList(1562532)
#bl[3] = 2
#bl[1] = 2
#bl[15] = 2
#nbl = expandBitList(bl)
#for j in nbl :
#	print("bl: ", j)
#	print("   ", createBitList(j))

l = LoadV1("data.txt", 66000)
print("Part 1: memory sum is: ", l.sum())
l = LoadV2("data.txt")
#l.mem.dump()
print("Part 2: memory sum is: ", l.sum())
