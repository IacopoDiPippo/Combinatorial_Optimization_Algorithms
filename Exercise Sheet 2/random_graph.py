from datetime import datetime
import random

# Defining a Graph class
# Here, a graph is defined by a list of vertices and edges is a dictionary where the keys are a tuples of vertices the values are their weight
class Graph:
    # Defining Constructor
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        return


    # Defining the method that builds a rectangular grid graph
    # Inputs: height and length of maze
    def build_weighted_grid(self, height, length):

        # Creating a list of vertices
        self.vertices = [i for i in range(height * length)]

        # Initializing seed from random
        random.seed(datetime.now().timestamp())

        # Creating edges with random weights from the interval [0,99]
        # First, add vertical edges, then horizontal edges
        # For simplicity, here we are defining the edges as a tuple (v1,v2) instead of as a set {v1,v2}
        self.edges = {}
        for i in range(1,height):
            for j in range(length):
                v = length * i + j
                self.edges[(v,v-length)] = random.randint(0,99)
        for i in range(height):
            for j in range(1,length):
                v = length * i + j
                self.edges[(v,v-1)] = random.randint(0,99)
        return