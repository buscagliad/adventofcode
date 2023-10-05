

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
	
def Eq2(line, debug = False):
	global g_depth
	if (debug) : print ("[",g_depth,"] Line: ", line)
	rv = 0
	j = 0
	rline = ""
	while j < len(line) :
		s = line[j]
		j += 1
	
total = 0

for eq in open("data.txt", "r"):
	ans, k = EquationP1(eq)
	total += ans
	#print("$$$ eq: ", eq, " = ", ans)

print("Part 1: sum of all equations is ", total)

eq = "1 + 2 * 3 + 4 * 5 + 6"
#eq = "((1 + 2)) * (3 + 4) * (5 + 6)"
#eq = Eq2(eq)
#ans, k = EquationP1(eq)
#print("$$$ eq: ", eq, " = ", ans)

eq = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
eq = "5 * 9 * (7 * 3 * (3 + 9) * ( 3 + ( (8 + 6) * 4) ) ) "
ans, k = EquationP1(eq)
print("$$$ eq: ", eq, " = ", ans)

