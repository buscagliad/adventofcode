from enum import Enum

# operators are:
# '+', '*', '(', ')', 'V'

class Ops(Enum):
	Open = 1
	Close = 2
	Add = 3
	Mult = 4
	Value = 5

def EqRunX(line, start, end):
	mult = -1
	for s in range(start,end):
		if s == '\n' : return rv
		elif s == ' ': continue
		elif s == '+' :
			mult = 0
		elif s == '*' :
			mult = 1
		elif s == '(' :
			print("  ERROR - ( encountered")
		elif s == ')' :
			print("  ERROR - ) encountered")
		else :
			#print("thisvalue(s=)",s, int(s))
			thisValue = int(s)
			if mult == 1 :
				rv *= thisValue
			elif mult == 0:
				rv += thisValue
			elif mult == -1:
				mult = 2
				rv = thisValue
				print("Starting value is: ", rv)
		return rv

def EqRun(line, rv = 0, start = 0, end=-1):
	if end < 0 : end = len(line)
	#print ("Line: ", line[start:end], "Mult: ", mult, "RV = ", rv, "start = ", start, "end = ", end)
	for j in range(start,end):
		s = line[j]
		if s == '\n' : return rv
		elif s == ' ': continue
		elif s == '+' :
			mult = False
		elif s == '*' :
			mult = True
		elif s == '(' :
			print("EqRun - ERROR, encountered ')'")
			return rv, j
		elif s == ')' :
			#print("EqRun - ERROR, encountered '('")
			return rv, j
		else :
			thisValue = int(s)
			if 'mult' not in locals():
				rv = thisValue
				mult = False
			elif mult :
				rv *= thisValue
			else:
				rv += thisValue
	return rv, len(line)

g_depth = 0

def Equation(line):
	global g_depth
	print ("[",g_depth,"] Line: ", line)
	rv = 0
	for j in range(len(line)):
		s = line[j]
		if not s == ' ' : print("[",g_depth,"] ", s)
		if s == '\n' : return rv, len(line)
		elif s == ' ': continue
		elif s == '+' :
			mult = False
		elif s == '*' :
			mult = True
		elif s == '(' :
			print("[",g_depth,"]   rv:", rv, " mult: ", mult)
			if mult:
				#return rv * Equation(line, mult, j+1)
				#rv *= Equation(line, mult, j+1)
				g_depth += 1
				nrv, dj = Equation(line[j+1:])
				g_depth -= 1
				rv *= nrv
				j += dj+2
				print ("[",g_depth,"] Line: ", line[j:], " * rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)
			else:
				#return rv + Equation(line, mult, j+1)
				#rv += Equation(line, mult, j+1)
				g_depth += 1
				nrv, dj = Equation(line[j+1:])
				g_depth -= 1
				j += dj+2
				rv += nrv
				print ("[",g_depth,"] Line: ", line[j:], " + rv ", rv, " nrv", nrv, " j = ", j, " dj = ", dj)

		elif s == ')' :
			print("[",g_depth,"] ",rv, " line[",j,":] ", line[j:])
			return rv, j
		else :
			#print("thisvalue(s=)",s, int(s))
			thisValue = int(s)
			if 'mult' not in locals():
				rv = thisValue
				print("[",g_depth,"] First value ", thisValue)
			elif mult :
				rv *= thisValue
				#rv = thisValue * Equation(line, False, rv, j + 1)
				#print("* ", rv)
				#return rv
			else:
				rv += thisValue
				#rv = thisValue + Equation(line, True, rv, j + 1)
				#print ("+ ", rv)
				#return rv
	return rv, len(line)

eq = "2 * 3 + (4 * 5)"
eq = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
eq = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) "
eq = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
eq = "1 + (2 * 3) + (4 * (5 + 6))"
#eq = "1 + 2 * 3 + 4 * 5 + 6"

#print("$$$ eqRun: ", eq, " = ", EqRun(eq))
print("$$$ equation: ", eq, " = ", Equation(eq))

#for eq in open("test.txt", "r"):
#	print("$$$ eq: ", eq, " = ", Equation(eq))
