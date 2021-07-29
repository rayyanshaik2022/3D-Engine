import numpy as np
import math
from vector3 import Vector3
import re

class Mesh(object):
    def __init__(self, name, vertices, faces):
        
        self.name = name
        self.vertices = vertices
        self.line = []
        self.faces = faces
    
    def generate_line(self):
        
        lines = {}
        
        for i in range(len(self.vertices)-1):
            lines[i] = [i+1]
        lines[len(self.vertices)-1] = [0]
        
        return lines
    
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
    
    print(mesh.generate_line())