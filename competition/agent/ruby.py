from pprint import pprint
from enum import Enum
from operator import itemgetter
#class Strategy(Enum):
#    GREEDY = 1
#    CONTROL = 2
#turn = 1
# Modify this function
def start():
    print('start')
    return None

def listById(id, things):
    found = []
    for index, thing in enumerate(things):
        if (thing['id'] == id):
            found.append((thing, index))
    return found
   

# Modify this function
def play(state):
    enemyMinionList = sorted(state['opponent_target'][1:], key=itemgetter('cost'), reverse=True)

    playableMinions = []
    playableSpells = []
    #if (state['player_mana'] > turn):
    #    turn = state['player_mana'] 

    for card_index, card in enumerate(state['player_hand']):
        if (card['cost'] <= state['player_mana']):
            if (card['type'] == 'spell'):
                playableSpells.append(card)
            else:
                playableMinions.append(card)

    playableMinions = sorted(playableMinions, key=itemgetter('cost'), reverse=True)
    #look for removal spells

    poisonMinion = (1 in [minion["id"] for minion in enemyMinionList])
    chargeMinion = (5 in [minion["id"] for minion in enemyMinionList])
    growMinion = (11 in [minion["id"] for minion in enemyMinionList])
    stickyMinion = (14 in [minion["id"] for minion in enemyMinionList])

    twoSpell = (3 in [spell["id"] for spell in playableSpells])
    chanceSpell = (12 in [spell["id"] for spell in playableSpells])
    fireballSpell = (9 in [spell["id"] for spell in playableSpells])
    #two
    if(stickyMinion and twoSpell):
        minions = listById(14, state['opponent_target'])
        spells = listById(3, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=2):
                return 2, (spells[0][1], minion[1])
    if(growMinion and twoSpell):
        minions = listById(11, state['opponent_target'])
        spells = listById(3, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=2):
                return 2, (spells[0][1], minion[1])
    if(chargeMinion and twoSpell):
        minions = listById(5, state['opponent_target'])
        spells = listById(3, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=2):
                return 2, (spells[0][1], minion[1])
    if(poisonMinion and twoSpell):
        minions = listById(1, state['opponent_target'])
        spells = listById(3, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=2):
                return 2, (spells[0][1], minion[1])
    #chance
    if(stickyMinion and chanceSpell):
        minions = listById(14, state['opponent_target'])
        spells = listById(12, state['player_hand'])
        for minion in minions:
            if(len(state['player_targets']) > 1):
                if(minion[0]['health']<=5):
                    return 2, (spells[0][1], minion[1])
            else:
                if(minion[0]['health']<=3):
                    return 2, (spells[0][1], minion[1])
    if(chargeMinion and chanceSpell):
        minions = listById(5, state['opponent_target'])
        spells = listById(12, state['player_hand'])
        for minion in minions:
            if(len(state['player_targets']) > 1):
                if(minion[0]['health']<=5):
                    return 2, (spells[0][1], minion[1])
            else:
                if(minion[0]['health']<=3):
                    return 2, (spells[0][1], minion[1])
    #fireball
    if(stickyMinion and fireballSpell):
        minions = listById(14, state['opponent_target'])
        spells = listById(9, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=6):
                return 2, (spells[0][1], minion[1])
    if(chargeMinion and fireballSpell):
        minions = listById(11, state['opponent_target'])
        spells = listById(9, state['player_hand'])
        for minion in minions:
            if(minion[0]['health']<=6):
                return 2, (spells[0][1], minion[1])
 
    #play minions
    if(playableMinions):
        for minion in playableMinions:
            if (minion['cost'] <= state['player_mana']):
                minions = listById(minion['id'], state['player_hand'])
                return 1, minions[0][1]
    #trade minion for minionavorable


    for minion_index, minion in enumerate(list(state['player_target'])[1:], start=1):
        for enemy in enemyMinionList:
            if(enemy['health'] <= minion['atk'] and minion['turns_in_play'] > 0):
                minions = listById(enemy['id'], state['opponent_target'])
                return 3, (minion_index, minions[0][1])


    if(state['player_mane'] >= 2):
        return 0



    for minion_index, minion in enumerate(list(state['player_target'])[1:], start=1):
        if (minion['turns_in_play'] > 0):
            return 3, (minion_index, 0)

    return 4, None

# Modify this function
def end(victory):
    print(f'Victor: {victory}')
    return None


# Don't touch this function
def communicate(pipe, *args, **kwargs):
    while True:
        packet = pipe.recv()
        action = packet['action']
        if action == 'start':
            pipe.send(start())
        elif action == 'play':
            pipe.send(play(packet['args']))
        elif action == 'end':
            pipe.send(end([packet['args']]))


class CommunicateDebug:
    def __init__(self, *args):
        self.out = None

    def send(self, packet):
        action = packet['action']
        if action == 'start':
            start()
        elif action == 'play':
            self.out = play(packet['args'])
        elif action == 'end':
            end([packet['args']])

    def recv(self):
        return self.out

