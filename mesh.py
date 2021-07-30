import numpy as np
import math
from vector3 import Vector3
import re
import random
from pygame import Color
import random

class Mesh(object):
    def __init__(self, name, vertices, faces):
        
        self.name = name
        self.vertices = vertices
        self.line = []
        self.faces = faces
        
        self.poly_palette = {}
        
    def translate(self, vec):
    
        if isinstance(vec, Vector3):
            for i in range(len(self.vertices)):
                self.vertices[i] += vec
        elif isinstance(vec, tuple):
            add_vec = Vector3(*vec)
            for i in range(len(self.vertices)):
                self.vertices[i] += add_vec
    
    def scale(self, mag):
        for i in range(len(self.vertices)):
                self.vertices[i] *= mag
    
    def generate_line(self):
        
        lines = {}
        
        for i in range(len(self.vertices)-1):
            lines[i] = [i+1]
        lines[len(self.vertices)-1] = [0]
        
        return lines
    
    def generate_random_colors(self, size=5):
        base = Color(242, 200, 82)
        h, s, v, a = base.hsva
        
        for i in range(size):
            h = random.random() * 20
            base.hsva = (h,s,v,a)
            self.poly_palette[i] = (base.r, base.g, base.b)
        
        return self.poly_palette
    
class MeshReader(object):
    
    def __init__(self):
        pass
    
    def read(self, file, scale=1):
        
        if ".obj" not in file:
            raise NotImplementedError
        
        name = None
        vertices = []
        faces = []
        
        
        with open(file) as f:
            for line in f:

                contents =  re.sub(' +', ' ', line.strip()).split(" ")
                if contents[0] == "o":
                    name = contents[1]
                if contents[0] == "v":
                    vertices.append(
                        Vector3(
                            float(contents[1]), float(contents[2]), float(contents[3])
                        ) * scale
                    )
                if contents[0] == "f":
                    
                    points = [int(x.split("/")[0])-1 for x in contents[1:]] # by index (-1 bc .obj index starts at 1)
                    
                    faces.append(
                        points
                    )
                    
        return Mesh(name, vertices, faces)


if __name__ == '__main__':
    
    a = MeshReader()
    mesh = a.read("objects/cube.obj")
    
    mesh.generate_random_colors(3)
    
    print(mesh.generate_line())
    print(mesh.generate_random_colors())