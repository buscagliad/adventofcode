'''
match term:
    case pattern-1:
         action-1
    case pattern-2:
         action-2
    case pattern-3:
         action-3
    case _:
        action-default
'''

class Wire(object):
	def __init__(self, name, op, in1, in2):
		self.name = name
		self.op = op	# for LS or RS, in2 is the shift number
						# if wire is SET, value will be set to int(in1)
		self.in1 = in1	# name of input wire
		self.in2 = in2	# name of input wire OR shift number
		self.value = None	# Value is assigned later
		if op == "SET": 
			self.value = int(in1)

	def out(self, onlyset = False):
		if self.op == "SET":
			print(self.value, " -> ", self.name)
		elif onlyset: 
			return
		elif self.op == "ASS":
			print(self.in1, " -> ", self.name)
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
		if len(words) == 3:
			n = words[0]
			in1 = n
			if n.isnumeric():
				op = "SET"
			else:
				op = "ASS"	# assigned
		elif words[0] == "NOT":
			op = "NOT"
			in1 = words[1]
		elif words[1] == "RSHIFT":
			op = "RSHIFT"
			in1 = words[0]
			in2 = words[2]
		elif words[1] == "LSHIFT":
			op = "LSHIFT"
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
	def out(self, onlyset = False):
		for x in self.connect:
			w = self.connect[x]
			w.out(onlyset)
	def display(self, name):
		x = self.connect[name]
		if x is None:
			print("Invalid connector name: ", name)
		else:
			x.out()
	def set(self, name, value):
		x = self.connect[name]
		if x is None:
			print("Invalid connector name: ", name)
		else:
			x.value = value
			x.op = "SET"
	#
	# finds all instance of 'name' and updates them with the value
	def findValue(self, name, debug=False):
		if name[0].isdigit(): return int(name)
		x = self.connect[name]
		#x.out()
		match x.op:
			case "SET":
				if (debug) : print(name, "SET has value: ", x.value)
				return x.value
			case "ASS":
				x.value = self.findValue(x.in1) & 0x0000FFFF
				if (debug) : print(name, "ASS has value: ", x.value)
				x.op = "SET"
				return x.value
			case "LSHIFT":
				x.value = (self.findValue(x.in1) << int(x.in2)) & 0x0000FFFF
				if (debug) : print(name, "LSHIFT has value: ", x.value)
				x.op = "SET"
				return x.value
			case "RSHIFT":
				x.value = (self.findValue(x.in1) >> int(x.in2)) & 0x0000FFFF
				if (debug) : print(name, "RSHIFT has value: ", x.value)
				x.op = "SET"
				return x.value
			case "AND":
				x.value = (self.findValue(x.in1) & self.findValue(x.in2)) & 0x0000FFFF
				if (debug) : print(name, "AND has value: ", x.value)
				x.op = "SET"
				return x.value
			case "OR":
				x.value = (self.findValue(x.in1) | self.findValue(x.in2)) & 0x0000FFFF
				if (debug) : print(name, "OR has value: ", x.value)
				x.op = "SET"
				return x.value
			case "NOT":
				x.value = (~self.findValue(x.in1)) & 0x0000FFFF
				if (debug) : print(name, "NOT has value: ", x.value)
				x.op = "SET"
				return x.value
			case _:
				print("ERROR with name: ", name)
				exit(1)
		


sym = Symbol()
for line in open("data.txt", "r"):
	sym.add(line)

wire = 'a'
wire_value = sym.findValue(wire)
print("Part 1: wire ", wire, " has value ", wire_value)

sym2 = Symbol()
for line in open("data.txt", "r"):
	sym2.add(line)

sym2.set('b', wire_value)
wire_value = sym2.findValue(wire)
print("Part 2: wire ", wire, " has value ", wire_value)

