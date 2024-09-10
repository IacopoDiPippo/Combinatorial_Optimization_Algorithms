import time
import maze
import random_graph
import dijkstra

# Define some parameters here
height =9
length = 10
block_size = 40
p = .6

# Creating a random weighted grid graph
# A graph here is an object containing a list of vertices, and a dictionary of weighted edges
# The keys of entry in this dictionary is a tuple (v1,v2) representing the edge incident to v1 and v2, and it's value is it's weight
start_time = time.time()
grid_graph = random_graph.Graph([],{})
grid_graph.build_weighted_grid(height, length,p)
end_time = time.time()
s = 0
t = height * length - 1
print("Random weighted grid graph built in " + str(end_time - start_time) + " seconds")

# Drawing a Maze
maze = maze.Maze(block_size,height,length)
maze.draw_final(grid_graph.edges)

# Running Shortest Path Algorithm
start_time = time.time()
sol = dijkstra.dijkstra_algorithm(grid_graph,s,t)
end_time = time.time()
print("Dijkstra ran in " + str(end_time - start_time) + " seconds")
maze.draw_solution(maze,sol,t)


input()
maze.close()