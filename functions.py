import networkx as nx
import matplotlib.pyplot as plt
from random import randint

def randomList(v, e, k): 
    arr = [0] * v;                      #Make an empty array of v elements    
       
    for i in range(2*e):
        while True:
            j = randint(0, v-1)         #Pick a random value j
            if arr[j] < min(v-1,k):     #Evaluate to see if the array in the j position is incrementable
                break
            
        arr[j] += 1
    return arr


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
        while True:
            arr = randomList(v, e, k)   #Make a random list of degrees
            try:                        
                G = nx.random_degree_sequence_graph(arr)
                break
            except Exception:           #This catches an exception if the list generated can't be made a simple graph
               pass 
        return G


def fibonacci_sequence(arr: list)-> list:
    if len(arr) <= 2:                   #No possible Fibonacci subsequences of length <= 2
        return []
    
    i = 0
    j = 1
    sequence = []

    while i < len(arr) and j < len(arr):
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
                i += 1
                j += 1
    return sequence