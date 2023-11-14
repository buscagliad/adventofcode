
import numpy as np

def paperneed(l, w, h):
	s = np.array([l*w, l*h, h*w])
	s2 = np.sum(s)
	return 2 * s2 + min(s)

def ribbonneed(l, w, h):
	ds = [2*(l+h), 2*(l+w), 2 *(w+h)]
	return min(ds) + l*w*h

def pn_line(line):
	ls = line.split('x')
	l = int(ls[0])
	w = int(ls[1])
	h = int(ls[2])
	return paperneed(l, w, h), ribbonneed(l, w, h)


pn = 0
rn = 0
for line in open("data.txt", "r"):
	thispn, thisrn = pn_line(line)
	pn += thispn
	rn += thisrn

print("Part1:: Total paper need is ", pn)
print("Part2:: Total ribbon need is ", rn)

