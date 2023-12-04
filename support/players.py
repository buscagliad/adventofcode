import time

Roster = {}
Roster[3187848] = ["Phil Calora", "philip.calora@vts-i.com"]
Roster[1540194] = ["Matt Binning", "matthew.binning@vts-i.com"]
Roster[1797397] = ["Roxy Jamieson", "roxy.jamieson@vts-i.com"]
Roster[3187770] = ["Dana Kimball", "dana.kimball@vts-i.com"]
Roster[2260695] = ["Josh Gold", "josh.gold@vts-i.com"]
Roster[3207955] = ["Joaquim Pedroza", "joaquim.pedroza@vts-i.com"]
Roster[1856280] = ["John Basrai", "john.basrai@vts-i.com"]
Roster[3193300] = ["Rob Pierson", "rob.pierson@vts-i.com"]
Roster[1528019] = ["David Buscaglia", "david.buscaglia@vts-i.com"]
Roster[2260751] = ["Ash Evans", "ash.evans@vts-i.com"]
Roster[1739534] = ["Jill Thornton", "jill.thornton@vts-i.com"]
Roster[3209547] = ["Davin Jimenez", "davin.jimenez@vts-i.com"]
Roster[2326479] = ["Alexis Johnson", "alexis.johnson@vts-i.com"]
Roster[3188951] = ["Ashley Venn", "ashley.venn@vts-i.com"]
Roster[685392]  = ["Anthony Lee", "anthony.lee@vts-i.com"]
Roster[2256426] = ["Patrick O'Brien", "patrick.obrien@vts-i.com"]
Roster[2511823] = ["Nathan Ferrara", "eric.ferrara@vts-i.com"]
Roster[3184451] = ["Robb Davis", "robb.davis@vts-i.com"]
Roster[551197]  = ["John Moon", "john.moon@vts-i.com"]
Roster[1521453] = ["Eric Ferrara", "eric.ferrara@vts-i.com"]
Roster[1738884] = ["Stephanie Stites", "stephanie.stites@vts-i.com"]
Roster[2327715] = ["Nicholas Henderson", "nicholas.henderson@vts-i.com"]
Roster[2309566] = ["Kevin Matei", "kevin.matei@vts-i.com"]
Roster[1710591] = ["Neil Jacklin", "neil.jacklin@vts-i.com"]
Roster[3198185] = ["Dominick Beaman", "dominick.beaman@vts-i.com"]
Roster[1096925] = ["Macie Matthews", "macie.matthews@vts-i.com"]
Roster[2246495] = ["Sean McCarthy", "sean.mccarthy@vts-i.com"]
Roster[2258724] = ["Mattie Sanz", "mattie.sanz@vts-i.com"]


def getPlayerName(idx):
	global Roster
	if Roster[idx] is None:
		print("ERROR - so such player index: ", idx)
		return "ERROR"
	return Roster[idx][0]

def getPlayerEmail(idx):
	global Roster
	if Roster[idx] is None:
		print("ERROR - so such player index: ", idx)
		return "ERROR"
	return Roster[idx][1]

#
# returns True if p1 is better than p2
# either more stars OR
# last star was earlier
#
def plcomp(p1, p2):
	if p1.numstars == p2.numstars:
		if p1.laststar < p2.laststar:
			return -1
		else:
			return 1
	if p1.numstars > p2.numstars:
		return -1
	else:
		return 1

def pltime(t):
	tm = time.localtime(t)
	stm = time.strftime("%d %b %Y %H:%M:%S", tm)
	return stm

class Player:
	def __init__(self, idx, numstars, laststar):
		self.idx = idx
		self.name = getPlayerName(idx)
		self.laststar = laststar
		self.numstars = numstars
		self.email = getPlayerEmail(idx)
		self.problems = [[0,0]]*26
		self.lastStarDate = 0
		self.lastPuzzle = ""

	def addDay(self, day, p1, p2=0):
		self.problems[day] = [int(p1), int(p2)]
		# print(self.name, " adding day ", day, " times: ", int(p1), int(p2))
		if p1 > self.lastStarDate:
			self.lastStarDate = p1
			self.lastPuzzle = "Day " + str(day) + " Part 1"
		if p2 > self.lastStarDate:
			self.lastStarDate = p2
			self.lastPuzzle = "Day " + str(day) + " Part 2"
	def out(self):
		print("***  ", self.name)
		print()
		tm = time.localtime(self.laststar)
		stm = time.strftime("%d %b %Y %H:%M:%S", tm)
		print(" Number of stars: ", self.numstars, end="")
		if (self.numstars > 0) : print ("      Last Star: ", stm);
		else:  print()
		for d in range(len(self.problems)):
			t1, t2 = self.problems[d]
			if t1 == 0 and t2 == 0: continue
			print("  Day ", d, end = "")
			print("   Part1: ", pltime(t1), end = "")
			if t2 > 0:
				print("    Part2: ", pltime(t2), end = "")
			print()
		print()

	def simpleout(self, n):
		if (n == 0):
			print("    Name                        # Stars  Last Star Achieved")
			return
		tm = time.localtime(self.laststar)
		stm = time.strftime("%d %b %Y %H:%M:%S", tm)
		if (self.numstars == 0) : stm = ""
		print(f'{n:2d}  {self.name:30}  {self.numstars:3d}  {stm}')
