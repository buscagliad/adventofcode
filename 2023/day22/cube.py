
def isect(r1, r2):
	a, b = r1
	c, d = r2
	if c > b  or  a > d: return False
	if c <= a and a <= d: return True
	if a <= c and c <= b: return True
	print("ERROR", a, b, c, d) 

brickName=1

class Brick:
	def __init__(self, line):
		global brickName
		w=line.split(",")
		tilde = w[2].find("~")
		e1 = [int(w[0]),int(w[1]),int(w[2][:tilde])]
		e2 = [int(w[2][tilde+1:]),int(w[3]),int(w[4])]
		self.v = tuple(map(lambda i, j: j - i, e1, e2))
		self.xrange = [e1[0], e1[0]+self.v[0]]
		self.yrange = [e1[1], e1[1]+self.v[1]]
		self.zrange = [e1[2], e1[2]+self.v[2]]
		self.frozen = e1[2] == 1
		self.name = brickName
		#brickName = chr(ord(brickName)+1)
		brickName += 1
		self.isupport = []
		self.supportsme = []
		self.mark = False
	def markit(self):
		self.mark = True
	def doesSupport(self, nm):
		for b in self.isupport: 
			if b.name == nm: return True
		return False
	def supports(self, b):
		if b in self.isupport: return
		self.isupport.append(b)
	def supportedby(self, b):
		if b in self.supportsme: return
		self.supportsme.append(b)
	def dropto(self, z):
		if self.frozen : return 0
		if z > self.zrange[0]:
			print("ERROR - z range is bad for item", self.name, " drop to ",
				z, "from", self.zrange[0])
			exit(1)
		zd = self.zrange[1] - self.zrange[0]
		self.zrange[0]  = z
		self.zrange[1]  = z + zd
		return 1
	def xycover(self, ob):
		if ( isect(self.yrange, ob.yrange) and
		     isect(self.xrange, ob.xrange) ) : return True
		return False
	def intersect(self, ob):
		if ( isect(self.zrange, ob.zrange) and
		     isect(self.yrange, ob.yrange) and
		     isect(self.xrange, ob.xrange) ) : return True
		return False
	def out(self):
		print("Brick: ", self.name, " Frozen: ", self.frozen, self.xrange, self.yrange, self.zrange)
		for s in self.isupport:
			print("   supports ", s.name)
		for s in self.supportsme:
			print("   supports me ", s.name)
	def freeze(self):
		self.frozen = True

	
	

def freezecount():
	global bricks
	cnt = 0
	for b in bricks:	# skip all bricks above inb
		if b.frozen: cnt += 1
	return cnt

def countmarks():
	global bricks
	cnt = 0
	for b in bricks:	# skip all bricks above inb
		if b.mark: cnt += 1
		b.mark = False
	return cnt

def getbricks( znum):
	global bricks
	rlist = []
	for b in bricks:
		if b.zrange[0] == znum:
			rlist.append(b)
	return rlist
	
def getfrozen():
	global bricks
	rlist = []
	maxz = 0
	for b in bricks:
		if b.frozen:
			rlist.append(b)
			if maxz < b.zrange[0]: maxz = b.zrange[0]
	return rlist, maxz


bricks = []      
for line in open("data.txt", "r"):
	b = Brick(line.strip())
	bricks.append(b)
	
bricks.sort(key=lambda a: a.zrange[0], reverse=True)
		

maxz = 2
#
# determine 
#
maxz = 2
while maxz < 400:
	xlist = getbricks(maxz)
	flist, n = getfrozen()
	#print(len(xlist), len(flist))
	for x in xlist:
		fheight = -1
		fcover = []

		for f in flist:
			if x.xycover(f):
				#fcover.append(f)
				if f.zrange[1] > fheight: 
					fheight = f.zrange[1]
					fcover.clear()
				if f.zrange[1] == fheight:
					fcover.append(f)
		#print("Covers: ", len(fcover))
		for f in fcover:
			fheight = f.zrange[1]+1

			x.dropto(fheight)
			x.freeze()
			f.supports(x)
			x.supportedby(f)
			#print(x.name, " dropped to ", fheight,
			#	" supported by ", f.name)
		if len(fcover) == 0:
			x.dropto(1)
			x.freeze()
		#	f.supports(x)
		#	x.supportedby(f)
		#	print(x.name, " dropped to ", fheight,
		#		" supported by ", f.name)
			
	bricks.sort(key=lambda a: a.zrange[0], reverse=True)
	maxz += 1

cset = set()
def markem(b):
	if len(b.isupport) == 0 : return
	for i in b.isupport:
		i.markit()
		markem(i)

def markcheck():
	global bricks
	for i in b.isupport:
		i.markit()
		collapse(i)
	

def collapsex(b, clear=True):
	markem(b)
	markcheck()
	if len(b.isupport) == 0 : return
	for i in b.isupport:
		i.markit()
		collapsex(i)

cset = dict()
def collapse(b, clear=True):
	global cset
	if clear: cset.clear()

	for i in b.isupport:
		addit = True
		if len(i.supportsme) > 1:
			for s in i.supportsme:
				if not s.name in cset.keys():
					addit = False
		if addit:
			cset[i.name] = i
			collapse(i, False)

	return len(cset)
		
colb = 0


n = 1
remb = 0
for b in bricks:
	if len(b.isupport) == 0: 
		remb += 1
		#print(b.name, " does not support any brick count: ", remb)
	else:
		otherSupportCount = 0
		#print("\n\nChecking on ", b.name, " has ", len(b.isupport))
		#for isup in b.isupport: print("       -> ", isup.name)
		for isup in b.isupport:
			# check to see if another brick supports this brick
			ok = False
			for cb in bricks:
				if cb.name == b.name: continue
				if cb.doesSupport(isup.name):
					ok = True
			if ok: otherSupportCount += 1
		if otherSupportCount == len(b.isupport):
			remb += 1
		else:
			c = collapse(b)
			#c = countmarks()
			#print("calling collapse for ", b.name, " :: ", c)
			colb += c

print("Part 1, we can disintegrate", remb, "bricks")

print("Part 2, a total of", colb, "bricks will fall")
		
## 114230 is too high

# 101541

#for b in bricks:
#	b.out()
