import random as r
import collections as c

newDeck = lambda n: list((range(1,n+1)))*4

def shuffleDeck(deck):
    r.shuffle(deck)
    return deck

def distribute(deck, p):
    n = len(deck)
    len_sub = n//p
    return [deck[i:i+len_sub] for i in range(0,n,len_sub) if len(deck[i:i+len_sub])==len_sub]

def fight(played):
    same_cards = c.defaultdict(list)
    for i, item in enumerate(played):
        same_cards[item].append(i)
    same_cards = {k: v for k, v in same_cards.items() if len(v) > 1}
    if same_cards == {} or max(same_cards) != max(played):
        return False, played.index(max(played))
    else:
        return True, same_cards.values()[0]

def playTurn(current_state):
    war = True
    played = []
    cards_already_engaged = 0
    still_here = list(range(len(current_state)))
    players = still_here
    while war:
        p = len(still_here)
        for pl in players:
            if pl in still_here:
                played += [current_state[pl][0]]
                current_state[pl].pop(0)
            else:
                played += [-1]
        fighting = played[cards_already_engaged:]
        war, still_here = fight(fighting)
        played[cards_already_engaged:] = sorted(filter(lambda a : a >= 0, fighting), reverse = True)
        cards_already_engaged += p
    current_state[players[still_here]] += played
    return current_state
    
print(fight([0,1,1]))
print()
print(playTurn([[1,2,9],[5,4,1],[5,4,9]]))
print()
print(fight([0,1,1]))
print()
lol = distribute(shuffleDeck(newDeck(8)),4)
print(lol)
print(playTurn(lol))
