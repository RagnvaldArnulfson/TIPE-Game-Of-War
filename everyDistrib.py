import math as m
from itertools import groupby
import operator
from collections import Counter
from functools import reduce

def cardPermutations(l):
    num = m.factorial(len(l))
    mults = Counter(l).values()
    den = reduce(operator.mul, (m.factorial(v) for v in mults), 1)
    return num // den

def permutationsSansRepetition(l,maj = -1):
    if len(l) <= 1:
        return [l]
    perm = []
    dejaVus = []
    for i in range(len(l)):
        if l[i] not in dejaVus:
            m = l[i]
            dejaVus.append(l[i])
            sous_liste = l[:i] + l[i+1:]
            for p in permutationsSansRepetition(sous_liste,-1):
                if maj==-1 or len(perm)<maj:
                    perm.append([m] + p)
    return perm
    
    
def toutesDistributions(deck):
    n = len(deck)//2
    permCard = cardPermutations(deck)
    
    l = permutationsSansRepetition(deck,permCard//2)
    
    distribs = []
    
    for e in l:
        distribs +=  [[e[:n],e[n:]]]
    return distribs
