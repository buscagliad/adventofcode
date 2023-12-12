import copy
from collections import namedtuple


# Hit Points: 55
# Damage: 8

BOSS_DAMAGE = 8
BOSS_HIT_POINTS = 55

minmana = 100000000
Spell = namedtuple('spell', "cost, damage, armor, heals, cycles, addMana, name")
# tuple:     [cost, damage, armor, heals, cycles, addMana,    xxx, name]
#                0       1      2      3       4        5       6  7
Spells = [
	Spell( 53,      4,     0,     0,      1,       0,  "MagicMissle"),
	Spell( 73,      2,     0,     2,      1,       0,  "Drain"),
	Spell(113,      0,     7,     0,      6,       0,  "Shield"),
	Spell(173,      3,     0,     0,      6,       0,  "Poison"),
	Spell(229,      0,     0,     0,      5,     101,  "Recharge") ]

hard = False


def applyspells(g):
	global Spells
	for i, t in enumerate(g['timers']):
		if (t == 0) : continue
		g['timers'][i] -= 1
		spell = Spells[i]
		g['bosshits'] -= spell.damage
		g['mana'] += spell.addMana
	return True


''' playxxx returns True is game is still active
            returns False if boss or player wins
'''

def playme(g):
	if hard:
		g['mehits'] -= 1
		if g['mehits'] <= 0:
			return False
	applyspells(g)
#	addspell(g)
	return True

	
def playboss(g):
	applyspells(g)
	if g['bosshits'] <= 0: 
		return False
	md = g.bossdamage
	if g['timers'][2] > 0:
		md = g.bossdamage - 7
	if md <= 0: md = 1
	g['mehits'] -= md
	if g['mehits'] <= 0: 
		print("Boss wins")
		return False
	return True

def play(g):
	if not playme(g):
		return playboss(g)
	return True

	
def recplay(game):
	global Spells
	global minmana
	games = [dict(mana=500, mehits=50, bosshits=55, timers=[0,0,0,0,0], spend=0)]
	while games:
		g = games.pop()
		if g['spend'] > minmana: continue
		for i, spell in enumerate(Spells):
			if g['timers'][i] > 0: continue
			gc = copy.deepcopy(g)
			gc['timers'][i] = spell.cycles
			if play(gc):
				games.append(gc)
			else:
				if gc['mehits'] > 0 and gc['spend'] < minmana:
					minmana = gc['spend']
					print("Minmana: ", minmana, " depth: ", len(games))
	


minmana = 100000000
#recplay(games)
print("Part 1: minimum amount of mana for winning is: ", minmana)

hard = True

ngames = [dict(mana=500, mehits=50, bosshits=55, timers=[0,0,0,0,0], spend=0)]

minmana = 100000000
recplay(ngames)
print("Part 2: minimum amount of mana for winning is: ", minmana)


