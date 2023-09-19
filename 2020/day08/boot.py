
g_accumulator = 0
g_ptr = 0
g_program = []

def reset() :
	global g_ptr
	global g_accumulator
	global g_program
	for p in g_program : p.times_called = 0
	g_ptr = 0
	g_accumulator = 0
	
class instruction:
	def __init__(self, ins, val, idx) :
		self.instruction = ins
		self.index = idx
		self.value = val
		self.times_called = 0

	def display(self) :
		print ("Instruction at ", self.index, " ", self.instruction, " :: ", self.value)

	def execute(self) : # returns next instruction
		global g_ptr
		global g_accumulator
		global g_program
		self.times_called += 1
		if self.times_called >= 2 :
			return -1
		if self.instruction == "nop" : 
			g_ptr += 1
		elif self.instruction == "acc" :
			g_accumulator += self.value
			g_ptr += 1
		elif self.instruction == "jmp" :
			g_ptr += self.value
			if g_ptr < 0 or g_ptr > len(g_program) :
				print ("ERROR - Program counter: ", g_ptr, " outside limits.");
				exit(1)
		else :
			print ("ERROR - Invalid instruction ", self.instruction, " Exitting.")
			exit(1)
		return g_ptr

	def insup(self) :
		if self.instruction == "jmp" : self.instruction = "nop"
		elif self.instruction == "nop" : self.instruction = "jmp"
		
			
def load(fname) :
	global g_program
	index = 0
	for line in open(fname, 'r'):
		#print("LINE: ", line)
		words = line.split()
		if len(words) < 2: return
		g_program.append(instruction(words[0], int(words[1]), index))
		index += 1
	#for p in g_program :
	#	p.display()

load("data.txt")

def run() :
	done = False
	reset()
	global g_ptr
	global g_program
	global g_accumulator
	g_accumulator = 0
	g_ptr = 0
	while not done:
		#print ("Instruction: " "Program counter: ", g_ptr+1)
		g_ptr = g_program[g_ptr].execute()
		if g_ptr < 0 : return False
		if g_ptr >= len(g_program) : return True

run()
print ("Part 1 - value of accumulator: ", g_accumulator)

done = False
sv_ptr = 0
for ins in g_program :
	ins.insup()
	if run() :
		print ("Part 2 - boot code success - accumulator: ", g_accumulator)
		break
		
	ins.insup()

