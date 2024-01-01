

sides = []
sides2 = []
correction = 0
correction2 = 0

def process(line):
	# L 4 (#135080)
	w = line.strip().split()
	udlr = w[0]
	num = int(w[1])
	return udlr, num

def process2(line):
	# L 4 (#135080)
	w = line.strip().split()
	color = w[2]
	num = int(color[2:7], 16)
	match color[7]:
		case '0': udlr = 'R'
		case '1': udlr = 'D'
		case '2': udlr = 'L'
		case '3': udlr = 'U'
	return udlr, num





def getsides(fname, part2 = False):
	xpos = 0
	ypos = 0
	sides = []
	correction = 0
	down = 0
	up = 0
	left = 0
	right = 0
	for line in open(fname):
		if part2:
			u, n = process2(line)
		else:
			u, n = process(line)
		#n += 1
		#print("UDLR: ", u, "   Num: ", n)
		if u == 'U' : 
			ypos -= n
			up += n
		elif u == 'L' : 
			xpos += n
			left += n
		elif u == 'D' : 
			ypos += n
			down += n
		elif u == 'R' : 
			xpos -= n
			right += n
		s = (xpos, ypos)
		sides.append(s)
		if u == 'R' or u == 'D':
			correction += n
	return sides, correction


def computeArea(s):
	n = len(s)
	plus = 0
	neg = 0

	for i in range(n):
		if i + 1 == n:
			j = 0
		else: 
			j = i + 1
		plus += s[i][0] * s[j][1]
		neg  += s[j][0] * s[i][1]
	
	return int(abs((plus - neg) / 2))
	
sides, scor = getsides('data.txt', False)
sides2, scor2 = getsides('data.txt', True)

print("Part 1: area of dig is: ", computeArea(sides)+scor+1)
print("Part 2: area of dig is: ", computeArea(sides2)+scor2+1)
