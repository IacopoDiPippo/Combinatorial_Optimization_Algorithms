# Define the function that finds nearest vertex not in the visited
# It receives tree arguments: list dist with the distances, list of vertices V, and the list of visited vertices in the visited
# It outputs nearest vertex not in the visited if any, otherwise it should return -1
def minDistance(dist, V, visited):
    
    mindist= float('inf')
    v_min=-1
    for v in V:
        if visited[v]==False and dist[v]<mindist:
            mindist=dist[v]
            v_min=v

    if mindist!=float('inf'):
        return v_min


    return -1


# Define the function that runs Dijkstra's algorithms
# It receives one arguments: a graph, initial vertex s and final vertex t
# It outputs a dictionary of the edges in a shortest from s to t
def dijkstra_algorithm(graph,s,t):

    V = graph.vertices
    E = graph.edges.items()

    dist = [float("inf")] * len(V)
    dist[s] = 0
    visited_order_list = [] #used for printing reasons
    visited = [False] * len(V)
    visited[s] = True

    # For each vertex v adjacent to s, start with distance value equal to 1
    edges_incident_to_s = [e[0] for e in E if e[1] == 1 and (e[0][0] == s or e[0][1] == s)]
    for e in edges_incident_to_s:
        if e[0] != s:
            v = e[0]
        else:
            v = e[1]
        dist[v] = 1
        visited_order_list.append(e)

    while dist[t] == float("inf"):

        # Obtain nearest vertex not in the visited and include it in the visited
        # if u == -1, then no path can be found
        u = minDistance(dist, V, visited)
        if u == -1:
            return (visited_order_list,dist)
        visited[u] = True

        # For each vertex v not in visited that is adjacent to u, update distance value
        edges_incident_to_u = [e[0] for e in E if e[1] == 1 and (e[0][0] == u or e[0][1] == u)]
        for e in edges_incident_to_u:
            if e[0] != u:
                v = e[0]
            else:
                v = e[1]

            if (visited[v] == False and dist[v] > dist[u] + 1):
                dist[v] = dist[u] + 1
                visited_order_list.append(e)

    return  (visited_order_list,dist)
