from math import sqrt, sin, cos
import numpy as np

class Vector3(object):
    
    def __init__(self, x : float, y : float, z : float):
        self.raw = np.array([float(x), y, z, 1.0])

    @property
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    @property
    def x(self):
        return self.raw[0]
    
    @property
    def y(self):
        return self.raw[1]
    
    @property
    def z(self):
        return self.raw[2]
    
    @x.setter
    def x(self, val):
        self.raw[0] = val
    
    @y.setter
    def y(self, val):
        self.raw[1] = val
    
    @z.setter
    def z(self, val):
        self.raw[2] = val
    
    def __add__(self, other):
        
        if isinstance(other, Vector3):
            return Vector3(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )
        elif isinstance(other, np.ndarray):
            self.raw += other
            return self
        else:
            raise NotImplementedError
        
    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z
            )
        elif isinstance(other, np.ndarray):
            self.raw -= other
            return self
        else:
            raise NotImplementedError
        
    def __mul__(self, other):
        if isinstance(other, Vector3):
            # TODO: should this be changed?
            return self.matmul(other)
        elif isinstance(other, np.ndarray):
            self.raw *= other
            return self
        elif isinstance(other, (int, float)):
            return Vector3(
                self.x * other,
                self.y * other,
                self.z * other
            )
        else:
            raise NotImplementedError
        
    def __truediv__(self, other):
        if isinstance(other, np.ndarray):
            self.raw /= other
            return self
        elif isinstance(other, (int, float)):
            return Vector3(
                self.x / other,
                self.y / other,
                self.z / other
            )
        else:
            raise NotImplementedError
        
    def dot(self, other) -> float:
        return (self.x*other.x) + (self.y*other.y) + (self.z*other.z)
    
    def matmul(self, other):
        product = np.matmul(self.raw, other.raw)
        return Vector3(product[0], product[1], product[2])
    
    def rotate(self, angle):
        
        sin_x = sin(angle.x)
        cos_x = cos(angle.x)
        rotation_x_matrix = [
            [1, 0, 0, 0],
            [0, cos_x, -sin_x, 0],
            [0, sin_x, cos_x, 0],
            [0, 0, 0, 1.0]
        ]
        
        sin_y = sin(angle.y)
        cos_y = cos(angle.y)
        rotation_y_matrix = [
            [cos_y, 0, sin_y, 0],
            [0, 1, 0, 0],
            [-sin_y, 0, cos_y, 0],
            [0, 0, 0, 1.0]
        ]
        
        sin_z = sin(angle.z)
        cos_z = cos(angle.z)
        rotation_z_matrix = [
            [cos_z, -sin_z, 0, 0],
            [sin_z, cos_z, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1.0]
        ]
        
        rotation_x_matrix = np.array(rotation_x_matrix)
        rotation_y_matrix = np.array(rotation_y_matrix)
        rotation_z_matrix = np.array(rotation_z_matrix)
        
        result = np.matmul(rotation_x_matrix, self.raw)
        result = np.matmul(rotation_y_matrix, result)
        result = np.matmul(rotation_y_matrix, result)
        
        self.raw = result
    
    def normalize(self):
        length = self.magnitude
        if self.x != 0:
            self.x /= length
        if self.y != 0:
            self.y /= length
        if self.z != 0:
            self.z /= length

    def distance(self, other) -> float:

        if isinstance(other, Vector3):
            dist = sqrt(
                (self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2
            )
        elif isinstance(other, np.ndarray):
            dist = sqrt(
                (self.x-other[0])**2 + (self.y-other[1])**2 + (self.z-other[2])**2
            )
        else:
            raise NotImplementedError
        return dist

    def set_as(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z + 0.00001

    def copy(self):
        return Vector3(self.x, self.y, self.z)
    
    def __iter__(self):
        return iter( (self.x, self.y, self.z) )
    
    def __repr__(self):
        return f"<Vector3 x={self.raw[0]}, y={self.raw[1]}, z={self.raw[2]}>"
    
    @classmethod
    def average_vector(cls, vectors : list):
        
        sum_ = Vector3(0,0,0)
        for v in vectors:
            sum_ += v
        
        avg_ = sum_ / len(vectors)
        
        return avg_
    
if __name__ == '__main__':
    a = Vector3(1,2,3)
    b = Vector3(3,2,1)
