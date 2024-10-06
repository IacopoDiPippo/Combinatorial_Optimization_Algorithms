import time
import graph_module

# use float("float("Inf")") for edges of infinite weight
# src defines the source vertex and it should always be an out-edge from it to all other vertices with weight $0$.
src = 0
adjacency_matrix = [[float("Inf"), 0, 0, 0],
                    [-1, float("Inf"), 2, 1],
                    [-1, 3, float("Inf"), 3],
                    [2, -1, 3, float("Inf")]]


# Generate random graph
# For each possible edge, with probability prob_inf the edge has weight infinity (i.e. float("Inf")), otherwise a random integer in the interval [lower_cap, higher_cap] is chosen for its weight
num_vertices = 100
lower_cap = -100
upper_cap = 100
prob_inf = .9
#adjacency_matrix = graph_module.random_network_adjacency_matrix(num_vertices,lower_cap,upper_cap,prob_inf,src) #uncomment to use random graph

# creating graph object
graph = graph_module.Graph(adjacency_matrix)


print("Starting the Minimum Mean Cycle Algorithm.")

start_time = time.time()
graph.bellman_ford(src)
end_time = time.time()
bf_time = end_time - start_time
print("Bellman-Ford Algorithm ran in " + str(bf_time) + " seconds.")

start_time = time.time()
min_mean_cycle = graph.minimum_mean_cycle()
end_time = time.time()
mmc_time = end_time - start_time
print("Remaining of the Minimum Mean Cycle Algorithm ran in " + str(mmc_time) + " seconds.")
print("Total of " + str(mmc_time + bf_time) + " seconds.")
if min_mean_cycle == None:
    print("No cycles were found")
else:
    print("Cycle found has mean weight of: " + str(min_mean_cycle[1]))
    print("The edges in the cycle are: " + str(min_mean_cycle[0]))