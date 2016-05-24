from copy import deepcopy
from threading import Thread
import time as t
import random as r
import collections as col
import multiprocessing as mp

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
        fighting[i] = current_state[i][0]         
        current_state[i].pop(0)
    played[:0] = sorted(filter(lambda a : a >= 0, fighting))
    if fighting[0] != fighting[1]:
        current_state[fighting.index(min(fighting))] += played
        return current_state, []
    else:
        return current_state, played

def playGame(state, verbose, c): #FAUX, A ne pas prendre en compte
    played = []
    game = []
    while state[0].count(1) != c and state[0].count(2) != c and state[0] != [] and state[1] != [] and [state,played] not in game:
        game = game+deepcopy([[state,played]])
        state, played = playTurn(state, played)
    if [state,played] in game:
        print("INFINITE")
        print(game)
        return "wow"
    elif verbose:
        print("FINITE")
    return game + [state, played]

def randomSearch(ha):
    n,c = ha
    j = 0
    lol = distribute(shuffleDeck(newDeck(n,c)))
    playGame(lol,False,4)
    deb = t.time()
    while  t.time()-deb < 1:
        j+=1
        playGame(lol,False,4)
        lol = distribute(shuffleDeck(newDeck(n,c)))
    return j
            
class obj_RandomSearch(Thread):
    def __init__(self, n, c):
        Thread.__init__(self)
        self.n = n
        self.c = c

    def run(self):
        randomSearch(self.n,self.c)

result_list = []

def log_result(result):
    # This is called whenever randomSearch returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

if __name__ == '__main__':
    pool = mp.Pool()
    lil = t.time()
    asyncResult = pool.map(randomSearch,[(5, 4)]*100)
    pool.close()
    pool.join()
    print(sum(asyncResult),t.time()-lil)
    
