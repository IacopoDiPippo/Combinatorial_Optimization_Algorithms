from datetime import datetime
import random

# Creates a random weight adjacency matrix
# For each possible edge, a random integer in the interval [lower_cap, higher_cap] is chosen
def random_network_adjacency_matrix(num_vertices,lower_cap,upper_cap,prob_inf,src):
    random.seed(datetime.now().timestamp()) # Initializing seed from random
    r_adjacency_matrix = []
    for i in range(num_vertices):
        r_adjacency_matrix.append([])
        for j in range(num_vertices):
            r_num = random.randint(lower_cap,upper_cap)
            if prob_inf >= random.uniform(0, 1):
                r_num = float("Inf")
            r_adjacency_matrix[i].append(r_num)
    r_adjacency_matrix[src] = [0] * num_vertices
    return r_adjacency_matrix


class Graph:
    # Defining Constructor
    def __init__(self, adjacency_matrix):
        self.vertex_num = len(adjacency_matrix)
        self.vertex_list = [i for i in range(self.vertex_num)]
        self.adjacency_matrix = adjacency_matrix
        self.f = [[{"weight" : float("Inf"), "parent" : None} for _ in range(self.vertex_num)] for _ in range(self.vertex_num+1)]

    def bellman_ford(self, src):
        n = self.vertex_num
        self.f[0][src] = {"weight" : 0, "parent" : None}

        for i in range(1,n+1):
            for u in range(n):
                for v in range(n):
                    weight_uv = self.adjacency_matrix[u][v]
                    if self.f[i-1][u]["weight"] != float("Inf") and self.f[i-1][u]["weight"] + weight_uv <= self.f[i][v]["weight"]:
                        self.f[i][v] = {"weight" : self.f[i-1][u]["weight"] + weight_uv, "parent" : u}


    # This method should return a tuple of a minimum mean cycle and its mean weight mu if a cycle exists, otherwise it should return None.
    # The cycle should be returned as a list of tuples (u,v,weight(u,v)), where (u,v) is a directed edge in the cycle, and weight(u,v) is its weight.
    # This method should make use of the values stored in the matrix self.f to compute mu and a vertex x_star for which an edge progression from the source to x_star contains a minimum mean cycle of weight mu.
    # The variable self.f is a matrix such that self.f[i][x]["weight"] returns the weight of a shortest edge progression P from the source to vertex x with exactly i edges, and self.f[i][x]["parent"] returns the vertex that is the predecessor of x in P.
    # After finding x_star, the method should call self.find_cycle(x_star) to obtain the corresponding minimum mean cycle.
    def minimum_mean_cycle(self):
        n = self.vertex_num # number of vertices
        vertex_list = self.vertex_list # list of vertices

        fkx =  [[(self.f[n][x]["weight"] - self.f[k][x]["weight"])/(n-k) for k in range(n) if self.f[k][x]["weight"] != float("Inf")] for x in range(n)]
        fx_max = [max(fkx[k]) for k in range(n)]
        mu = min(fx_max)
        

        if mu == float("Inf"):
            return None

        x_star= fx_max.index(mu)
        cycle = self.find_cycle(x_star)
        return (cycle, mu)


    # Given, a vertex x_star for which an edge progression P from the source to x_star contains a cycle, this method should return a in the edge progression cycle.
    # The found cycle should be a list of tuples (u,v,weight(u,v)), where (u,v) is a directed edge in the cycle, and weight(u,v) is its weight.
    # This method should make use of the values stores in the matrix self.f the cycle in P.
    # The variable self.f is a matrix such that self.f[i][x]["weight"] returns the weight of a shortest edge progression P from the source to vertex x with exactly i edges, and self.f[i][x]["parent"] returns the vertex that is the predecessor of x in P.
    def find_cycle(self,x_star):
        n = self.vertex_num # number of vertices
        vertex_list = self.vertex_list # list of vertices

        # modify this code so cycle is computed correctly
        cycle = []
        visited = [0] * n
        
        for i in range(n,-1,-1):
            parent = self.f[i][x_star]["parent"]
            if visited[parent] == 0:
                visited[parent] = i             
                cycle.append((parent, x_star, self.adjacency_matrix[parent][x_star]))
                x_star = parent
            else : 
                cycle.append((parent, x_star, self.adjacency_matrix[parent][x_star]))
                x_star = parent
                del cycle[0:n-visited[parent]+1]
                break
        
        cycle.reverse()

        return cycle