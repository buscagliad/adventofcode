door = 6929599
card = 2448427

div = 20201227
subnum = 7
doorloop = 0
cardloop = 0
rem = 1
loop_count = 0

def crem(v):
	global div
	global subnum
	val = v * subnum
	n = (val) % div
	return n

'''
rem = 1
for r in range(100):
	print("rem is: ", rem)
	rem = crem(rem)
	
exit(1)
'''

while doorloop == 0 or cardloop == 0:
	loop_count += 1
	rem = crem(rem)
	if doorloop == 0 and rem == door:
		doorloop = loop_count
	if cardloop == 0 and rem == card:
		cardloop = loop_count

print("Door loop is: ", doorloop)
print("Card loop is: ", cardloop)

rem = 1
subnum = card
for i in range(doorloop):
	rem = crem(rem)
print("Door loop produces crypto: ", rem)

rem = 1
subnum = door
for i in range(cardloop):
	rem = crem(rem)
print("Card loop produces crypto: ", rem)

	
