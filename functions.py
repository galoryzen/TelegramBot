import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import numpy as np


def generateGraph(v, e, k):
    """
    v: Número de vértices
    e: Cantidad de aristas
    k: Grado máximo del vertice
    """
    if e > k*v/2:                       #No graph posible with this parameters
        return None
    elif e > v*(v-1)/2:                 #Simple graph can't have more edges than a complete graph
        return None
    elif e == v*(v-1)/2:                #Check if it's the complete graph, so we can return it instantly
        return nx.complete_graph(v)
    else:
        degree_sequence_list = get_all_degree_sequences(v,e,k)
        while True:
            #Make a random list of degrees
            degree_sequence = degree_sequence_list[randint(0, len(degree_sequence_list)-1)]
            try:                        
                G = nx.random_degree_sequence_graph(degree_sequence)
                break
            except Exception:           #This catches an exception if the degree sequence generated can't be made a simple graph
                pass 
        return G


def get_randrom_degree_sequence(v, e, k):
    x = np.random.randint(0, min(v-1,k)+1, size=v)
    while sum(x) != 2*e:
        x = np.random.randint(0, min(v-1,k)+1, size=v)
    return x


def get_all_degree_sequences(v, e, k):
    x = []
    for i in range(40):
        arr = get_randrom_degree_sequence(v,e,k)
        if sorted(arr) in x:
            continue
        x.append(sorted(arr))
    return x


def fibonacci_sequence(arr: list)-> list:
    if len(arr) <= 2:                   #No possible Fibonacci subsequences of length <= 2
        return []
    
    i = 0
    j = 1
    sequence = []

    while i < len(arr)-1 and j < len(arr):
        if len(sequence) == 0:          #Add the first 2 numbers into the sequence
            sequence.append(arr[i])
            sequence.append(arr[j])
        
        s = arr[i] + arr[j]
        if s in arr:                    #If the sum is in the array we add it to the sequence and change the iterators
            sequence.append(s)
            i = j
            j = arr.index(s)
        else:                           #If it isn't in the array we check to see if the sequence is longer than 2, in which case we break
            if len(sequence) > 2:
                break
            else:                       #Else we make an empty sequence and increment the iterators
                sequence = []
                j += 1
                if(j == len(arr)):
                    i+=1
                    j = i+1
    return sequence


def recurrencia(coefficients: list)-> str:
    roots = np.roots(coefficients)      #Get roots of the characteristic polynomial of the recurrence relation
    roots = [round(root.real, 2) if round(root.imag,2)==0 else np.round(root, decimals=2) for root in roots]    #Round to 2 decimals and delete imaginary part if its 0
    multiplicities = {root: roots.count(root) for root in set(roots)}
    s = "f(n) = "
    i = 1

    for root, multiplicity in multiplicities.items():
        s+= "("
        for j in range(multiplicity):
            if j == 0:
                s+= f"c{i} + "
            elif j == 1:
                s+= f"c{i}*n + "
            else:
                s+= f"c{i}*n^{j} + "
            i+=1
        s = s[:-3]
        s+=f"){root}^n + "
    return s[:-3]