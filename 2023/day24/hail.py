# 12, 31, 28 @ -1, -2, -1

import numpy as np
import random

def cross(a, b):
	
	x = a[1] * b[2] - a[2] * b[1]
	y = a[0] * b[2] - a[2] * b[0]
	z = a[0] * b[1] - a[1] * b[0]
	return np.array((x, -y, z))
		
def process(line):
	w = line.strip().split(", ")
	x = w[2].split()
	return int(w[0]), int(w[1]), int(x[0]), int(x[2]), int(w[3]), int(w[4])

hail = []
x = []
y = []
z = []
dx = []
dy = []
dz = []
for line in open("test.txt"):
	ax,ay,az,adx,ady,adz = process(line)
	hail.append((ady/adx, ay-ax*(ady/adx), ax, adx))
	x.append(ax)
	y.append(ay)
	z.append(az)
	dx.append(adx)
	dy.append(ady)
	dz.append(adz)
	
print("x: ", min(x), " - ", max(x), "  dx: ", min(dx), " - ", max(dx))
print("y: ", min(y), " - ", max(y), "  dy: ", min(dy), " - ", max(dy))
print("z: ", min(z), " - ", max(z), "  dz: ", min(dz), " - ", max(dz))

if 1 in dx:
	print("x has a 0 velocity")
if 1 in dy:
	print("y has a 0 velocity")
if 1 in dz:
	print("z has a 0 velocity")

def intersect(h, l):
	b1 = h[1]
	m1 = h[0]
	b2 = l[1]
	m2 = l[0]
	if abs(m2 - m1) < 0.0001:
		return 0, 0, False
	x = (b1 - b2) / (m2 - m1)
	y = m1 * x + b1
	return x, y, True

XMAX = 400000000000000
YMAX = 400000000000000
XMIN = 200000000000000
YMIN = 200000000000000

def is_whole(f, eps):
	return abs(f - round(f)) < abs(eps)

count = 0
for i in range(len(hail)-1):
	for j in range(i+1, len(hail)):
		gx, gy, tf = intersect(hail[i], hail[j])
		if tf:
			x0 = hail[i][2]
			dx0 = hail[i][3]
			x1 = hail[j][2]
			dx1 = hail[j][3]
			t0 = (gx - x0) / dx0
			t1 = (gx - x1) / dx1
			#
			# did intersection happen when t < 0 ?
			#
			if t0 > 0 and t1 > 0 and is_whole(t0, 0.0001) and is_whole(t1, 0.0001):
				print(i, " intersects ", j, " at time ", t0, t1)
				t = int(t0)

			
print("Part 1: there are ", count, " pairs of hailstones that intersect in the future")

#
# Let P and V be 3-vectors such that, P is the position of the rock thrown at time t=0,
# and V is the velocity vector:  therefore the rock is at P(t) = P + tV
# P = (x,y,z) V = (dx,dy,dz).   The hail that is falling is given by:
# p[i] with velocity v[i]  ( p[i] = (xi,yi,zi) and v[i] = (dxi,dyi,dzi) )
#
# We know that there is a time, t1, where the hailstone is hit by the rock, so all three equations 
# would hold:
#         Px + t1 Vx = pi.x + vi.x * t1
#         Py + t1 Vy = pi.y + vi.y * t1
#         Pz + t1 Vz = pi.z + vi.z * t1
#
# Solving for t1, yields the following:
#
#               pi.x - Px     pi.y - Py     pi.y - Py
#         t1 = ----------- = ----------- = -----------
#               Vx - vi.x     Vy - vi.y     Vz - vi.z
#
# Cross multiplying the equations for x and y yields:
#
#   pi.x * Vy - pi.x * vi.y - Px * Vy + Px * vi.y = Vx * pi.y - Vx * Py - vi.x * pi.y + vi.x * Py
#
# Arranging the nonliner terms on the LHS yields:
#
#   Px * Vy - Vx * Py = pi.x * Vy - pi.x * vi.y  + Px * vi.y - Vx * pi.y + vi.x * pi.y - vi.x * Py
#
# The LHS is a constant (albeit unknown), but holds for all i
#
# We can now equate vectors for i and j which yields:
#
#      pi.x * Vy - pi.x * vi.y  + Px * vi.y - Vx * pi.y + vi.x * pi.y - vi.x * Py = 
#                  pj.x * Vy - pj.x * vj.y  + Px * vj.y - Vx * pj.y + vj.x * pj.y - vj.x * Py
#
# Grouping like terms:
#
#      Px(vi.y - vj.y) + Py(vj.x - vi.x) + Vx(pj.y - pi.y) + Vy(pi.x - pj.x) =
#				 pi.x * vi.y - vi.x * pi.y - pj.x * vj.y  + vj.x * pj.y                (1)
#
# This gives 1 equation in the unkowns Px, Py, Vx, and Vy.  Selecting four unique pairs, i, j
# will yield four equations.  (Obviously this problem is over-subscribed, but is constructed so
# that all hailstones can be intersected as described in the problem).
#
# We will reducte (1) to:
#
#      a Px + b Py + c Vx + d Vy = r
#
#	NOTE: becuase of symmetry - x, y can be replaced with x, z or y, z
#
#   a, b, c, d, r = compcoeffs(x, y, dx, dy, i, j)
#

def compcoeffs(x, y, dx, dy, i, j):
	a = dy[j] - dy[i]
	b = dx[i] - dx[j]
	c =  y[i] -  y[j]
	d =  x[j] -  x[i]
	
	r = dx[i] * y[i] - x[i] * dy[i] -  dx[j] * y[j]  + x[j] * dy[j]
	
	#print(x, y, dx, dy, i, j)
	#print(x[i] * dy[i], dx[i] * y[i],  x[j] * dy[j], dx[j] * y[j])
	print(a,b,c,d,r)
	#print()
	return a, b, c, d, r
	
m = np.zeros([4,4])

a = np.zeros(4)
b = np.zeros(4)
c = np.zeros(4)
d = np.zeros(4)
r = np.zeros(4)

i = 0
for (si, sj) in [(0,1), (0,2), (1,2), (3, 4)]:
	a, b, c, d, rhs = compcoeffs(x, y, dx, dy, si, sj)
	m[i][0] = a
	m[i][1] = b
	m[i][2] = c	
	m[i][3] = d

	r[i] = rhs
	i += 1

rb = np.array(r) #.reshape((4, 1))
print("rb:", rb)
soln = np.array((24,13,-3,1)).reshape((4, 1))


yy = np.matmul(m, soln)
print("M * soln: ", yy)

xx = np.linalg.solve(m, rb)
print("x soln.: ", xx)

print("M*x: ", np.matmul(m, xx))
print("M*soln: ", np.matmul(m, soln))

def test():
	print("Top of test()")
	v = np.array([3, -3, 1])
	print("v.out()", v)
	v2 = np.array([4, 9, 2])
	print("v2.out()", v2)
	v3 = cross(v, v2)
	print("v3.out()", v3)
	print("v3.dot(v2): ", v3.dot(v2))
	print("v3.dot(v): ", v3.dot(v))
	m = np.zeros((6,6))
	for i in range(6):
		for j in range(6):
			m[i][j] = random.random()
	
	print("Matrix M", m)
	MI = np.linalg.inv(m)
	print("Matrix M inverse", MI)
	mm = np.matmul(MI, m)
	print("Matrix M inverse * M (should be I)", mm)
	
	A = np.array([[1, 9, 2, 1, 1],
				 [10, 1, 2, 1, 1],
				 [1, 0, 5, 1, 1],
				 [2, 1, 1, 2, 9],
				 [2, 1, 2, 13, 2]])
	b = np.array([170, 180, 140, 180, 350]).reshape((5, 1))
	x = np.linalg.solve(A, b)
	print(x)
	
	M = np.zeros((5,5))
	for i in range(5):
		for j in range(5):
			M[i][j] = A[i][j]
	x = np.linalg.solve(A, b)
	print(x)
	
test()
