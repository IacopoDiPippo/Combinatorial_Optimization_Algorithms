from datetime import datetime
import random

# Creates a random cost adjacency matrix
# For each possible edge, a random integer in the interval [lower_cap, higher_cap] is chosen
def random_network_adjacency_matrix(num_vertices,prob_inf,lower_cap,upper_cap,lower_cost,upper_cost,sup_dem_range):
    random.seed(datetime.now().timestamp()) # Initializing seed from random
    
    # sampling random graph with capacities and costs on edges
    r_adjacency_matrix = [[[0,0] for _ in range(num_vertices)] for _ in range(num_vertices)]
    for u in range(num_vertices):
        for v in range(num_vertices):
            if r_adjacency_matrix[v][u][0] > 0:
                r_adjacency_matrix[u][v] = [0,-r_adjacency_matrix[v][u][1]]
            elif u == v or prob_inf > random.uniform(0, 1):
                r_adjacency_matrix[u][v] = [0,float("Inf")]
                continue
            else:
                r_cap = random.randint(lower_cap,upper_cap)
                r_cost = random.randint(lower_cost,upper_cost)
                r_adjacency_matrix[u][v] = [r_cap,r_cost]
    
    # sampling supply and demands
    r_sup_dem = []
    sum = 0
    for u in range(num_vertices):
        if u == num_vertices - 1:
            r_sup_dem.append(-sum)
        else:
            r_num = random.randint(-sup_dem_range, sup_dem_range)
            r_sup_dem.append(r_num)
            sum += r_num
        
    return [r_adjacency_matrix,r_sup_dem]


class Graph:
    # Defining Constructor
    def __init__(self, adjacency_matrix, sup_dem):
        self.vertex_num = len(adjacency_matrix)
        self.vertex_list = [i for i in range(self.vertex_num)]
        self.original_adjacency_matrix = adjacency_matrix

        self.residual_graph=[]
        for u in range(self.vertex_num):
            self.residual_graph.append([])
            for v in range(self.vertex_num):
                cap = adjacency_matrix[u][v][0]
                cost = adjacency_matrix[u][v][1]
                self.residual_graph[u].append([cap,cost])

        self.sup_dem = sup_dem

    def bellman_ford(self, src):
        n = self.vertex_num+1
        self.f[0][src] = {"cost" : 0, "parent" : None}
        for i in range(1,n+1):
            for u in range(n):
                for v in range(n):
                    cost_uv = self.digraph[u][v][1]
                    if self.f[i-1][u]["cost"] != float("Inf") and self.f[i-1][u]["cost"] + cost_uv <= self.f[i][v]["cost"]:
                        self.f[i][v] = {"cost" : self.f[i-1][u]["cost"] + cost_uv, "parent" : u}
        return


    # This method returns a tuple (C, mu), where C is a minimum mean cycle and mu is its mean cost if such a cycle exists, otherwise it should return None.
    # The returned minimum mean cycle C is a list of lists of the form [u,v,[capacity(u,v),cost(u,v)]], where (u,v) is an edge in the cycle
    def minimum_mean_cycle(self):
        n = self.vertex_num

        # creating digraph copied from residual
        # removes edges of 0 capacities have infinite cost in the copy
        self.digraph = []
        for u in range(n):
            self.digraph.append([])
            for v in range(n):
                cap = self.residual_graph[u][v][0]
                cost = self.residual_graph[u][v][1]
                self.digraph[u].append([cap,cost])
                if self.digraph[u][v][0] == 0:
                    self.digraph[u][v][1] = float("Inf")
        for u in range(n):
            self.digraph[u].append([0,float("Inf")])
        self.digraph.append([[0,0] for _ in range(n+1)])
        src = n
        self.digraph[src][src][1] = float("Inf")
        n = n+1

        # self.vertex_num = len(self.residual_graph)
        # self.vertex_list = [i for i in range(self.vertex_num)]
        # self.residual_graph = self.residual_graph
        self.f = [[{"cost" : float("Inf"), "parent" : None} for _ in range(n)] for _ in range(n+1)]
        
        self.bellman_ford(src)

        fkx =  [[(self.f[n][x]["cost"] - self.f[k][x]["cost"])/(n-k) for k in range(n) if self.f[k][x]["cost"] != float("Inf")] for x in range(n)]
        fx_max = [max(fkx[k]) for k in range(n)]

        mu = min(fx_max)
        if mu == float("Inf"):
            return None

        x_star = fx_max.index(mu)
        cycle = self.find_cycle(x_star)

        return (cycle, mu)

    def find_cycle(self,x_star):
        n = self.vertex_num+1

        # Computing progression until a cycle is found
        visited = [False] * n
        progression = []
        v = x_star
        for i in range(n,-1,-1):
            visited[v] = True
            parent = self.f[i][v]["parent"]
            progression.append((parent,v,self.digraph[parent][v]))
            v = parent
            if visited[v] == True:
                break

        # From progression, extracting just the cycle
        cycle = []
        progression.reverse()
        for e in progression:
            cycle.append(e)
            if e[1] == v:
                break

        return cycle

    # Edmonds-Karp algorithm
    def edmonds_karp(self, source, sink):
        max_flow = 0
        parent = [-1] * (self.vertex_num)
        
        while self.find_aug_path_BFS(source, sink, parent):
            path_flow = float("Inf") # artificial unbounded upper value
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.residual_graph[parent[s]][s][0])
                s = parent[s]

            max_flow += path_flow # Adding the path flows

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.residual_graph[u][v][0] -= path_flow
                self.residual_graph[v][u][0] += path_flow
                v = parent[v]

        return max_flow
    
    # BFS to find augmenting path
    def find_aug_path_BFS(self, s, t, parent):

        visited = [False] * (self.vertex_num)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)
            for ind, val in enumerate(self.residual_graph[u]):
                if visited[ind] == False and val[0] > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False
    
    # This method updates the residual graph with an initial b-flow
    # This is done by including an artificial source and sink and solving the max flow problem
    # If no b-flow exists, it returns False, otherwise it returns True
    def initial_b_flow(self):
        n = self.vertex_num

        # Extend residual_graph to include a source and a sink
        for i in range(n):
            self.residual_graph[i].append([0,0])
            self.residual_graph[i].append([0,0])
        self.residual_graph.append([[0,0] for i in range(n+2)])
        self.residual_graph.append([[0,0] for i in range(n+2)])

        # reducing to maximum flows to find a b-flow
        source = n
        sink = n+1
        supply_sum = 0
        for v in range(n):
            if self.sup_dem[v] < 0:
                self.residual_graph[v][sink][0] = - self.sup_dem[v]
            if self.sup_dem[v] > 0:
                self.residual_graph[source][v][0] = self.sup_dem[v]
                supply_sum = supply_sum + self.sup_dem[v]
        self.vertex_num = len(self.residual_graph)
        self.vertex_list = [i for i in range(self.vertex_num)]
        self.residual_graph = self.residual_graph
        self.f = [[{"cost" : float("Inf"), "parent" : None} for _ in range(self.vertex_num)] for _ in range(self.vertex_num+1)]
        
        # Update the residual graph with a b-flow, if any
        max_flow = self.edmonds_karp(source, sink)
        
        # Removing source and sink
        self.residual_graph.pop()
        self.residual_graph.pop()
        for v in self.residual_graph:
            v.pop()
            v.pop()
        self.vertex_num = len(self.residual_graph)
        self.vertex_list = [i for i in range(self.vertex_num)]
        self.residual_graph = self.residual_graph
        self.f = [[{"cost" : float("Inf"), "parent" : None} for _ in range(self.vertex_num)] for _ in range(self.vertex_num+1)]

        # If no initial is found, return False
        if max_flow != supply_sum:
            return False
        else:
            return True

    # Minimum Mean Cycle Cancelling algorithm
    # Returns None if no initial b-flow is found (instance is unfeasible), otherwise updates the residual graph to the residual graph of a minimal cost b-flow and returns its cost
    def minimum_mean_cycle_cancelling(self):

        # update residual graph with an initial b-flow
        if self.initial_b_flow()==False:
            return None
        
        cycle = self.minimum_mean_cycle()
        while cycle != None and cycle[1] < 0:
            # find maximum flow one can push through the cycle
            gamma = float("Inf")
            for e in cycle[0]:
                if gamma > e[2][0]:
                    gamma = e[2][0]
            
            # push the flow and update residual graph
            for e in cycle[0]:
                u = e[0]
                v = e[1]
                self.residual_graph[u][v][0] -= gamma
                self.residual_graph[v][u][0] += gamma
            cycle = self.minimum_mean_cycle()
            
        # compute actual b-flow solution by comparing the residual graph to the original
        total_cost = 0
        n = self.vertex_num
        for u in range(n):
            for v in range(n):
                cap_original = self.original_adjacency_matrix[u][v][0]
                if cap_original < 0:
                    continue
                cap_residual = self.residual_graph[u][v][0]
                flow = cap_original - cap_residual
                uv_cost = self.original_adjacency_matrix[u][v][1]
                if uv_cost == float("Inf"):
                    uv_cost = 0
                total_cost += flow * uv_cost

        return total_cost
