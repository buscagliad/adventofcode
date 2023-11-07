

	
class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

	def __repr__(self):
		return self.data

class LinkedList:
	def __init__(self, n):
		self.head = {i: Node(i) for i in range(1,n+1)}
		self.size = n
		self.index = {}
	
	def __iter__(self):
		node = self.head
		while node is not None:
			yield node
			node = node.next
	
	def display(self):
		node = self.head
		n = node.next
		#while not n == node:
		for i in range(self.size):
			print(n.data, sep="", end="")
			n = n.next
		print("")

	def find(self, value):
		if False: print("find .. Searching for ", value)
		return self.index[value]



class Cups:
	def __init__(self, numstring, maxlen=9):
		self.debug = False
		self.cups = {i: Node(i) for i in range(1,maxlen+1)}
		self.hold = [0] * 3
		self.cut = None  # this is the list of three cups to move
		self.current_cup = None
		self.size = maxlen
		self.movenum = 0
		last = None
		for i in range(1, maxlen):
			self.cups[i].next = self.cups[i+1]
		first = []
		for i in numstring:
			first.append(int(i))
		#print(len(numstring))
		for i in range(len(numstring)):
			self.cups[first[i]].next = self.cups[first[(i+1) % len(numstring)]]
			if self.debug: print("Cup ", self.cups[first[i]].data, " -> ", self.cups[first[(i+1) % len(numstring)]].data)
			
		#
		# point last in numstring to either first element (if maxlen == 9)
		# or to 'next' element
		if maxlen <= 9:
			if self.debug: print("Mapping ", self.cups[first[maxlen-1]].data, " to ", self.cups[first[0]].data)
			self.cups[first[maxlen-1]].next = self.cups[first[0]]
		else:
			if self.debug: print("Mapping ", self.cups[maxlen].data, " to ", self.cups[first[0]].data)
			self.cups[first[len(numstring)-1]].next = self.cups[10]
			#
			# wrap the cups around - last points to first
			self.cups[maxlen].next = self.cups[first[0]]
		#
		# current cup points to first element in string
		self.current_cup = self.cups[first[0]]
		if self.debug: print("size", self.size)
		if self.debug: print("Current cup is: ", self.current_cup.data)

	def dest(self):
		label = self.current_cup.data - 1
		if label == 0 : label = self.size 
		self.destination = label
		if self.debug: print("dest label: ", self.destination)
		if self.debug: print("dest .. hold: ", self.hold)
		## make sure destination is NOT one of the removed cups
		while self.destination in self.hold:
			if self.debug: print("dest .. self.destination", self.destination, " in hold")
			self.destination -= 1
			if self.destination == 0: self.destination = self.size

	def pickup(self):
		cc = self.current_cup
		h = cc.next
		self.cut = h
		if self.debug: print("pickup cc ", cc.data, "  next: ", h.data)
		g = h
		for n in range(3):
			self.hold[n] = g.data
			if self.debug: print(n, " g.data: ", g.data)
			g = g.next
		cc.next = g
		if self.debug: 
			print("After pickup: ", end = "")
			self.show(self.cups[1], 20)
		
		return h
		
	def show(self, x, n):
		for i in range(n):
			print(i, " show ", x.data)
			x = x.next
	
	def append(self):
		d = self.cups[self.destination]
		if self.debug: print("destination: ", self.destination, " append after ", d.data)
		s = d.next
		if self.debug: print("append next ", s.data)
		if self.debug: print(d.data, " points to ", self.cut.data)
		d.next = self.cut
		self.cut.next.next.next = s
		
	def display(self):
		print("cups: ", end="")
		n = self.cups[1]
		c = 0
		while c < self.size:
			if n.data == self.current_cup.data:
				print("(", n.data, ") ", sep="", end="")
			else:
				print(n.data, " ", end="")
			n = n.next
			c += 1
		print("")

	def move(self, status = False):
		if status: print(" ")
		self.movenum += 1
		if status: print("-- move: ", self.movenum)
		if status: self.display()
		self.pickup()
		if status: print("Pickup: ", self.hold)
		self.dest()
		if status: print("destination: ", self.destination)
		self.append()
		
		# select new current cup
		self.setcc()
		
	def setcc(self):
		self.current_cup = self.current_cup.next
		
	def sstate(self):
		x = self.cups[1]
		f1 = x.next.data
		f2 = x.next.next.data
		print("Next number after 1: ", f1)
		print("Next number after that: ", f2)
		return f1 * f2
		
	def state(self):
		num = 0
		x = self.cups[1]
		x = x.next
		for n in range(self.size-1):
			num = 10 * num + x.data
			x = x.next
		return num

cup_string="389125467"
cup_string="925176834"

x = Cups(cup_string)

m = 0
num_moves = 100
for n in range(num_moves):
	m +=1
	x.move()

print ("Part 1 After ", m, "moves, state is ", x.state())


y = Cups(cup_string, 1000000)
num_moves = 10000000
m = 0
#y.show(y.cups[999999], 20)
#exit(1)
p = 0
for n in range(num_moves):
	m +=1
	y.move(False)

print ("Part 2 After ", m, "moves, state is ", y.sstate())
