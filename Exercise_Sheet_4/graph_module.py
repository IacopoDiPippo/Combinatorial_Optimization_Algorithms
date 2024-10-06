from datetime import datetime
import random

# Creates a random weight adjacency matrix
# For each possible edge, a random integer in the interval [lower_cap, higher_cap] is chosen
# if the number is negative, the capacity is 0
# otherwise the number becomes the capacity
def random_network_adjacency_matrix(num_vertices,lower_cap,upper_cap):
    random.seed(datetime.now().timestamp()) # Initializing seed from random
    r_adjacency_matrix = []
    for i in range(num_vertices):
        r_adjacency_matrix.append([])
        for j in range(num_vertices):
            r_num = random.randint(lower_cap,upper_cap)
            if j == i or r_num < 0:
                r_num = 0
            r_adjacency_matrix[i].append(r_num)
    return r_adjacency_matrix


class Graph:

    # Defining Constructor
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.numOfVertices = len(adjacency_matrix)

    # DFS to find augmenting path
    # def find_aug_path_DFS(self, current_vertex, t, parent, visited_list):
    def find_aug_path_DFS(self, s, t, parent):

        visited = [False] * (self.numOfVertices)
        stack = []

        stack.append(s)
        visited[s] = True

        while stack:
            u = stack.pop()
            for ind, val in enumerate(self.adjacency_matrix[u]):
                if visited[ind] == False and val > 0:
                    stack.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # BFS to find augmenting path
    def find_aug_path_BFS(self, s, t, parent):

        visited = [False] * (self.numOfVertices)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)
            for ind, val in enumerate(self.adjacency_matrix[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Ford-Fulkerson algorithm
    def ford_fulkerson(self, source, sink):
        max_flow = 0
        parent = [-1] * (self.numOfVertices)
        
        # While there is an augmenting path, do:
        while self.find_aug_path_DFS(source, sink, parent):

            # Finding the highest path flow
            gamma = float("Inf") # artificial unbounded upper value
            s = sink
            while(s != source):
                gamma = min(gamma, self.adjacency_matrix[parent[s]][s])
                s = parent[s]

            # Updating the residual values of edges
            self.update_residual(source, sink, gamma, parent, self.adjacency_matrix)

            max_flow += gamma # Adding the path flows to the solution
        return max_flow
    
    # Edmonds-Karp algorithm
    def edmonds_karp(self, source, sink):
        max_flow= 0 
        parent = [-1] * (self.numOfVertices)
        while self.find_aug_path_BFS(source, sink, parent ):

            gamma = float('Inf')
            s=sink
            while (s!=source):
                gamma = min(gamma, self.adjacency_matrix[parent[s]][s])
                s=parent[s]

            self.update_residual(source,sink,gamma,parent,self.adjacency_matrix)
            max_flow+=gamma
        return max_flow
    
    # Update residual graph
    def update_residual(self, source, sink, gamma, parent_list, residual_graph):
        s=sink
        while (s != source):
            residual_graph[parent_list[s]][s] -= gamma
            residual_graph[s][parent_list[s]] += gamma
            s=parent_list[s]

        return 0