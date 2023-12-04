import copy


# Hit Points: 55
# Damage: 8

minmana = 100000000

# tuple:     [cost, damage, armor, heals, cycles, addMana,    xxx, name]
#                0       1      2      3       4        5       6  7
MagicMissle = [ 53,      4,     0,     0,      1,       0,   True, "MagicMissle"]
Drain       = [ 73,      2,     0,     2,      1,       0,   True, "Drain"]
Shield      = [113,      0,     7,     0,      6,       0,  False, "Shield"]
Poison      = [173,      3,     0,     0,      6,       0,   True, "Poison"]
Recharge    = [229,      0,     0,     0,      5,     101,   True, "Recharge"]
Spells = [MagicMissle, Drain, Shield, Poison, Recharge]
MAGICMISSILE=0
DRAIN=1
SHIELD=2
POISON=3
RECHARGE=4


class Players:
	def __init__(self):
		self.gameover = False
		self.mewins = False
		self.bossdamage = 8
		self.bossarmor = 0
		self.bosshits = 55
		self.medamage = 0
		self.mearmor = 0
		self.mehits = 50
		self.debug = False
		self.mana = 500
		self.timers = [0,0,0,0,0]
		self.spend = 0
		self.debug = False
		##
		## test case 1
		##self.bosshits = 13
		##self.bossdamage = 8
		##self.mehits = 10
		##self.mana = 250
		##
		## test case 2
		##self.bosshits = 14
		##self.bossdamage = 8
		##self.mehits = 10
		##self.mana = 250
		
# tuple:     [cost, damage, armor, heals, cycles, addMana,    xxx, name]
#                0       1      2      3       4        5       6  7
	def applyspells(self):
		global Spells
		self.mearmor = 0  ## need to reset
		for t in range(len(self.timers)):
			if (self.timers[t] == 0) : continue
			self.timers[t] -= 1
			spell = Spells[t]
			if t == 2: # SHIELD:		# 2
				self.mearmor = spell[2]
			elif t == 3: # POISON:		# 3
				self.bosshits -= spell[1]
			elif t == 4: # RECHARGE:		# 4	
				self.mana += spell[5]
		return True

# tuple:     [cost, damage, armor, heals, cycles, addMana,    xxx, name]
#                0       1      2      3       4        5       6  7
	def addspell(self, index):
		global Spells
		spell = Spells[index]
		if self.mana < spell[0]: 
			self.gameover = True
			self.mewins = False
			return False
		if self.timers[index] > 0: return False
		if index == 0:
			self.bosshits -= spell[1]
		elif index == 1:
			self.bosshits -= spell[1]
			self.mehits += spell[3]
		elif index == 2: # SHIELD:		# 2
			self.mearmor = spell[2]
			self.timers[index] = spell[4]
		elif index == 3: # POISON
			self.timers[index] = spell[4]
		elif index == 4: # Recharge
			self.timers[index] = spell[4]
		if (self.debug) : print("Player casts ", spell[7], "using ", spell[0], " mana changing mana from ", self.mana, " to ", end = "")
		self.mana -= spell[0]
		self.spend += spell[0]
		if (self.debug) : print(self.mana)
		return True
		

	def bossout(self):
		print("Boss:: damage: ", self.bossdamage, " hits: ", self.bosshits)
		print("")
	def meout(self):
		print("Timers: ", self.timers)
		print("Me::  ", self.mehits, " hit points, ", self.mearmor," armor, ",
			self.mana, " mana", sep="" )
	def out(self):
		self.meout()
		self.bossout()

	def spellok(self, spell):
		return self.timers[spell] == 0

	def playme(self, spell):
		self.applyspells()
		if (self.debug) : print("-- Player turn --")
		if (self.debug) : print("- Player has ", self.mehits, " hit points, ", self.mearmor," armor, ",
			self.mana, " mana", sep="" )
		if (self.debug) : print(self.timers)
		self.addspell(spell)
		
		if (self.debug) : print("- Boss has ", self.bosshits, " hit points", sep = "")
		
		if self.bosshits <= 0: 
			self.mewins = True
			self.gameover = True
		if (self.debug) : print("")
		
	def playboss(self):
		if (self.debug) : print("-- Boss turn --")
		if (self.debug) : print("- Player has ", self.mehits, " hit points, ", self.mearmor," armor, ",
			self.mana, " mana", sep="" )
		if (self.debug) : print(self.timers)
		self.applyspells()
		if (self.debug) : print("- Boss has ", self.bosshits, " hit points", sep = "")
		if self.bosshits <= 0: 
			self.gameover = True
			self.mewins = True
			return
		md = self.bossdamage - self.mearmor
		if md <= 0: md = 1
		self.mehits -= md
		if (self.debug) : print(" - After attack, player has ", self.mehits, " hit points", sep = "")
		if (self.debug) : print("")
		if self.mehits <= 0: 
			self.gameover = True
			self.mewins = False

	def play(self, spell):
		self.playme(spell)
		if not self.gameover:
			self.playboss()



def onespell(gamex, spell):
	global minmana
	global Spells
	if gamex.gameover:
		if gamex.mewins and gamex.spend < minmana:
			minmana = gamex.spend
			print("minmana: ", minmana, " me: ", gamex.mehits, " boss: ", gamex.bosshits)
		return False

	for spell in range (len (Spells) ):
		game = copy.deepcopy(gamex)
		game.play(spell)
		onespell(game, spell)
	return True
	
def recplay(game):
	global Spells
	#game.out()
	for spell in range (len (Spells) ):
		g = copy.deepcopy(game)
		while(onespell(g, spell)): pass
		
	


game = Players()
##
## Test Case 1
## game.out()
## game.addspell(POISON)
## game.playme()
## game.playboss()
## game.addspell(MAGICMISSILE)
## game.playme()
## game.playboss()
## game.playme()
## game.playboss()
##
## Test Case 2
## game.out()

## game.playme(RECHARGE)
## game.playboss()

## game.playme(SHIELD)
## game.playboss()

## game.playme(DRAIN)
## game.playboss()

## game.playme(POISON)
## game.playboss()

## game.playme(MAGICMISSILE)
## game.playboss()
## exit(1)

recplay(game)
print("Part 1: minimum amount of mana for winning is: ", minmana)
