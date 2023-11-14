import numpy as np

lights = np.zeros((1000,1000), dtype=np.bool_)

def count():
	global lights
	on = 0
	for i in range(1000):
		for j in range(1000):
			if lights[i][j]: on += 1
	return on

def toggle(ul, br):
	global lights
	for i in range(ul[0], ul[1]+1):
		for j in range(br[0], br[1]+1):
			lights[i][j] = not lights[i][j]

def turnon(ul, br):
	global lights
	for i in range(ul[0], ul[1]+1):
		for j in range(br[0], br[1]+1):
			lights[i][j] = True

def turnoff(ul, br):
	global lights
	for i in range(ul[0], ul[1]+1):
		for j in range(br[0], br[1]+1):
			lights[i][j] = False
'''
turn off 199,133 through 461,193
toggle 322,558 through 977,958
turn on 226,196 through 599,390
'''
def do_line(line):
	if line[0:5] == "turn"

toggle([5,10], [9, 100])

print("Part 1: there are ", count(), "lights on")
