
def sumline(line):
	neg = False
	s = 0
	v = 0
	t = 0
	rsum = 0
	for a in line:
		if a.isdigit() :
			s = 10 * s + ord(a) - ord('0')
			t *= 10
		elif a == '-':
			neg = True
		else:
			if s > 0:
				if neg: 
					rsum -= s
					#print ("s =  -", s, "  sum is ", rsum)
				else: 
					rsum += s
					#print ("s =   ", s, "  sum is ", rsum)
			s = 0
			v = 0
			t = 0
			neg = False
	return rsum


def remarray(line):
	sc = 0		# start curly bracket {
	ec = 0		# end curly bracket }
	ss = 0		# start square bracket [
	es = 0		# end square bracket ]
	#print("remarray line length: ", len(line), flush=True)
	for i in range(len(line)):
		a = line[i]
		if a == '[':
			sc = 0
			ss = i
			ec = 0
			es = 0
		elif a == ']':
			es = i + 1		
		elif a == '{':
			#print("{", j)
			sc = i
			ss = 0
			ec = 0
			es = 0
		elif a == '}':  
			ec = i+1
		if sc > 0 and ec > 0:
			nline = line[sc:ec]
			if "red" in nline:
				middle = ""
			else:
				middle = str(sumline(nline))
			#print("{} middle: ", middle)
			xline = ''.join([line[:sc],middle,line[ec:]])
			return remarray(xline)
		elif ss > 0 and es > 0:
			nline = line[ss:es]
			middle = str(sumline(nline))
			#print("[] middle: ", middle)
			xline = ''.join([line[:ss],middle,line[es:]])
			return remarray(xline)
	return line

redsum = 0
total = 0
for line in open("data.txt", "r"):
	total += sumline(line)
	redsum += sumline(remarray(line))

print("Part 1: sum of all numbers is ", total)
print("Part 2: sum of not 'red' ", redsum)

