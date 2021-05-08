import networkx as nx
import matplotlib.pyplot as plt
from random import randint

def randomList(v, e, k): 
    arr = [0] * v; 
       
    for i in range(2*e):
        while True:
            j = randint(0, v-1)
            if arr[j] < min(v-1,k):
                break
            
        arr[j] += 1; 
    print(arr)
    return arr


def generateGraph(v, e, k):
    """
    k: Grado máximo del vertice
    e: Cantidad de aristas
    v: Número de vértices
    """
    if e > k*v/2:
        print("No se puede generar un grafo de estas características")
        return None
    elif e > v*(v-1)/2:
        print(f"No se puede generar un grafo de {v} nodos con más de {v*(v-1)//2} aristas")
        return None
    elif e == v*(v-1)/2:
        return nx.complete_graph(v)
    else:
        arr = randomList(v, e, k)
        while True:
            try:
                G = nx.random_degree_sequence_graph(arr)
                break
            except Exception:
               pass 
        return G

def fibonacci_sequence(arr: list)-> list:
    if len(arr) <= 2:
        return []
    
    i = 0
    j = 1
    new_arr = []

    while i < len(arr) and j < len(arr):
        if len(new_arr) == 0:
            new_arr.append(arr[i])
            new_arr.append(arr[j])
        
        s = arr[i] + arr[j]
        if s in arr:
            new_arr.append(s)
            i = j
            j = arr.index(s)
        else:
            if len(new_arr) > 2:
                break
            else:
                new_arr = []
                i += 1
                j += 1
    return new_arr