import numpy as np
from itertools import combinations
import bitstring

def seqcount(q, m):
	c = 0
	a = []

	#print(q)
	for i in q:
		if (i == 1): c += 1
		elif i == 0 and c > 0:
			a.append(c)
			c = 0
	if c > 0: a.append(c)
	#print("Before: ", a)
	if len(m) == len(a):
		for i, k in enumerate(a):
			if not m[i] == k: return False
		return True
	return False
	#print(a)
#
# play counts all possible combinations of sequences of #
# give and string of #'s and ?'s
# each ? is alternately a . or a #
# counting each run of #'s for each combination
#
def play(s, x):
	qcount = s.count('?')
	count = 0
	#print("qcount: ", qcount)
	# bi will generat ALL possible bit sequences for 
	# ? mark replacements (0 -> .   1 -> #)
	for bi in range(2**qcount, 2**(qcount+1)):
		dig = 1
		seq = np.zeros(len(s), dtype=int)
		for i, a in enumerate(s):
			if a == '#' : seq[i] = 1
			elif a == '.': seq[i] = 0
			else:  # it is a ?
				#print("dave...", i, ix)
				if dig & bi:
					seq[i] = 1
				dig = dig << 1
		if seqcount(seq, x) : count += 1
	return count


def doline(line, w):
	return sline(line, w)
#	count = 0
#	for i in range(len(line)):
#		if sline(line[i:], w, 0) : count += 1
#	return count


def process(line):
	line = line.strip()
	#print(line)
	w = line.split(' ')
	fields = w[0]
	x = w[1].split(',')
	#print(fields)
	m = []
	for i in x: m.append(int(i))
	return play(fields, m)
	
def process2(line):
	line = line.strip()
	#print(line)
	w = line.split(' ')
	fields = w[0]
	x = w[1].split(',')
	#print(fields)
	m = []
	for i in x: m.append(int(i))
	return doline(fields, m)


def sline(pline, w, li=0, wi=0, sindex=0, rec=False):
	line=pline[li:]
	if rec: print("   ", end="")
	print("sline: ", line, " w[", wi, "] = ", w[wi])
	if wi + 1 == len(w) and line.count('#') == 0:
		sindex += 1
		return 1 + sline(line, w, sindex, wi+1, sindex, True)
	if len(line) == 0: return 0
	c = 0
	i = 0
	while i < len(line) and line[i] == '.': i += 1
	questionmark = line[i] == '?'
	qindex = i
	print("Q found", qindex)
	if i >= len(line): return 0
	for i in range(len(line)):
		if line[i] == '#' or line[i] == '?' : c += 1
		print("i: ", i, " c: ", c, " wi: ", wi)
		if c == w[wi] :
			if wi == len(w) - 1: 
				print("TRUE")
				return 1 + sline(line, w, sindex+1, wi+1, sindex+1, True)
				
			if i < len(line) - 1 and not line[i+1] == '#':
				if questionmark:
					return sline(line, w,      i+2, wi+1, sindex, True) + \
						   sline(line, w, qindex+1, wi+1, sindex, True)
				return     sline(line, w,      i+2, wi+1, sindex, True)

			return sline(line, w, sindex+1, wi+1, sindex+1, True)
			
	return sline(line, w, sindex+1, wi+1, sindex+1, True)

def slinex(line, w, wi, rec=False):
	if rec: print("   ", end="")
	print("sline: ", line, " w[", wi, "] = ", w[wi])
	if wi + 1 == len(w) and line.count('#') == 0:
		return True
	if len(line) == 0: return False
	c = 0
	i = 0
	while i < len(line) and line[i] == '.': i += 1
	if i >= len(line): return False
	for i in range(len(line)):
		if line[i] == '#' or line[i] == '?' : c += 1
		if c == w[wi] :
			if wi == len(w) - 1: 
				#print("TRUE")
				return True
			if i < len(line) - 1 and not line[i+1] == '#':
				return sline(line[i+2:], w, wi+1, True)
			return False

print("Part 1 process: ", process("?###???????? 3,2,1"))
print("Part 2 process: ", process2("?###???????? 3,2,1"))
exit(1)
count = 0
for line in open("test.txt"):
	print(line)
	print("Part 1 process: ", process(line))
	print("Part 2 process: ", process2(line) )
	#count += process(line)
	
print ("Part 1: Number of possible valid arrangements: ", count)
