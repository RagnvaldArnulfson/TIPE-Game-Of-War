# -*- coding: cp1252 -*-
import networkx as nx
import random as r
import matplotlib.pyplot as plt
from copy import deepcopy
import scipy.stats as stats
import sys
sys.setrecursionlimit(10000) 


jeu52Cartes = [(i%13)+1 for i in range(13*4)]
#poids du jeu : 364
#poids minimal d'un paquet (26 cartes tirÃ©es dedans) : 98
#poids maximal : 266 (=364-98)

jeu32Cartes = [(i%8)+1 for i in range(8*4)]
#poids du jeu : 144
#poids minimal d'un paquet (16 cartes tirÃ©es dedans) : 40
# maximal : 104 (=144-40)


def genererDistribution(jeuComplet,poidsSouhaite,aleatoire = False):
    
    jeuComplet = sorted(jeuComplet) #ON TRIE LE JEU DONNE (obligatoire pour genererPaquet)
    poidsTotal = sum(jeuComplet)

    jeuContraire = False

    if poidsSouhaite > poidsTotal//2:
        poidsSouhaite = poidsTotal-poidsSouhaite
        jeuContraire = True
    
    paquet1 = genererPaquet(jeuComplet,len(jeuComplet)//2,poidsSouhaite,aleatoire)
    
    paquet2 = jeuComplet[:]
    for carte in paquet1:
        paquet2.remove(carte)
    
    if aleatoire:
        r.shuffle(paquet2)
    
    return [paquet2,paquet1] if jeuContraire else [paquet1,paquet2]
    
def genererPaquet(cartesDispo,nombreDeCartesSouhaitees,poidsSouhaite,aleatoire = False,paquetActuel = []):
    
    nombreDeCartesDispo = len(cartesDispo)
    nombreDeCartesActuel = len(paquetActuel)
    poidsActuel = sum(paquetActuel)
    nombreDeCartesATirer = nombreDeCartesSouhaitees-nombreDeCartesActuel

    poidsMin = poidsActuel + sum(cartesDispo[:nombreDeCartesATirer])
    poidsMax = poidsActuel + sum(cartesDispo[(nombreDeCartesDispo-nombreDeCartesATirer):])
    
    if nombreDeCartesActuel == nombreDeCartesSouhaitees and poidsActuel == poidsSouhaite:
        return paquetActuel
    elif nombreDeCartesActuel == nombreDeCartesSouhaitees \
        or poidsMin > poidsSouhaite or poidsMax < poidsSouhaite:
        return []
    
    
    dejaVu = []
    
    piocheAlea = cartesDispo[:]
    if aleatoire:
        r.shuffle(piocheAlea)

    for cartePioche in piocheAlea:
        if cartePioche not in dejaVu:
            dejaVu.append(cartePioche)
            nouveauDispo = cartesDispo[:]
            nouveauDispo.remove(cartePioche)
            solution = genererPaquet(nouveauDispo,nombreDeCartesSouhaitees,poidsSouhaite,aleatoire,paquetActuel+[cartePioche])
            if solution != []:
                return solution
    
    return []
    
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
        return [[],[]],[],2 #EGALITE
    
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
    
    nx.draw_networkx_edges(F,pos,alpha=0.7)
    nx.draw_networkx_labels(F,pos)
    
    plt.show()
    
    return partie

def recPartieComplete(decks,partie,graphePartie):
    partie += deepcopy([decks])
    
    previous = decksString(decks)
    
    decks, enJeu, gagnant = jouerTour(decks, [])
    strategies = permutationsSansRepetition(enJeu)
    res = []
    
    for strat in strategies:
        nouveauDeck = []
        if gagnant == 0:
            nouveauDeck = deepcopy([decks[0] + strat,decks[1]])
        elif gagnant == 1:
            nouveauDeck = deepcopy([decks[0],decks[1] + strat])
            
        if gagnant == 0 and decks[1]==[]:
            graphePartie.add_edge(previous,"P1")
            return "P1"
        elif gagnant == 1 and decks[0]==[]:
            graphePartie.add_edge(previous,"P2")
            return "P2"
        elif gagnant == 2:
            graphePartie.add_edge(previous,"E")
            return "E"
        else:
            visu = decksString(nouveauDeck)
            graphePartie.add_edge(previous,visu)
            
            appelRec = "BOUCL"
            
            if nouveauDeck not in partie:
                appelRec = recPartieComplete(nouveauDeck,partie,graphePartie)
                res += [appelRec]
            else:
                res += ["BOUCL"]
    
            if len(nouveauDeck[0]) == len(nouveauDeck[1]):
                test = ""
                if appelRec=="P1":
                    test = "P1"
                elif appelRec=="P2":
                    test = "P2"
                elif appelRec=="BOUCL":
                    test = "BOUCL"
                elif appelRec=="E":
                    test = "E"
                print(visu+" : "+test)
    
    
    if "P1" in res and gagnant==0:
        return "P1"
    elif "P2" in res and gagnant==1:
        return "P2"
    elif "E" in res:
        return "E"
    elif "BOUCL" in res:
        return "BOUCL"
    elif gagnant==0: #DANS TOUS LES CAS PERDANT
        return "P2" 
        
    return "P1"
                     
    
def partieComplete(decks,draw):
    F = nx.DiGraph()
    
    print(recPartieComplete(decks,[],F))
    if draw:
        pos = nx.spring_layout(F)
        plt.figure(facecolor = 'w')
        plt.axis('off')
        
        nx.draw_networkx_edges(F,pos,alpha=0.5)
        nx.draw_networkx_labels(F,pos)
        
        plt.show()
    
    return F

a = distribuer(melanger(nouveauPaquet(8,4)))
print(a)
partieComplete(a,False)
