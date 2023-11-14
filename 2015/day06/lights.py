import numpy as np
import re

lights = np.zeros((1000,1000), dtype=np.int32)
lightsp2 = np.zeros((1000,1000), dtype=np.int32)

def count():
	global lights
	on = 0
	for i in range(1000):
		for j in range(1000):
			if lights[i][j]: on += 1
	return on

def toggle(ul, br):
	global lights
	#print("Toggling: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			lights[i][j] = not lights[i][j]

def turnon(ul, br):
	global lights
	#print("Turning on: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			lights[i][j] = True


def turnoff(ul, br):
	global lights
	#print("Turning off: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			lights[i][j] = False
			
def p2count():
	global lightsp2
	on = 0
	for i in range(1000):
		for j in range(1000):
			on += lightsp2[i][j]
	return on

def p2toggle(ul, br):
	global lightsp2
	#print("Toggling: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			lightsp2[i][j] += 2

def p2turnon(ul, br):
	global lightsp2
	#print("Turning on: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			lightsp2[i][j] += 1


def p2turnoff(ul, br):
	global lightsp2
	#print("Turning off: ", ul, " thru ", br)
	for i in range(ul[0], br[0]+1):
		for j in range(ul[1], br[1]+1):
			if lightsp2[i][j] > 0: lightsp2[i][j] -= 1


'''
turn off 199,133 through 461,193
toggle 322,558 through 977,958
turn on 226,196 through 599,390
'''
def do_line(line):
	t = 0
	if line[0:8] == "turn off":
		mode = 0
		t = 9
	elif line[0:7] == "turn on":
		mode = 1
		t = 8
	elif line[0:6] == "toggle":
		mode = 2
		t = 7
	else:
		print("ERROR")
	words = re.split(',| |\n', line[t:])
	#print(words)
	ul = [int(words[0]), int(words[1])]
	lr = [int(words[3]), int(words[4])]
	if mode == 0:
		turnoff(ul, lr)
		p2turnoff(ul, lr)
	elif mode == 1:
		turnon(ul, lr)
		p2turnon(ul, lr)
	else:
		toggle(ul, lr)
		p2toggle(ul, lr)

for line in open("data.txt", "r"):
	do_line(line)
	

print("Part 1: there are ", count(), "lights on")
print("Part 2: there is a brightness of ", p2count())
