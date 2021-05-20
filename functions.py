import networkx as nx
from random import randint
import numpy as np

def generateGraph(v, e, k):
    """
    v: Número de vértices
    e: Cantidad de aristas
    k: Grado máximo del vertice
    """
    if e > k*v/2:                     #No graph posible with this parameters
        return None
    elif e > v*(v-1)/2:                 #Simple graph can't have more edges than a complete graph
        return None
    elif e == v*(v-1)/2:                #Check if it's the complete graph, so we can return it instantly
        return nx.complete_graph(v)
    else:
        while True:
            #Make a random list of degrees
            degree_sequence = get_randrom_degree_sequence(v,e,k)
            try:                        
                G = nx.random_degree_sequence_graph(degree_sequence)
                break
            except Exception:           #This catches an exception if the degree sequence generated can't be made a simple graph
                pass 
        return G


def get_randrom_degree_sequence(v, e, k):
    sequence = [0]*v

    while sum(sequence)!= 2*e:
        sequence = [0]*v
        partial_sum = 0
        for i in range(v):
            if partial_sum == 2*e:
                continue
            sequence[i] = randint(0, min(v-1,k,e, 2*e-partial_sum))
            partial_sum += sequence[i]
    
    return sequence


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
        for j in range(multiplicity):
            if j == 0:
                s+= f"c{i}*({root})^n + "
            elif j == 1:
                s+= f"c{i}*n*({root})^n + "
            else:
                s+= f"c{i}*n^{j}*({root})^n + "
            i+=1
    return s[:-3]


def recurrenciavi(coefficients: list, initial_values: list):
    if len(coefficients) - 1 != len(initial_values):
        return ""
    
    recurrence = recurrencia(coefficients)
    constants = get_constant_values(recurrence[7:], initial_values)
    
    for i in range(len(initial_values)):
        recurrence = recurrence.replace(f"c{(i+1)}", f"({constants[i]:.2f})")
    return recurrence


def get_constant_values(recurrence: str, initial_values: list):
    terms = recurrence.split(" + ")
    equation_system = []

    for i in range(len(initial_values)):
        equation = []
        n = i
        for term in terms:
            k = term.index("*")+1
            equation.append(eval(term[k:].replace('^', '**')))
        
        equation_system.append(equation)
    
    return np.linalg.solve(equation_system, initial_values)