import time
import graph_module
import numpy as np

# Use float("Inf") for edges of infinite value
# The entry adjacency_matrix[u][v] is a list [capacity(u,v),cost(u,v)] of edge (u,v)
# adjacency_matrix[u][v][0] = 0 represents this edge not existing in the input
# For simplicity, assume that there are no inverse edges in the input, hence adjacency_matrix[u][v][1] = -adjacency_matrix[v][u][1], i.e., the matrix already contains the cost of the backward edge, and adjacency_matrix[v][u][0] = 0 if adjacency_matrix[u][v]][0] > 0
# sup_dem is a list and sup_dem[v] represents the supply of v if positive, and demand if negative
adjacency_matrix = [[[0,float("Inf")], [2,-1], [0,1], [1,1]],
                    [[0,1], [0,float("Inf")], [2,-2], [0,3]],
                    [[1,-1], [0,2], [0,float("Inf")], [0,-1]],
                    [[0,-1], [2,-3], [1,1], [0,float("Inf")]]]
sup_dem = [2,-1,-2,1]


# Generate random graph
# For each possible pair of vertices (u,v), with probability prob_inf there are no edges between this pair (represented by infinite cost).
# Otherwise, an edge is created with a random capacity sampled from the interval [lower_cap, higher_cap] and a random cost sampled from [lower_cost,upper_cost]
# For a pair (u,v), adjacency_matrix[u][v] is the list [capacity(u,v),cost(u,v)]
# The matrix created has the property that adjacency_matrix[u][v][1] = -adjacency_matrix[v][u][1] and adjacency_matrix[v][u][0] = 0 if adjacency_matrix[u][v]][0] > 0
# The routine also creates a sup_dem list with random values that sums up to 0 that are, ,except for one value, sampled from [-sup_dem_range,sup_dem_range] 
num_vertices = 100
prob_inf = .1
lower_cap = 1
upper_cap = 10
lower_cost = -10
upper_cost = 10
sup_dem_range = 5
start_time = time.time()
# [adjacency_matrix,sup_dem] = graph_module.random_network_adjacency_matrix(num_vertices,prob_inf,lower_cap,upper_cap,lower_cost,upper_cost,sup_dem_range) #uncomment to use random graph
end_time = time.time()
bf_time = end_time - start_time
print("Random graph generated in " + str(bf_time) + " seconds.")


# creating graph object
graph = graph_module.Graph(adjacency_matrix,sup_dem)

start_time = time.time()
cost = graph.minimum_mean_cycle_cancelling()
end_time = time.time()
bf_time = end_time - start_time
print("Minimum Mean Cycle-Canceling algorithm ran in " + str(bf_time) + " seconds.")
if cost == None:
    print("No b-flow was found. The instance is unfeasible")
else:
    print("Optimal b-flow has cost: " + str(cost))