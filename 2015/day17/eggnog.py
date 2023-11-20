



containers=[]
for line in open("data.txt", "r"):
	containers.append(int(line))

count = 0

def contsum(n):
	global containers
	i = 0
	b = 1
	s = 0
	nc = 0
	for i in range(len(containers)):
		if b & n: 
			s += containers[i]
			nc += 1
		i+=1
		b=b<<1
	return nc, s

numconts=[0]*len(containers)

for n in range(2**len(containers)):
	cc, s = contsum(n)
	if s == 150:
		numconts[cc] += 1
		count += 1

mc = 0
for k in range(len(numconts)):
	if numconts[k] > 0:
		mc = k
		break

print("Part 1: count of possible eggnog containers is: ", count)
print("Part 2: minimum number of containers: ", mc, " possible combos: ", numconts[mc])
