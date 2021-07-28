from math import sin, cos, sqrt, degrees, radians
import numpy as np
from vector3 import Vector3


class Camera(object):
    
    def __init__(self, dim):
        
        self.global_pos = Vector3(0,0,5)
        self.rotation = Vector3(0,0,0)
        self.local_pos = Vector3(0,0,0)
        
        self.focal_length = 0.1
        self.pixelX = dim[0]
        self.pixelY = dim[1]
        self.sensorX = dim[0] / 10000
        self.sensorY = dim[1] / 10000
        
        self.offsetX = dim[0] / 2
        self.offsetY = dim[1] / 2
        self.skew = 0
    
    def orient_vector(self, point):

        projection_matrix = [
            [(self.focal_length * self.pixelX) / (2 * self.sensorX), self.skew, 0, 0],
            [0, (self.focal_length * self.pixelY) / (2 * self.sensorY), 0, 0],
            [0, 0, -1, 0], 
            [0, 0, 0, 1.0]
        ]

        local_translation_matrix = [
            [1, 0, 0, -self.local_pos.x],
            [0, 1, 0, -self.local_pos.y], 
            [0, 0, 1, -self.local_pos.z], 
            [0, 0, 0, 1.0]
        ]
        
        global_translation_matrix = [
            [1, 0, 0, -self.global_pos.x],
            [0, 1, 0, -self.global_pos.y], 
            [0, 0, 1, -self.global_pos.z], 
            [0, 0, 0, 1.0]
        ]
        
        sin_x = sin(self.rotation.x)
        cos_x = cos(self.rotation.x)
        rotation_x_matrix = [
            [1, 0, 0, 0],
            [0, cos_x, -sin_x, 0],
            [0, sin_x, cos_x, 0],
            [0, 0, 0, 1.0]
        ]
        
        sin_y = sin(self.rotation.y)
        cos_y = cos(self.rotation.y)
        rotation_y_matrix = [
            [cos_y, 0, sin_y, 0],
            [0, 1, 0, 0],
            [-sin_y, 0, cos_y, 0],
            [0, 0, 0, 1.0]
        ]
        
        sin_z = sin(self.rotation.z)
        cos_z = cos(self.rotation.z)
        rotation_z_matrix = [
            [cos_z, -sin_z, 0, 0],
            [sin_z, cos_z, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1.0]
        ]
        
        offset_matrix = [
            [ 1, 0, 0, self.offsetX ],
            [ 0, -1, 0, self.offsetY ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1.0 ]
        ]
        
        global_translation_matrix = np.array(global_translation_matrix)
        rotation_z_matrix = np.array(rotation_z_matrix)
        rotation_y_matrix = np.array(rotation_y_matrix)
        rotation_x_matrix = np.array(rotation_x_matrix)
        local_translation_matrix = np.array(local_translation_matrix)
        offset_matrix = np.array(offset_matrix)
        
        result = np.matmul(global_translation_matrix, point.raw)
        
        result = np.matmul(rotation_z_matrix, result)
        
        result = np.matmul(rotation_y_matrix, result)
        
        result = np.matmul(rotation_x_matrix, result)
        
        result = np.matmul(local_translation_matrix, result)
        
        result = np.matmul(projection_matrix, result)
        
        
        
        # gives depth scaling
        perspective_matrix = [
            [1/result[2], 0, 0, 0],
            [0, 1/result[2], 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        perspective_matrix = np.array(perspective_matrix)
        
        result = np.matmul(perspective_matrix, result)
        result = np.matmul(offset_matrix, result)
        
        return result
    
    def forward_vector(self, adjust=0, channel=0):
        
        #* channel
        # 0 = y rotation plane and x rotation plane
        # 1 = y rotation plane
        # 2 = x rotation plane
        
        rot = self.rotation
        x_deg, y_deg, z_deg = degrees(rot.x) % 360, degrees(rot.y) % 360, degrees(rot.z) % 360
        
        movement_vector = Vector3(0,0,0)
        
        if channel != 2:
            movement_vector.z += -cos(radians(y_deg + adjust))
            movement_vector.x += sin(radians(y_deg + adjust))
    
        x_deg_prime = 360 - x_deg - adjust
        
        if channel != 1:
            #movement_vector.z += -cos(radians(x_deg_prime)) * move_speed
            movement_vector.y += sin(radians(x_deg_prime))
        
        movement_vector.normalize()
        return movement_vector