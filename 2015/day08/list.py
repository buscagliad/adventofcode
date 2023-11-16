
def cline(line):
	line = line.strip()
	total = len(line)
	suptotal = total
	mem = 0
	ignore = 0
	slash = False
	for c in line:
		if slash:
			if c == 'x': 
				ignore = 2
				suptotal += 1
			elif c == '\\':
				suptotal += 1
			mem += 1
			slash = False
		elif ignore > 0:
			ignore -= 1
		elif c == '\\':
			slash = True
			suptotal += 1
		else:
			mem += 1
	return suptotal+4, total, mem-2

suptotal = 0
total = 0
mem = 0
for line in open("test.txt", "r"):
	s, t, m = cline(line)
	print(line, "S: ", s, " T: ", t, " M: ", m)
	total += t
	mem += m
	suptotal += s

print("Part1: Total is ", total, "  Mem is ", mem, "  Diff is ", total - mem)
	
print("Part2: Sup Total is ", suptotal, "Total is ", total,  
			" Diff is ", suptotal - total)
