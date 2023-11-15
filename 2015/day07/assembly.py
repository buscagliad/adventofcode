

class Wire(object):
	def __init__(self, name, op, in1, in2):
		self.name = name
		self.op = op	# for LS or RS, in2 is the shift number
						# if wire is SET, value will be set to int(in1)
		self.in1 = in1	# name of input wire
		self.in2 = in2	# name of input wire OR shift number
		self.value = None	# Value is assigned later
		if op == "SET": self.value = int(in1)

	def out(self):
		if self.op == "SET":
			print(self.value, " -> ", self.name)
		elif self.op == "NOT":
			print("NOT", self.in1, " -> ", self.name)
		else:
			print(self.in1, self.op, self.in2, " -> ", self.name)

class Symbol:
	def __init__(self):
		self.connect = {}

	def add(self, line):
		words = line.split()
		name = words[len(words)-1]
		in1 = ""
		in2 = ""
		op = ""
		if words[0] == "NOT":
			op = "NOT"
			in1 = words[1]
		elif words[1] == "RSHIFT":
			op = "RS"
			in1 = words[0]
			in2 = words[2]
		elif words[1] == "LSHIFT":
			op = "LS"
			in1 = words[0]
			in2 = words[2]
		elif words[1] == "AND":
			op = "AND"
			in1 = words[0]
			in2 = words[2]
		elif words[1] == "OR":
			op = "OR"
			in1 = words[0]
			in2 = words[2]
		self.connect[name] = Wire(name, op, in1, in2)
	def out(self):
		for x in self.connect:
			w = self.connect[x]
			w.out()

sym = Symbol()
for line in open("data.txt", "r"):
	sym.add(line)

sym.out()
print("Number of entries: ", len(sym.connect))
