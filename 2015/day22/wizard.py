import copy
from collections import namedtuple


minmana = 100000000
Spell = namedtuple('spell', "cost, damage, armor, heals, cycles, addMana, name")
# tuple: [cost, damage, armor, heals, cycles, addMana,   name]
#            0       1      2      3       4        5       6  
Spells = [
    Spell( 53,      4,     0,     0,      1,       0,  "MagicMissle"),
    Spell( 73,      2,     0,     2,      1,       0,  "Drain"),
    Spell(113,      0,     7,     0,      6,       0,  "Shield"),
    Spell(173,      3,     0,     0,      6,       0,  "Poison"),
    Spell(229,      0,     0,     0,      5,     101,  "Recharge") ]

SP_COST = 0
SP_DAMAGE = 1
SP_ARMOR = 2
SP_HEALS = 3
SP_CYCLES = 4
SP_ADD_MANA = 5
SP_NAME = 6


MANA=0
MEHITS=1
BOSSHITS=2
TIMERS=3
SPENT=4

boss_damage = 0

def applyspells(g, boss_turn=False):
    global Spells
    if boss_turn:
        g[MEHITS] -= boss_damage
    for i, t in enumerate(g[TIMERS]):
        if (t == 0) : continue
        g[TIMERS][i] -= 1
        spell = Spells[i]
        g[BOSSHITS] -= spell.damage
        g[MEHITS] += spell.heals
        g[MANA] += spell.addMana
        if spell.armor > 0 and boss_turn: 
            g[MEHITS] += spell.armor    # this corrects BOSS attack
    return True


#
# returns True if game is still active
def playboss(g):
    applyspells(g, True)


def playme(g):
    applyspells(g, False)


def recplay(mana, mehits, bosshits, BossDamage, hard=False):
    global Spells
    global minmana
    global boss_damage
    boss_damage = BossDamage
    
    #{ ( mana, mehits, bosshits, timers[], spent-mana )
    games = [[mana, mehits, bosshits, [0,0,0,0,0], 0]]
    while games:
        g = games.pop()
        if hard:
            g[MEHITS] -= 1
            if g[MEHITS] <= 0: continue # loss
        
        if g[SPENT] >= minmana: continue  ## if we already spent minmana, no need to go 
        
        ## apply spells for 'me'
        playme(g)
        if g[MEHITS] <= 0: continue
        if g[BOSSHITS] <= 0:
            if minmana > gc[SPENT]: 
                minmana = gc[SPENT]
                print("Minmana: ", minmana, " depth: ", len(games))
            continue

        
        ## apply each available spell
        for i, spell in enumerate(Spells):
            if g[TIMERS][i] > 0: continue ## cannot add this spell as it is active
            if g[MANA] < spell.cost: continue ## cannot affort this spell
            gc = copy.deepcopy(g)
            gc[TIMERS][i] = spell.cycles
            gc[SPENT] += spell.cost
            gc[MANA] -= spell.cost
            ##
            ## plaer played above - time for boss to play
            playboss(gc)
            if gc[BOSSHITS] <= 0:
                if minmana > gc[SPENT]: 
                    minmana = gc[SPENT]
                    # print("Minmana: ", minmana, " depth: ", len(games))
                continue
            games.append(gc)

    

# Hit Points: 55
# Damage: 8

BOSS_DAMAGE = 8
BOSS_HIT_POINTS = 55


minmana = 100000000
#games = [dict(mana=500, mehits=50, bosshits=55, timers=[0,0,0,0,0], spend=0)]
recplay(500, 50, BOSS_HIT_POINTS, BOSS_DAMAGE)
print("Part 1: minimum amount of mana for winning is: ", minmana)
# 953

minmana = 100000000
recplay(500, 50, BOSS_HIT_POINTS, BOSS_DAMAGE, True)
print("Part 2: minimum amount of mana for winning is: ", minmana)

# 1289
