import time
import graph_module

# Insert instance manually
# To use this, you should comment the code on line 18
adjacency_matrix = [[0, 8, 0, 0],
                    [1, 0, 9, 3],
                    [0, 3, 0, 2],
                    [0, 0, 1, 0]]

# Creating a random weight adjacency matrix
# num_vertices denotes the number of vertices in the graph, and for each possible edge (each possible tuple (v,u)), a random integer in the interval [lower_cap, higher_cap] is chosen
# If the number is negative, it's capacity is 0, otherwise the random number becomes the capacity
start_time = time.time()
num_vertices = 100
lower_cap = -100
upper_cap = 100
adjacency_matrix = graph_module.random_network_adjacency_matrix(num_vertices,lower_cap,upper_cap) # uncomment to generate random graph
end_time = time.time()
print("Random network generated in " + str(end_time - start_time) + " seconds.")


# Defining sink and source vertices
source = 0
sink = len(adjacency_matrix)-1


# Running Ford-Fulkerson
adjacency_matrix_copy = [list.copy() for list in adjacency_matrix]
g = graph_module.Graph(adjacency_matrix_copy)
start_time = time.time()
f_max = g.ford_fulkerson(source, sink)
end_time = time.time()
print("Ford-Fulkerson executed in " + str(end_time - start_time) + " seconds. Max Flow found: " + str(f_max))


# Running Edmonds-Karp
adjacency_matrix_copy = [list.copy() for list in adjacency_matrix]
g = graph_module.Graph(adjacency_matrix_copy)
start_time = time.time()
f_max = g.edmonds_karp(source, sink)
end_time = time.time()
print("Edmonds-Karp executed in " + str(end_time - start_time) + " seconds. Max Flow found: " + str(f_max))


# Running Push-Relabel (Goldberd-Tarjan)
adjacency_matrix_copy = [list.copy() for list in adjacency_matrix]
g = graph_module.Graph(adjacency_matrix_copy)
start_time = time.time()
f_max = g.push_relabel(source, sink)
end_time = time.time()
print("Push-Relabel executed in " + str(end_time - start_time) + " seconds. Max Flow found: " + str(f_max))