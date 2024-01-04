# 12, 31, 28 @ -1, -2, -1

def process(line):
	w = line.strip().split(", ")
	x = w[2].split()
	return float(w[0]), float(w[1]), float(x[0]), float(x[2]), float(w[3]), float(w[4])

hail = []
for line in open("data.txt"):
	x,y,z,dx,dy,dz = process(line)
	print(x,y,z,dx,dy,dz)
	hail.append((dy/dx, y-x*(dy/dx), x, dx))
	
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
			if t1 < 0 or t0 <0:
				print(i, " intersects ", j, " in the past")
			else:
				if (XMIN <= x) and (x <= XMAX) and (YMIN <= y) and (y <= YMAX):
					print(i, " intersects ", j, " at ", x, y, " inside test area")
					count += 1
				else:
					print(i,  " intersects ", j, " outside test area")
		else:
			print(i, " is parallel to ", j)
			
		#
		# did intersection happen when t < 0 ?
		#
print("Part 1: there are ", count, " pairs of hailstones that intersect in the future")
