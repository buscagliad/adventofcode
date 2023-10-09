import re

class Rule:
	def __init__(self, line):
		#line = line.split(':')
		index, nothing, rule = line.partition(': ')
		#print(index, rule)
		##	
		## rules[0] is list of indeces for this rule
		## rules[1] is list of indeces for this rule
		##
		## rules[self.numRules - 1] is list of indeces for this rule
		self.id = int(index)
		self.rule = rule.strip('"\n')
		if self.rule == "a":
			self.rule == 'a'
		if self.rule == "b":
			self.rule == 'b'
				
	def display(self):
		print("ID: ", self.id, "  Rule : [", self.rule, "]")


def getrule(rules, id):
	for r in rules:
		if r.id == id: return r
	return None

def regexp(rules, rz):
	rexp = ""
	if rules[rz].rule == "a" : 
		return 'a'
	if rules[rz].rule == "b" : 
		return 'b'
	
		
	for c in rules[rz].rule.split():
		if c == '|' :
			rexp += ")|("
		else:
			n = int(c)
			rexp += "(" + regexp(rules, n) + ")"
	return "(" + rexp + ")"

	

rulesDone = False
lineno = 0
messages = []
rules = {}
zeroindex = 0

filename = "data.txt"
for line in open(filename):
	lineno += 1
	if len(line) < 3: 
		rulesDone = True
		continue
	if not rulesDone:
		nr = Rule(line)
		if nr.id == 0: zeroindex = lineno - 1
		rules[nr.id] = nr
	else:
		messages.append((lineno, line[:len(line)-1]))

count = 0


regx = regexp(rules, 0)+"$"

##
## part 1 testing loop
##

test = re.compile(regx)
for m in messages:
	#print(m, test.match(m[1]))
	if not test.match(m[1]) == None:
		count += 1
print ("Part 1: (file: ",filename, ")  Number of good messages: ", count)


##
## part 2 testing loop
##
## 8: 42 | 42 8
## 11: 42 31 | 42 11 31

## Note: if coming into a rule 8, it can repeat rule 42 as many times as it wants
##       if coming into rule 11, 42 can be repeated many times, but must end in rule 31
##       NOTE also, that 0: 8 11, so we complete the matching patterns with just these two 
##       new rules.  So, we will get rules 42 and 31, and thus:
##       0: (42 | 42 8) (42 31 | 42 11 31)
##
##       So, we can start with as many 42's as we'd like, we will end in 31's   AND
##       the number of 42's > number of 31's (and number of 31's > 0)
##
test = re.compile(regx)
reg42 = regexp(rules, 42) ## has to match at start of the string
reg31 = regexp(rules, 31)
rule42 = re.compile(reg42)
rule31 = re.compile(reg31)
count = 0

for m in messages:
	r42count = 0
	r31count = 0

	done = False
	midx = 0
	mlen = 0
	do42 = True  # changes to False when rule 42 is over
	while not done:
		# if we have gone thru the entire message (now empty) we only
		# need to check that we have more r42's that r31's  == AND ==
		# that there is at least 1 r31
		if (m[1][midx:] == "") :
			if (r42count > r31count) and (r31count > 0) :
				count += 1
			done = True
			
			continue
		if do42:
			minfo = rule42.match(m[1], midx)
			if not minfo:
				do42 = False
			else:
				if minfo.span(0)[0] == midx and minfo.span(0)[1] > 0:
					midx = minfo.span(0)[1]
					mlen = minfo.span(0)[1]
					r42count += 1
					continue
				else:
					do42 = False
		if not do42:
			minfo = rule31.match(m[1], midx)
			if not minfo:
				done = True
				continue
			else:
				if minfo.span(0)[0] == midx and minfo.span(0)[1] > 0:
					midx = minfo.span(0)[1]
					mlen = minfo.span(0)[1]
					r31count += 1
					continue
				else:
					done = True
	
print ("Part 2: (file: ",filename, ")  Number of good messages: ", count)
