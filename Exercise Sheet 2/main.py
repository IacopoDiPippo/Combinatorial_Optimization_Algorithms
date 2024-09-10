import time
import maze
import random_graph
import kruskal

# Define some parameters here
height = 4
length = 4
block_size = 40

# Creating a random weighted grid graph
# A graph here is an object containing a list of vertices, and a dictionary of weighted edges
# The keys of entry in this dictionary is a tuple (v1,v2) representing the edge incident to v1 and v2, and it's value is it's weight
start_time = time.time()
grid_graph = random_graph.Graph([],{})
grid_graph.build_weighted_grid(height, length)
end_time = time.time()
print("Random weighted grid graph built in " + str(end_time - start_time) + " seconds")

# Running Kruskal's Algorithm
start_time = time.time()
sol = kruskal.kruskals_algorithm(grid_graph)
end_time = time.time()
print("Kruskal ran in " + str(end_time - start_time) + " seconds")
print("Solution found has cost " + str(sum(sol.values())))

# Drawing a Maze
maze = maze.Maze(block_size,height,length)
maze.draw_animated(sol) # This presents an animated building of the maze (slow)
# maze.draw_final(sol) # This just presents the end result (fast)