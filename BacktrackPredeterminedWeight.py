# -*- coding: cp1252 -*-
import random as rd

jeu52Cartes = [(i%13)+1 for i in range(13*4)]
#poids du jeu : 364
#poids minimal d'un paquet (26 cartes tirÃ©es dedans) : 98
#poids maximal : 266 (=364-98)

jeu32Cartes = [(i%8)+1 for i in range(8*4)]
#poids du jeu : 144
#poids minimal d'un paquet (16 cartes tirÃ©es dedans) : 40
# maximal : 104 (=144-40)


#CF NB en bas de page pour des commentaires sur la nouvelle version

#aleatoire boolÃ©en pour savoir si on veut un jeu alÃ©atoire
#attention, augmente significativement le temps de calcul pour les cas Ã©quilibrÃ©s
#si aleatoire == True
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
        paquet2.shuffle()
    
    return [paquet2,paquet1] if jeuContraire else [paquet1,paquet2]
    

#cartesDispo doit Ãªtre triÃ©e Ã  chaque Ã©tape de la rÃ©cursivitÃ©
def genererPaquet(cartesDispo,nombreDeCartesSouhaitees,poidsSouhaite,aleatoire = False,paquetActuel = []):
    
    nombreDeCartesDispo = len(cartesDispo)
    nombreDeCartesActuel = len(paquetActuel)
    poidsActuel = sum(paquetActuel)
    nombreDeCartesATirer = nombreDeCartesSouhaitees-nombreDeCartesActuel
    
    #comme cartesDispo est triÃ©e il est simple de dÃ©terminer le poids min
    #ainsi que le poids max du paquetActuel quand celui-ci sera complet
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
        rd.shuffle(piocheAlea)

    for cartePioche in piocheAlea:
        if cartePioche not in dejaVu:
            dejaVu.append(cartePioche)
            nouveauDispo = cartesDispo[:]
            nouveauDispo.remove(cartePioche)
            #nouveau dispo est bien triÃ©
            solution = genererPaquet(nouveauDispo,nombreDeCartesSouhaitees,poidsSouhaite,aleatoire,paquetActuel+[cartePioche])
            if solution != []:
                return solution
    
    return []


#preuve que mÃªme si le tirage est alÃ©atoire, le temps de calcul pour les cas
#de poids extremes est relativement rapide
#(Ã§a tombe bien c'est ce qui nous intÃ©resse)
for i in range(100):
    print(genererDistribution(jeu52Cartes,100,True)[0])
    
    
#NB :
#on a ajoutÃ© une condition d'arrÃªt symetrique Ã  l'ancienne qui utilisais ajoutMin
#on a rendu cette condition plus fine en considÃ©rant que si cartesDispo est triÃ©e
#Ã  chaque niveau de la rÃ©cursivitÃ©, on peut vraiment donner le poidsMin ainsi que
#le poidsMax du paquet courant (et non plus un simple minorant)
#le renversement du probleme (jeuContraire) reste pertinent car si cartesDispo est
#triÃ©e par ordre croissant, les solutions de poids faibles sont trouvÃ©es en premier
    
