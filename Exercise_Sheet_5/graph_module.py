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
        self.num_vertices = len(adjacency_matrix)
        self.vertex_list = [i for i in range(self.num_vertices)]

    # DFS to find augmenting path
    # def find_aug_path_DFS(self, current_vertex, t, parent, visited_list):
    def find_aug_path_DFS(self, s, t, parent):

        visited = [False] * (self.num_vertices)
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

        visited = [False] * (self.num_vertices)
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
        parent = [-1] * (self.num_vertices)
        
        while self.find_aug_path_DFS(source, sink, parent):
            path_flow = float("Inf") # artificial unbounded upper value
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.adjacency_matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow # Adding the path flows

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.adjacency_matrix[u][v] -= path_flow
                self.adjacency_matrix[v][u] += path_flow
                v = parent[v]

        return max_flow
    
    # Edmonds-Karp algorithm
    def edmonds_karp(self, source, sink):
        max_flow = 0
        parent = [-1] * (self.num_vertices)
        
        while self.find_aug_path_BFS(source, sink, parent):
            path_flow = float("Inf") # artificial unbounded upper value
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.adjacency_matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow # Adding the path flows

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.adjacency_matrix[u][v] -= path_flow
                self.adjacency_matrix[v][u] += path_flow
                v = parent[v]

        return max_flow
    
    # Push-Relabel (Goldberg-Tarjan)
    def push_relabel(self, source, sink):

        # Initialization of Psi, ex_f_list, and active vertices list
        self.psi = [0] * self.num_vertices
        self.psi[source] = self.num_vertices
        self.ex_f_list = [0] * self.num_vertices
        self.ex_f_list[source] = sum(self.adjacency_matrix[source])
        self.active_vertices = []

        # Update G_f, ex_f_list, active vertices list
        for vertex in range(self.num_vertices):
            gamma = self.adjacency_matrix[source][vertex]
            self.adjacency_matrix[source][vertex] -= gamma
            self.adjacency_matrix[vertex][source] += gamma
            self.ex_f_list[source] -= gamma
            self.ex_f_list[vertex] += gamma
            if gamma > 0:
                self.active_vertices.append(vertex)

        # Main loop
        while self.active_vertices != []:

            # Finding active vertex with max psi
            max_psi_vertex = self.active_vertices[0]
            max_psi = self.psi[max_psi_vertex]
            for vertex in self.active_vertices:
                if self.psi[vertex] > max_psi:
                    max_psi_vertex = vertex
                    max_psi = self.psi[vertex]

            # finding admissible edge (max_psi_vertex, admissible_vertex) - if any
            admissible_vertex = -1
            for w in range(self.num_vertices):
               if self.adjacency_matrix[max_psi_vertex][w] > 0 and max_psi == self.psi[w] + 1:
                   admissible_vertex = w
                   break

            # If an admissible edge is found, then Push and update active vertex list, else relabel
            if admissible_vertex != -1:
                self.push(max_psi_vertex, admissible_vertex)
                if self.ex_f_list[max_psi_vertex] <= 0:
                    self.active_vertices.pop(self.active_vertices.index(max_psi_vertex))
                if self.ex_f_list[admissible_vertex] > 0 and admissible_vertex != source and admissible_vertex != sink and admissible_vertex not in self.active_vertices:
                    self.active_vertices.append(admissible_vertex)
            else:
                self.relabel(max_psi_vertex)

        max_flow = self.ex_f_list[sink]
        return max_flow

    def push(self, v1, v2):
        gamma = min (self.ex_f_list[v1], self.adjacency_matrix[v1][v2])
        self.adjacency_matrix[v1][v2] -= gamma
        self.adjacency_matrix[v2][v1] += gamma  
        self.ex_f_list[v1] -= gamma
        self.ex_f_list[v2] += gamma
        return 0
    
    def relabel(self, v):
        min_psi = self.psi[0]
        for w in range(self.num_vertices):
            if self.adjacency_matrix[v][w] > 0 and self.psi[w] < min_psi:
                min_psi=self.psi[w]
        self.psi[v]=min_psi +1
        return 0