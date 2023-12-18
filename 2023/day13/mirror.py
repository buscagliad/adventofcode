
import numpy as np
import copy

def rotarr(arr):
	s = []
	for i in range(len(arr[0])):
		st = ""
		for j in range(len(arr)):
			st = ''.join((st, arr[j][i]))
		s.append(st)
	return s

def getarray(f):
	arr = []
	line = f.readline()
	if line == '':
		return arr
	while len(line) > 3:
		arr.append(line.strip())
		line = f.readline()
	return arr


def check(m, i):
	top = i
	below = i+1
	rv = False
	done = False
	while not done: 
		#print("check:: len(m): ", len(m),  " i: ", i, " top: ",  top, " below: ",  below)
		if not m[top] == m[below] : 
			#print("check returning False: top: ", top, m[top], "  below: ", below, m[below])
			return False
		rv = True
		if top == 0 or below + 1 == len(m): 
			#print("check returning TRUE : top: ", top, m[top], "  below: ", below, m[below])
			return True
		top -= 1
		below += 1
	return False

def reflect(m, oldv):
	for i in range(len(m)-1):
		if (i + 1 == oldv) : continue
		if check(m, i): return i + 1
	return 0

def checkm(h, oldv):
	v = rotarr(h)
	hval = reflect(h, oldv//100)
	vval = reflect(v, oldv)
	#print("Hor: ", hval, "  Ver: ", vval)
	return 100*hval, vval

def pmat(k, sizeonly = False):
	print(" Matrix is ", len(k), " x ", len(k[0]))
	if sizeonly: return
	for kl in k:
		print(kl)


#
# part II
#


def smudge(g, i, j):
	x = copy.deepcopy(g)
	#print(len(g[0]))
	c = g[i][j]
	ng = ""
	if c == '#': c = '.'
	else: c = '#'
	if (j == 0):
		ng = ''.join([c, g[i][j+1:]])
	elif (j + 1) == len(g[0]):
		ng = ''.join([g[i][:j], c])
	else:
		ng = ''.join([g[i][:j], c, g[i][j+1:]])
	x[i] = ng
	return x

def smudger(g, oldv):
	for i in range(len(g)):
		for j in range(len(g[0])):
			x = smudge(g, i, j)
			#print(i, j, x[i][j], g[i][j])
			rh, rv = checkm(x, oldv)
			v = max(rh, rv)
			# if rh == oldv: v = rv
			# elif rv == oldv: v = rh
			#print("Smudger  at ", i, j, "  produces v: ", max(rh, rv), " OLD: ", oldv)
			if not (v == 0) :
				#print("Smudger  at ", i, j, "  produces v: ", v, " OLD: ", oldv)
				return v, i, j
	print("FAILED:: Smudger ", " at ", i, j, "  produces v: ", v, " OLD: ", oldv)
	return 0, -1, -1
	

f = open('data.txt', 'r')

# g = getarray(f)
# pmat(g)
# smudge(g, 3, 3)
# pmat(g)
# exit(1)
p1sum = 0
p2sum = 0
n = 0
matnum = 0
while True:
	g = getarray(f)
	matnum += 1
	if len(g) < 2: break
	h, v = checkm(g, 0)
	oldv = max(v, h)
	if oldv == 0: 
		print("Matrix number: ", matnum, " v: ", v, " h: ", h)
		pmat(g)
		print()
		pmat(rotarr(g))
	# pmat(g, True)
	# print("Value is: ", oldv)
	# print()
	k = max(v, h)
	# #pmat(g)
	p1sum += k
	# n += 1
	v, i, j = smudger(g, k)
	# print(n, " Return from smudger: v: ", v, "  i,j: ", i, j)
	p2sum += v
	
print("Part 1 - sum of mirror reflections is: ", p1sum)
print("Part 2 - sum of smudge fixed mirrors is: ", p2sum)
	

