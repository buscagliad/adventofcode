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
for line in open("data.txt"):
	ax,ay,az,adx,ady,adz = process(line)
	hail.append((ady/adx, ay-ax*(ady/adx), ax, adx))
	x.append(ax)
	y.append(ay)
	z.append(az)
	dx.append(adx)
	dy.append(ady)
	dz.append(adz)

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
		p1x, p1y, tf = intersect(hail[i], hail[j])
		if tf:
			x0 = hail[i][2]
			dx0 = hail[i][3]
			x1 = hail[j][2]
			dx1 = hail[j][3]
			t0 = (p1x - x0) / dx0
			t1 = (p1x - x1) / dx1
			if t1 < 0 or t0 <0:
				pass
				#print(i, " intersects ", j, " in the past")
			else:
				if (XMIN <= p1x) and (p1x <= XMAX) and (YMIN <= p1y) and (p1y <= YMAX):
					count += 1
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
	#print(a,b,c,d,r)
	#print()
	return a, b, c, d, r

def solve4x4(m, b):
	n = len(m[0])
	a = np.zeros((n,n+1), dtype = np.float128)
	for i in range(n):
		a[i][n] = b[i]
		for j in range(n):
			a[i][j] = m[i][j]
			
	x = np.zeros(n, dtype = np.float128)
# Applying Gauss Elimination
	for i in range(n):
		if a[i][i] == 0.0:
			print(a)
			exit(1)
			
		for j in range(i+1, n):
			ratio = a[j][i]/a[i][i]
			
			for k in range(n+1):
				a[j][k] = a[j][k] - ratio * a[i][k]

	# Back Substitution
	x[n-1] = a[n-1][n]/a[n-1][n-1]

	for i in range(n-2,-1,-1):
		x[i] = a[i][n]
		
		for j in range(i+1,n):
			x[i] = x[i] - a[i][j]*x[j]
		
		x[i] = x[i]/a[i][i]
	return x

# a = np.zeros(4)
# b = np.zeros(4)
# c = np.zeros(4)
# d = np.zeros(4)

def solvehail(x, y, dx, dy):
	i = 0
	m = np.zeros([4,4], dtype=np.float128)
	r = np.zeros(4, dtype=np.float128)
	for (si, sj) in [(0,1), (2,3), (1,2), (3, 4)]:
		a, b, c, d, rhs = compcoeffs(x, y, dx, dy, si, sj)
		m[i][0] = a
		m[i][1] = b
		m[i][2] = c	
		m[i][3] = d

		r[i] = rhs
		i += 1

	#print(m)
	rb = np.array(r, dtype=np.float128)
	#print("rb:", rb)
	#rx = np.linalg.solve(m, rb)
	#print("Solution: x, y, xdot, ydot: ", rx)
	rx = solve4x4(m, rb)
	#print("Solution: x, y, xdot, ydot: ", rx)
	return rx
	
rx = solvehail(x, y, dx, dy)
# print("Solution: x, y, xdot, ydot: ", int(rx[0]), int(rx[1]), int(rx[2]), int(rx[3]), rx)
xsol = int(round(rx[0]))
xdot = int(round(rx[2]))
ysol = int(round(rx[1]))
ydot = int(round(rx[3]))
# rx = solvehail(x, z, dx, dz)
# print("Solution: x, z, xdot, zdot: ", int(rx[0]), int(rx[1]), int(rx[2]), int(rx[3]), rx)

rx = solvehail(z, y, dz, dy)
# print("Solution: z, y, zdot, ydot: ", int(rx[0]), int(rx[1]), int(rx[2]), int(rx[3]), rx)
zsol = int(round(rx[0]))
zdot = int(round(rx[2]))

# print("Part 2: the x,y,z coordinates of the thrown stone at t=0", xsol, ysol, zsol)
# print("Part 2: the x,y,z velocities of the thrown stone at t=0", xdot, ydot, zdot)
# print("Part 2: sum of the x,y,z coordinates of the thrown stone at t=0", int(xsol), int(ysol), int(zsol))

print("Part 2: sum of the x,y,z coordinates of the thrown stone at t=0", int(xsol) + int(ysol) + int(zsol))

# NOTE: 722976491652739 is too low
#       722976491652737
#       722976491652740
# rounding error is getting us
# the velocity is being computed 'perfectly': -125, 25, 272
# we will see what time t1 is such that this velocity yiels a point 'close' to xsol, ysol, zsol
#
#tx = ( x[10] - xsol )  / ( xdot - dx[10])
#print(tx)
#ty = ( y[10] - ysol )  / ( ydot - dy[10])
#print(ty)
#tz = ( z[10] - zsol )  / ( zdot - dz[10])
#print(tz)

#print(tx, ty, tz)
