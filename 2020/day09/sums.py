
class code:
	def __init__(self, fname, code_length) :
		self.code_length = code_length
		self.list = []
		self.lineno = code_length - 1
		self.f = open(fname, 'r')
		for line in open(fname, 'r'):
			self.list.append(int(line))

	def check(self, target) :
		this = self.lineno - self.code_length
		that = self.lineno 
		#print ("check from ", this, " to ", that)
		for i in range(this, that) :
			for j in range(this, that) :
				if i == j  : continue
				nums = self.list[i] + self.list[j]
				#print (" i: ", i, self.list[i], " j: ", j, self.list[j], "  total ", nums, " target = ", target)
				if nums == target : return True
		return False

	def next(self) : # returns next instruction
		self.lineno += 1
		nn = self.list[self.lineno]
		if not self.check(nn) :
			return nn
		return 0
		
	def contig(self, target, startIndex):
		num = self.list[startIndex]
		while num < target :
			startIndex += 1
			num += self.list[startIndex]
		#print("num: ", num, " target: ", target)
		if num == target : return startIndex
		return 0

cc = code("data.txt", 25)
num = cc.next()
while num == 0 : num = cc.next()
print ("Part 1:  At line ", cc.lineno + 1, " no sum equals ", num)

for sti in range(cc.lineno) :
	endi = cc.contig(num, sti)
	if endi == 0 : continue
	endi += 1
	#print ("num: ", num, "  sum: ", sum(cc.list[sti:endi]))
	print ("Part 2:  From index: ", sti, " To: ", endi, " value sum is: ", 
		min(cc.list[sti:endi]) + max(cc.list[sti:endi]) )
	break
