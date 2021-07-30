from vector3  import Vector3
from math import sqrt

class Light(object):
    
    def __init__(self, pos : Vector3, color : tuple, intensity : float, rad : float):
        
        self.pos = pos
        self.color = color
        self.intensity = intensity
        self.rad = rad
    
    def in_rad(self, point : tuple) -> list:

        # point is tuple not vector for efficiency
        # (x, y, z)
        
        point_color = [0,0,0]
        
        lx, ly, lz = self.pos
        dist = sqrt( (point[0]-lx)**2 + (point[1]-ly)**2 + (point[2]-lz)**2 )
        
        if dist < self.rad:
            percent_intensity = self.intensity / (dist**2)
            point_color[0] += self.color[0] * percent_intensity
            point_color[1] += self.color[1] * percent_intensity
            point_color[2] += self.color[2] * percent_intensity
        
        return point_color