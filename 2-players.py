from copy import deepcopy
from threading import Thread
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
        game = game+deepcopy([[state,played]])
        state, played = playTurn(state, played)
    if [state,played] in game:
        print("INFINITE")
        print(game)
        return ["wow",game]
    elif verbose and played != []:
        print("Draw")
    elif verbose and len(state[0]) > len(state[1]):
        print("Player 1 win")
    elif verbose:
        print("Player 2 win")
    return game + [state, played]
    
def statesBefore(current_state, played):
    if played != []:
        hist = [played[0]]
        return [[[hist+current_state[0], hist+current_state[1]],played[2:]]]
    before = []
    for i in range(2):
        len_deck = len(current_state[i])
        if len_deck > 1:
            a = current_state[i][len_deck-1]
            b = current_state[i][len_deck-2]
            if a < b:
                before += [[[[a]+current_state[1-i],[b]+current_state[i][:len_deck-2]],[]]]
            elif a == b:
                before += [[[current_state[1-i],current_state[i][:len_deck-2]],[a,a]]]
    return before

def findGame(state, knownGame):
    if len(state[0][0]) == len(state[0][1]):
        return knownGame
    
    for hypothesis in statesBefore(state[0],state[1]):
        return findGame(hypothesis, [hypothesis]+knownGame)
    
    
def randomSearch(n,c):
    lol = distribute(shuffleDeck(newDeck(n,c)))
    mdr = playGame(lol,False)
    j = 0
    while mdr[0]!="wow":
        j+=1
        if(j%100==0):
            print(j)
        lol = distribute(shuffleDeck(newDeck(n,c)))
        mdr = playGame(lol,False)
    return mdr[1]
            
class obj_RandomSearch(Thread):
    def __init__(self, n, c):
        Thread.__init__(self)
        self.n = n
        self.c = c
        self.fichier = open("infini"+str(na)+"_"+str(ca)+"-"+str(r.randint(111111,999999))+".txt", "w")

    def run(self):
        self.fichier.write(str(randomSearch(self.n,self.c)))
        self.fichier.close()
        
def foo():
    i = 0
    na, ca = int(input("n?")),int(input("c?"))
    threadList = []
    
    for i in range(10) :
        curThread = obj_RandomSearch(na,ca)
        curThread.daemon = True
        curThread.start()
        threadList.append(curThread)
    
    for curThread in threadList :
    
        curThread.join()
