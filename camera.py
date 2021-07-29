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
        
        self.projection_matrix = np.array([
            [5, 5, 0, 0],
            [0, 5, 0, 0],
            [0, 0, -1, 0], 
            [0, 0, 0, 1.0]
        ])
        
        self.local_translation_matrix = np.array([
            [1, 0, 0, 5],
            [0, 1, 0, 5], 
            [0, 0, 1, 5], 
            [0, 0, 0, 1.0]
        ])
        
        self.global_translation_matrix = np.array([
            [1, 0, 0, 5],
            [0, 1, 0, 5], 
            [0, 0, 1, 5], 
            [0, 0, 0, 1.0]
        ])
        
        self.rotation_x_matrix = np.array([
            [1, 0, 0, 0],
            [0, 5, 5, 0],
            [0, 5, 5, 0],
            [0, 0, 0, 1.0]
        ])
        
        self.rotation_y_matrix = np.array([
            [5, 0, 5, 0],
            [0, 1, 0, 0],
            [5, 0, 5, 0],
            [0, 0, 0, 1.0]
        ])
    
        self.rotation_z_matrix = np.array([
            [5, 5, 0, 0],
            [5, 5, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1.0]
        ])
        
        self.offset_matrix = np.array([
            [ 1, 0, 0, 5 ],
            [ 0, -1, 0, 5 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1.0 ]
        ])
        
        self.perspective_matrix = np.array([
            [5, 0, 0, 0],
            [0, 5, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1.0]
        ])
        
    def orient_vector(self, point, z=False):
        
        self.projection_matrix[0][0] = (self.focal_length * self.pixelX) / (2 * self.sensorX)
        self.projection_matrix[0][1] = self.skew
        self.projection_matrix[1][1] = (self.focal_length * self.pixelY) / (2 * self.sensorY)

        self.local_translation_matrix[0][3] = -self.local_pos.x
        self.local_translation_matrix[1][3] = -self.local_pos.y
        self.local_translation_matrix[2][3] = -self.local_pos.z
        
        self.global_translation_matrix[0][3] = -self.global_pos.x
        self.global_translation_matrix[1][3] = -self.global_pos.y
        self.global_translation_matrix[2][3] = -self.global_pos.z
        
        
        
        sin_x = sin(self.rotation.x)
        cos_x = cos(self.rotation.x)
        self.rotation_x_matrix[1][1] = cos_x
        self.rotation_x_matrix[1][2] = -sin_x
        self.rotation_x_matrix[2][1] = sin_x
        self.rotation_x_matrix[2][2] = cos_x
        
        sin_y = sin(self.rotation.y)
        cos_y = cos(self.rotation.y)
        self.rotation_y_matrix[0][0] = cos_y
        self.rotation_y_matrix[0][2] = sin_y
        self.rotation_y_matrix[2][0] = -sin_y
        self.rotation_y_matrix[2][2] = cos_y
        
        sin_z = sin(self.rotation.z)
        cos_z = cos(self.rotation.z)
        self.rotation_z_matrix[0][0] = cos_z
        self.rotation_z_matrix[0][1] = -sin_z
        self.rotation_z_matrix[1][0] = sin_z
        self.rotation_z_matrix[1][1] = cos_z
        
        self.offset_matrix[0][3] = self.offsetX
        self.offset_matrix[1][3] = self.offsetY
        
        
        result = np.matmul(self.global_translation_matrix, point.raw)
        
        if z:
            result = np.matmul(self.rotation_z_matrix, result)
        
        result = np.matmul(self.rotation_y_matrix, result)
        
        result = np.matmul(self.rotation_x_matrix, result)
        
        #result = np.matmul(self.local_translation_matrix, result)
        
        result = np.matmul(self.projection_matrix, result)
        
        # gives depth scaling
        self.perspective_matrix[0][0] = 1/result[2]
        self.perspective_matrix[1][1] = 1/result[2]
        
        result = np.matmul(self.perspective_matrix, result)
        result = np.matmul(self.offset_matrix, result)
        
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