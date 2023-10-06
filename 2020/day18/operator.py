
def insert(line, index, ch):
	#print("insert ", ch, " at ", index)
	rline = line[:index]
	rline += ch
	rline += line[index:]
	return rline


g_depth = 0

def EquationP1(line, debug = False):
	global g_depth
	if (debug) : print ("[",g_depth,"] Line: ", line)
	rv = 0
	j = 0
	while j < len(line) :
		s = line[j]
		j += 1
		if (debug and not s == ' ' ) : print("[",g_depth,"]  lin4[",j,"] = ", s)
		if s == '\n' : return rv, len(line)
		elif s == ' ': continue
		elif s == '+' :
			mult = False
		elif s == '*' :
			mult = True
		elif s == '(' :
			if 'mult' not in locals():
				mult = False
			if (debug) : print("[",g_depth,"]   rv:", rv, " mult: ", mult)
			if mult:
				g_depth += 1
				nrv, dj = EquationP1(line[j:])
				g_depth -= 1
				rv *= nrv
				j += dj
				if (debug) : print ("[",g_depth,"] Line: ", line[j:], " * rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)
			else:
				g_depth += 1
				nrv, dj = EquationP1(line[j:])
				g_depth -= 1
				j += dj
				rv += nrv
				if (debug) : print ("[",g_depth,"] Line: ", line[j:], " + rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)

		elif s == ')' :
			if (debug) : print("[",g_depth,"] ",rv, " line[",j,":] ", line[j:])
			return rv, j
		else :
			thisValue = int(s)
			if 'mult' not in locals():
				rv = thisValue
				if (debug) : print("[",g_depth,"] First value ", thisValue)
			elif mult :
				rv *= thisValue
			else:
				rv += thisValue
	return rv, len(line)


def EquationP2(line, retNext = False, debug = False):
	global g_depth
	if (debug) : print ("[",g_depth,"] Line: ", line)
	rv = 0
	j = 0
	while j < len(line) :
		s = line[j]
		j += 1
		if (debug and not s == ' ' ) : print("[",g_depth,"]  lin4[",j,"] = ", s)
		if s == '\n' : return rv, len(line)
		elif s == ' ': continue
		elif s == '+' :
			g_depth += 1
			nrv, dj = EquationP2(line[j:], True)
			g_depth -= 1
			j += dj
			rv += nrv
			if (debug) : print ("[",g_depth,"] Line: ", line[j:], " + rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)
			mult = False
		elif s == '*' :
			mult = True
		elif s == '(' :
			if 'mult' not in locals():
				mult = False
			if (debug) : print("[",g_depth,"]   rv:", rv, " mult: ", mult)
			if mult:
				g_depth += 1
				nrv, dj = EquationP2(line[j:])
				g_depth -= 1
				rv *= nrv
				j += dj
				if (debug) : print ("[",g_depth,"] Line: ", line[j:], " * rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)
			else:
				g_depth += 1
				nrv, dj = EquationP2(line[j:])
				g_depth -= 1
				j += dj
				rv += nrv
				if (debug) : print ("[",g_depth,"] Line: ", line[j:], " + rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)
				if (retNext) : return rv, j

		elif s == ')' :
			if (debug) : print("[",g_depth,"] ",rv, " line[",j,":] ", line[j:])
			return rv, j
		else :
			thisValue = int(s)
			if 'mult' not in locals():
				rv = thisValue
				if (debug) : print("[",g_depth,"] First value ", thisValue)
			elif mult :
				rv *= thisValue
			else:
				rv += thisValue
	return rv, len(line)
	
def isdigit(s):
	if s < '0' or s > '9' : return False
	return True

def pmatch(line, ix, ch):
	count = 0
	for j in range(ix, -1, -1):
		#print("pmatch j=", j)
		if line[j] == ')' : count += 1
		elif line[j] == '(' : count -= 1
		if (count == 0) : 
			#print("match found at ", j)
			return j
	print("ERROR - no end found")
	return -1

def nmatch(line, ix, ch):
	count = 0
	for j in range(ix,len(line)):
		if line[j] == ')' : count += 1
		elif line[j] == '(' : count -= 1
		if (count == 0) : 
			#print("match found at ", j)
			return j
	print("ERROR - no end found")
	return -1
#((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
#((2 + 4) * 9) * (((6 + 9) * (8 + 6)) + 6) + (2 + 4) * 2
def nextIndex(line, j):
	#print("nextIndex: j: ", j)
	if line[j] == '+':
		if isdigit(line[j+1]) :
			return j+2
		elif line[j+1] == '(' :
			ix = nmatch(line, j+1, ')')
			return ix
		else:
			print ("ERROR (nextIndex) - unexpected character: ", line[j-1], "j-1:", j-1)
	else:
		print ("ERROR (nextIndex) - no + character: ", line[j])
	print("Return nextIndex: ", line)
		
def prevIndex(line, j):
	#print("prevIndex: j: ", j)
	if line[j] == '+':
		if isdigit(line[j-1]) :
			return j-1
		elif line[j-1] == ')' :
			ix = pmatch(line, j-1, '(')
			return ix
		else:
			print ("ERROR (prevIndex) - unexpected character: ", line[j-1], "j-1:", j-1)
	else:
		print ("ERROR (prevIndex) - no + character: ", line[j])

	print("Return prevIndex: ", line)
	return line	

def Eq2(line, debug = False):
	global g_depth
	if (debug) : print ("[",g_depth,"] Line: ", line)

	j = 0
	s = ' '
	while s != '\n' and j < len(line) :
		s = line[j]
		if s == '+' :
			ni = nextIndex(line, j)
			line=insert(line, ni, ')')
			pi = prevIndex(line, j)
			line=insert(line, pi, '(')
			#print("Line: ", line, "   j=",j," pi,ni:", pi, ni)
			j += 1
		j += 1
	return line

def check(line, answer):
	ans,k = EquationP2(line)
	if ans == answer : print (line, " = ", ans, " CORRECT!")
	else: print(line, " = ", ans, "NOT CORRECT - SHOULD BE", answer)
	
def check2(xline, answer):
	#print("check2: ", xline)
	line = xline.replace(" ", "")
	#print("check2: ", line)
	line = Eq2(line)
	ans,k = EquationP1(line)
	if ans == answer : print (line, " = ", ans, " CORRECT!")
	else: print(line, " = ", ans, "NOT CORRECT - SHOULD BE", answer)
	

#nline = insert("dave is cool", 3, 'z')
#print(nline)
#check2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340)
#exit(1)


	
total = 0

for eq in open("data.txt", "r"):
	ans, k = EquationP1(eq)
	total += ans
	#print("$$$ eq: ", eq, " = ", ans)

print("Part 1: sum of all equations is ", total)

total = 0

for eq in open("data.txt", "r"):
	line = eq.replace(" ", "")
	line = Eq2(line)
	ans, k = EquationP1(line)
	total += ans
	#print("$$$ eq: ", eq, " = ", ans)

print("Part 2: sum of all equations is ", total)


#check2("1 + 2 * 3 + 4 * 5 + 6", 231)
#check2("1 + (2 * 3) + (4 * (5 + 6))", 51)
#check2("2 * 3 + (4 * 5)", 46)
#check2("2 * (3 + (4 * 5))", 46)
#check2("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445)
#check2("5 + (8 * ((3 + 9) + 3) * 4 * 3)", 1445)
#check2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060)
#check2("5 * 9 * (7 * 3 * (3 + 9) * (3 + ((8 + 6) * 4)))", 669060)
#check2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340)

#(((2+4)*9)*((6+9)*(8+6))+6)+(2+4)*2  =  22704 NOT CORRECT - SHOULD BE 23340
#       (((2+4))*9)*((((6+9))*((8+6)))+6)+((2+4))*2  =  23340  CORRECT!
#Line:  (((2+4)*9)*((6+9)*(8+6))+6))+2)+4)*(((2    j= 31
