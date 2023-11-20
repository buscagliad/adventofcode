import itertools

class Person:
	def __init__(self, name):
		self.name=name
		self.next={}
	def add(self, name, val):
		self.next[name] = val
	def value(self, nname):
		return self.next[nname]
	def out(self):
		for k, v in self.next.items():
			print(self.name, " next to ", k, " ", v)

Happy={}
People=[]

def pline(line):
	w = line.split()
	name = w[0]
	val = int(w[3])
	if w[2]=="lose" : val = -val
	nname = w[10][:len(w[10])-1]
	return name, nname, val

def out(P):
	for p in P:
		P[p].out()
	
#Bob would gain 83 happiness units by sitting next to Alice.
#Bob would lose 7 happiness units by sitting next to Carol.

for line in open("data.txt", "r"):
	n, nn, v = pline(line)
	#print(n, nn, v)
	if not n in People:
		Happy[n] = Person(n)
		People.append(n)
	Happy[n].add(nn, v)



def seatvalue(H, p):
	value = 0
	for i in range(len(p)):
		left = p[(i + 1) % len(p)]
		right = p[(i - 1) % len(p)]
		value += H[p[i]].value(left)
		value += H[p[i]].value(right)
	return value
	
maxhappiness = 0
maxhaparrange = []

for p in itertools.permutations(People):
	sv = seatvalue(Happy, p)
	if sv > maxhappiness:
		maxhaparrange = p
		maxhappiness = sv

print("Part1: Seating arrangement: ", maxhaparrange, "  happiness is ", maxhappiness)

##
# Part 2
##

Happy["Me"] = Person("Me")
People.append("Me")
for p in People:
	Happy["Me"].add(p, 0)
	Happy[p].add("Me", 0)

maxhappiness = 0
maxhaparrange = []

for p in itertools.permutations(People):
	sv = seatvalue(Happy, p)
	if sv > maxhappiness:
		maxhaparrange = p
		maxhappiness = sv

print("Part2: Seating arrangement: ", maxhaparrange, "  happiness is ", maxhappiness)
