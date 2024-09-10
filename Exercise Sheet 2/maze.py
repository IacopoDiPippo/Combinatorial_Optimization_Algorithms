# Importing libraries
import random
import math
from datetime import datetime
from processing_py import *

# Defining the Maze class
class Maze:

    # Defining the constructor
    def __init__(self, block_size, height, length):
        self.length = length
        self.height = height
        self.block_size = block_size
        self.margin_size = 2 * self.block_size
        self.maze_length = (2*length + 1)*self.block_size
        self.maze_height = (2*height + 1)*self.block_size
        self.bg_color = [100,100,140] # rgb
        self.maze_color = [200,200,100] #rgb
        return
    
    def update(self):
        self.app.redraw() # refresh the window
        return
    
    def start(self):
        self.app = App(self.maze_length + 2*self.margin_size, self.maze_height + 2*self.margin_size) # create window: width, height
        self.app.background(self.bg_color[0],self.bg_color[1],self.bg_color[2]) # set background:  red, green, blue
        self.app.fill(self.maze_color[0],self.maze_color[1],self.maze_color[2]) # set color for objects: red, green, blue
        self.app.rect(self.margin_size, self.margin_size, self.maze_length, self.maze_height) # draw a rectangle: x0, y0, size_x, size_y
        self.create_exits()
        return
    
    def block_of_vertex(self,vertex):
        first_block = [self.margin_size + self.block_size, self.margin_size + self.block_size]
        block = [2 * (vertex % self.length) * self.block_size + first_block[0],
                 2 * math.floor(vertex / self.length) * self.block_size + first_block[1]]
        return block

    def block_of_edge(self,vertex_1,vertex_2):
        block_vertex_1 = self.block_of_vertex(vertex_1)
        block_vertex_2 = self.block_of_vertex(vertex_2)
        block = [(block_vertex_1[0] + block_vertex_2[0]) / 2, (block_vertex_1[1] + block_vertex_2[1]) / 2]
        return block

    def include_vertex(self, vertex):
        block = self.block_of_vertex(vertex)
        self.app.fill(self.bg_color[0],self.bg_color[1],self.bg_color[2]) # set color for objects: red, green, blue
        self.app.rect(block[0], block[1], self.block_size, self.block_size) # draw a rectangle: x0, y0, size_x, size_y
        return

    def include_edge(self,vertex_1,vertex_2,weight):
        block = self.block_of_edge(vertex_1,vertex_2)
        self.app.fill(self.bg_color[0],self.bg_color[1],self.bg_color[2]) # set color for objects: red, green, blue
        self.app.rect(block[0], block[1], self.block_size, self.block_size) # draw a rectangle: x0, y0, size_x, size_y
        self.app.textSize(self.block_size/2)
        self.app.fill(0, 408, 612)
        self.app.text(str(weight), block[0] + 1/5 * self.block_size, block[1] + 2/3 * self.block_size)
        return

    def create_exits(self):
        exit_1 = [self.margin_size + self.block_size, self.margin_size]
        exit_2 = [self.margin_size + self.maze_length - 2 * self.block_size, self.margin_size + self.maze_height - self.block_size]
        self.app.fill(self.bg_color[0],self.bg_color[1],self.bg_color[2]) # set color for objects: red, green, blue
        self.app.rect(exit_1[0], exit_1[1], self.block_size, self.block_size) # draw a rectangle: x0, y0, size_x, size_y
        self.app.fill(self.bg_color[0],self.bg_color[1],self.bg_color[2]) # set color for objects: red, green, blue
        self.app.rect(exit_2[0], exit_2[1], self.block_size, self.block_size) # draw a rectangle: x0, y0, size_x, size_y
        return

    def draw_animated(self,edges):
        self.start()
        edge_list = list(edges.items())

        for edge in edge_list:
            v1 = edge[0][0]
            v2 = edge[0][1]
            weight = edge[1]
            self.include_vertex(v1)
            self.update()
            self.include_vertex(v2)
            self.update()
            self.include_edge(v1,v2,weight)
            self.update()
        self.update()
        input()
        self.close()
        return
    
    def draw_final(self,edges):
        self.start()
        edge_list = list(edges.items())
        for edge in edge_list:
            weight = edge[1]
            v1 = edge[0][0]
            v2 = edge[0][1]
            self.include_vertex(v1)
            self.include_vertex(v2)
            self.include_edge(v1,v2,weight)
        self.update()
        input()
        self.close()
        return

    def close(self):
        self.app.exit()
        return