from vector3 import Vector3
from collections import namedtuple
from math import sqrt

class Environment(object):
    
    def __init__(self, camera, light, color):
        
        self.color = color
        self.camera = camera
        self.light_source = light
        
        self.objects = {}
        
        self.debug = False
        
        #* Suggested distance at which polygons should stop rendering
        self.poly_clip_dist = 0.4 
        
        
    def add_object(self, id_, points : [Vector3], lines : dict = None, faces : list = None, mesh= None):
        
        if id_ in self.objects:
            if self.objects[id_] != None:
                raise Exception("object already exists!")
            
        self.objects[id_] = {
            "id_" : id_,
            "points" : points,
            "lines" : lines,
            "faces" : faces,
            "mesh" : mesh
        }

    def remove_object(self, id_):
        if id_ in self.objects:
            self.objects.pop(id_)
            return True
        else:
            return False

    def draw_object(self, id_, config : dict):
        '''
        Return point, line, and face data to draw an object
        '''
        
        #* config information
        # {'points':bool, 'lines':bool, 'faces':bool}   
        
        if self.camera == None:
            raise AttributeError("Camera not specified!}")
        
        obj = self.objects[id_]
        perspective_points = []

        cam = self.camera
        c_x, c_y, c_z = cam.global_pos
        
        lines = []
        points = []
        faces = []
    
        perspective_points = [ self.camera.orient_vector(point) for point in obj['points']]     
        if config['points']:
            points = perspective_points
        
        
        
        # Get draw lines
        if config['lines']:
            for startpoint in obj['lines']:
                    for endpoint in obj['lines'][startpoint]:  
                        
                        a_x, a_y, a_z, _ = perspective_points[startpoint]
                        b_x, by_, b_z, _ = perspective_points[endpoint]
                        
                        if a_z > 0 and b_z > 0:
                            lines.append(
                                ((a_x, a_y, a_z), (b_x, by_, b_z))
                            )
        
        if config['faces']:
            ind = 0
            for face in obj['faces']:

                avg_x = 0
                avg_y = 0
                avg_z = 0
                avg_z_depth = 0
                for index in face:
                    avg_x += obj['points'][index].x
                    avg_y += obj['points'][index].y
                    avg_z += obj['points'][index].z
                    avg_z_depth += perspective_points[index][2] + obj['points'][index].z

                f_size = len(face)
                avg_x /= f_size
                avg_y /= f_size
                avg_z /= f_size
                
                distance_from_cam = -sqrt( (avg_z-c_z)**2 )
                if config['lighting']:
                    c_out = self.light_source.in_rad((avg_x, avg_y, avg_z))
                else:
                    c_out = [0,0,0]

                if avg_z_depth > self.poly_clip_dist:
                    faces.append(
                        ([(perspective_points[i][0], perspective_points[i][1]) for i in face], 
                         distance_from_cam, 
                         ind, 
                         (avg_x, avg_y, avg_z),
                         c_out
                        ))
                
                ind += 1
                
        return points, lines, faces
        
    def get_points(self) -> [[Vector3]]:
        '''
        Returns a list of all points.
        List is structured by object
        '''
        
        all_points = [self.objects[id_]['points'] for id_ in self.objects]
        return all_points
        
    def get_lines(self) -> [[Vector3]]:
        '''
        Returns a list of all lines.
        List is structured by object
        '''
        
        all_lines = []

        for id_ in self.objects:
            obj_ = []
            for startpoint in self.objects[id_]['lines']:
                for endpoint in self.objects[id_]['lines'][startpoint]:
                    obj_.append(
                        (self.objects[id_]['points'][startpoint], self.objects[id_]['points'][endpoint])
                    )
            all_lines.append(obj_)
            
        return all_lines