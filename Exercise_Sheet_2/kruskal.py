# Define the function that runs Kruskal's algorithms
# It receives one arguments: a graph
# It outputs a dictionary of weighted edges in a minimum spanning tree
import numpy as np

def kruskals_algorithm(graph):

    edge_list = list(graph.edges.items())
    sorted_edge_list = sorted(edge_list,key=lambda weighted_edge : weighted_edge [1])

    sol={}

    # Creating the set of sets of vertices, each set is a singleton
    # In python, a set cannot contain sets, unless they are "immutable", thus here we use frozenset
    components = {frozenset([v]) for v in graph.vertices}


    for weighted_edge in sorted_edge_list:

        #Starting and ending nodes of edge
        v1=weighted_edge[0][0]
        v2=weighted_edge[0][1]
        
        # c1 and c2 are the connected components containing v1 and v2, respectively
        c1 = next(comp for comp in components if v1 in comp)
        c2 = next(comp for comp in components if v2 in comp)

        # If c1 and c2 are distinct components, include the weighted_edge in our solution, and merge the two components
        if c1 != c2:
            sol[weighted_edge[0]] = weighted_edge[1]
            components.remove(c1)
            components.remove(c2)
            components.add(c1.union(c2))

        
    return sol

