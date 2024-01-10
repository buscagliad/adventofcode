# 12, 31, 28 @ -1, -2, -1


with open('../../util/linalg.py') as f: exec(f.read())

def process(line):
	w = line.strip().split(", ")
	x = w[2].split()
	return int(w[0]), int(w[1]), int(x[0]), int(x[2]), int(w[3]), int(w[4])

hail = []
stones = []
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
	stones.append([ax, ay, az, adx, ady, adz])
	
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
		x, y, tf = intersect(hail[i], hail[j])
		if tf:
			x0 = hail[i][2]
			dx0 = hail[i][3]
			x1 = hail[j][2]
			dx1 = hail[j][3]
			t0 = (x - x0) / dx0
			t1 = (x - x1) / dx1
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
# We know that P(t1) = P + t1 V = p[i] + v[i] * t1
# which is the statement that if P and V are correct, there is a time, t1, where the first 
# hail stone interesects at P(t1).  Solving we get
#            P - p[i] = t1 * (v[i] - V)
#
# This equation implies that the vectors ( P - p[i] )  and  ( v[i] - V ) are parrallel to each other 
# as they are a multiple (t1) of each other.  If two vectors A and B are parallel - then A x B = (0,0,0)
#
# crossing both sides with (v[i] - V) we get:
#
#           (P - p[i]) x (v[i] - V) = (0,0,0)    (1)
#
# 
# Exanding (1) we get:
#
#        P x v[i] - P X V - p[i] x v[i] + p[i] x V = 0   (2)
#
#		 P X V = P x v[i] - p[i] x v[i] + p[i] x V       (3)
#
# selecting j not equal to i, we also have 
#
#        P X V = P x v[j] - p[j] x v[j] + p[j] x V       (4)
#
# equating (3) and (4) vector equations, we get:
#
#		P x v[i] - p[i] x v[i] + p[i] x V = P x v[j] - p[j] x v[j] + p[j] x V   (5)
#
# Note that eqn (5) represents 3 equations with 6 unknowns (Px,Py,Pz) and (Vx, Vy, Vz) 
# We can used any other pair to get another 3 equations (same unkowns) and thus we'll
# have 6 eqns. with 6 unkowns.  Solving (5) for the unkonws yields:
#
#      P x (v[i] - v[j]) +  (p[j] - v[i]) x V = p[i] x v[i] - p[j] x v[j]    (6)
#
# Unknowns are Px, Py, Pz, Vx, Vy, Vz  and p[i] = (pi.x, pi.y, pi.z) and v[i] = (vi.x, vi.y, vi.z)
#
#  d = v[i] - v[j]
#  e = p[j] - v[i]
#  f = p[i] x v[i] - p[j] x v[j]
#
#  g = v[i] - v[l]
#  h = p[l] - v[i]
#  k = p[i] x v[i] - p[l] x v[l]
#
#	P x d = (Pz * d.y - Py * d.z, Pz * d.x - Px * d.z, Px * d.y - Py * d.x)
#
#   e x V = (e.z * Vy - e.y * Vz, e.z * Vx - e.x * Vz, e.x * Vy - e.y * Vx)
#
#  |   0    d.z  -d.y    0   -e.z   e.y  | | P.x |   |  f.x  |
#  | -d.z    0    d.x   e.z    0   -e.x  | | P.y |   |  f.y  |
#  |  d.y  -d.x    0   -e.y   e.x    0   | | P.z |   |  f.z  |
#  |   0    g.z  -g.y    0   -h.z   h.y  | | V.x | = |  k.x  |
#  | -g.z    0    g.x   h.z    0   -h.x  | | V.y |   |  k.y  |
#  |  g.y  -g.x    0   -h.y   h.x    0   | | V.z |   |  k.z  |
#
#
[px,py,pz,vx,vy,vz] = stones[1]
p1 = Vector3(px,py,pz)
v1 = Vector3(vx,vy,vz)
p1.out()
v1.out()

[px,py,pz,vx,vy,vz] = stones[2]
p2 = Vector3(px,py,pz)
v2 = Vector3(vx,vy,vz)
p2.out()
v2.out()


[px,py,pz,vx,vy,vz] = stones[3]
p3 = Vector3(px,py,pz)
v3 = Vector3(vx,vy,vz)
p3.out()
v3.out()

#  d = v[i] - v[j]
#  e = p[j] - v[i]
#  f = p[i] x v[i] - p[j] x v[j]
#
#  g = v[i] - v[l]
#  h = p[l] - v[i]
#  k = p[i] x v[i] - p[l] x v[l]

d = v1.sub(v2)
d.out("d.out(): ")
e = p2.sub(v1)

#  f = p[i] x v[i] - p[j] x v[j]
f1 = p1.cross(v1)
f = f1.sub(p2.cross(v2))


g = v1.sub(v3)
h = p3.sub(v1)

#  f = p[i] x v[i] - p[j] x v[j]
k = f1.sub(p3.cross(v3))


b = np.array((f.x, f.y, f.z, k.x, k.y, k.z)).reshape((6, 1))


m = Matrix(6)

#
#  |   0    d.z  -d.y    0   -e.z   e.y  | | P.x |   |  f.x  |
#  | -d.z    0    d.x   e.z    0   -e.x  | | P.y |   |  f.y  |
#  |  d.y  -d.x    0   -e.y   e.x    0   | | P.z |   |  f.z  |
#  |   0    g.z  -g.y    0   -h.z   h.y  | | V.x | = |  k.x  |
#  | -g.z    0    g.x   h.z    0   -h.x  | | V.y |   |  k.y  |
#  |  g.y  -g.x    0   -h.y   h.x    0   | | V.z |   |  k.z  |
#


m.M[0][0] = 0
m.M[0][1] = d.z
m.M[0][2] = -d.y
m.M[0][3] = 0
m.M[0][4] = -e.z
m.M[0][5] = e.y

m.M[1][0] = -d.z
m.M[1][1] = 0
m.M[1][2] = d.x
m.M[1][3] = e.z
m.M[1][4] = 0
m.M[1][5] = -e.x

m.M[2][0] = d.y
m.M[2][1] = -d.x
m.M[2][2] = 0
m.M[2][3] = -e.y
m.M[2][4] = e.x
m.M[2][5] = 0

#  |   0    g.z  -g.y    0   -h.z   h.y  | | V.x | = |  k.x  |
#  | -g.z    0    g.x   h.z    0   -h.x  | | V.y |   |  k.y  |
#  |  g.y  -g.x    0   -h.y   h.x    0   | | V.z |   |  k.z  |

m.M[3][0] = 0
m.M[3][1] = d.z
m.M[3][2] = -d.y
m.M[3][3] = 0
m.M[3][4] = -f.z
m.M[3][5] = f.y

m.M[4][0] = -d.z
m.M[4][1] = 0
m.M[4][2] = d.x
m.M[4][3] = f.z
m.M[4][4] = 0
m.M[4][5] = -f.x

m.M[5][0] = d.y
m.M[5][1] = -d.x
m.M[5][2] = 0
m.M[5][3] = -f.y
m.M[5][4] = f.x
m.M[5][5] = 0

print(m.M)
mi = np.linalg.inv(m.M)
x = m.solve(b)

print(x)
