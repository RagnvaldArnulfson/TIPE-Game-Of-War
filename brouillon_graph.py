from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx
import random as r

nouveauPaquet = lambda n, c: list((range(1,n+1)))*c

def melanger(deck):
    r.shuffle(deck)
    return deck

def distribuer(deck):
    n = len(deck)
    return [deck[:n//2],deck[n//2:]]
    
def permutations(l):
    if len(l) <= 1:
        return [l]
    perm = [] 
    for i in range(len(l)):
       m = l[i]
       sous_liste = l[:i] + l[i+1:]
       for p in permutations(sous_liste):
           perm.append([m] + p)
    return perm

def supprimerRepetitions(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n
    
def permutationsSansRepetition(l):
    if len(l) <= 1:
        return [l]
    perm = []
    dejaVus = []
    for i in range(len(l)):
        if l[i] not in dejaVus:
            m = l[i]
            dejaVus.append(l[i])
            sous_liste = l[:i] + l[i+1:]
            for p in permutationsSansRepetition(sous_liste):
                perm.append([m] + p)
    return perm


def jouerTour(decks, enJeu):
    joue = [0,0]
    while joue[0] == joue[1] and joue != [-1,-1]:
        for i in range(2):
            if decks[i] != []:
                joue[i] = decks[i][0]         
                decks[i].pop(0)
            else:
                joue[i] = -1
        enJeu += filter(lambda a : a >= 0, joue)
    if joue != [-1,-1]:
        return decks,enJeu,joue.index(max(joue))
    else:
        return [[],[]],[],1
    
def decksString(decks):
    return '.'.join(map(str,decks[0]))+" ; "+'.'.join(map(str,decks[1]))

def partieAleatoire(decks):
    partie = [decksString(decks)]
    enJeu = []
    
    F = nx.DiGraph()
    previous = decksString(decks)
    
    while decks[0] != [] and decks[1] != []:
        decks, enJeu, gagnant = jouerTour(decks, enJeu)
        strategies = permutationsSansRepetition(enJeu)
        enJeu = []
        decks[gagnant] += strategies[r.randint(0,len(strategies)-1)]
        
        visu = decksString(decks)
        partie += [visu]
        F.add_edge(previous,visu)
        previous = visu
        
    pos = nx.spectral_layout(F)
    plt.figure(facecolor = 'w')
    plt.axis('off')
    
    nx.draw_networkx_edges(F,pos,alpha=0.2)
    nx.draw_networkx_labels(F,pos)
    
    plt.show()
    return partie

def partieComplete(decks,partie):
    partie += deepcopy([decks])
    enJeu = []
    while decks[0] != [] and decks[1] != []:
        decks, enJeu, gagnant = jouerTour(decks, enJeu)
        strategies = permutationsSansRepetition(enJeu)
        for strat in strategies:
            enJeu = []
            decks[gagnant] += strat
            partieComplete(decks,partie)
    return partie
    
partieAleatoire([[1,2],[2,1]])
