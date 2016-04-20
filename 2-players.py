from copy import deepcopy
import random as r
import collections as c

newDeck = lambda n, c: list((range(1,n+1)))*c

def shuffleDeck(deck):
    r.shuffle(deck)
    return deck

def distribute(deck):
    n = len(deck)
    return [deck[:n//2],deck[n//2:]]

def playTurn(current_state, played):
    fighting = [0,0]
    cards_already_engaged = len(played)
    for i in range(2):
        if current_state[i] != []:
            fighting[i] = current_state[i][0]         
            current_state[i].pop(0)
        else:
            fighting[i] = -1
    played[:0] = sorted(filter(lambda a : a >= 0, fighting), reverse = True)
    if fighting[0] != fighting[1]:
        current_state[fighting.index(max(fighting))] += played
        return current_state, []
    else:
        return current_state, played

def playGame(state, verbose):
    played = []
    game = []
    while state[0] != [] and state[1] != [] and [state,played] not in game:
        game = game+[[deepcopy(state),played[::]]]
        state, played = playTurn(state, played)
    if [state,played] in game:
        print("INFINITE")
        print(game)
        return "wow"
    elif verbose and played != []:
        print("Draw")
    elif verbose and len(state[0]) > len(state[1]):
        print("Player 1 win")
    elif verbose:
        print("Player 2 win")
    return game + [state, played]

lol = distribute(shuffleDeck(newDeck(3,4)))
while playGame(lol,True) != "wow":
    lol = distribute(shuffleDeck(newDeck(13,4)))
