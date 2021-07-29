from vector3 import Vector3
from collections import namedtuple

ConvertedVertex = namedtuple('ConvertedVertex',['vector','xyz'])

class Environment(object):
    
    def __init__(self, camera, color):
        
        self.color = color
        self.camera = camera
        
        self.objects = {}
        
        self.debug = False
        
        #* Suggested distance at which polygons should stop rendering
        self.poly_clip_dist = 0.4 
        
    def add_object(self, id_, points : [Vector3], lines : dict = None, faces : list = None):
        
        if id_ in self.objects:
            if self.objects[id_] != None:
                raise Exception("object already exists!")
            
        self.objects[id_] = {
            "id_" : id_,
            "points" : points,
            "lines" : lines,
            "faces" : faces
        }
     
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
        
        lines = []
        points = []
        faces = []
        
        for point in obj['points']:
            
            vec = Vector3(0,0,0)
            output = self.camera.orient_vector(point)
            vec.raw = output
            
            x, y, z = int(output[0]), int(output[1]), output[2]
            
            perspective_points.append(
                ConvertedVertex(vec, (x,y,z))
            )
            
            if config['points']:
                points.append((x,y,z))
        
        
        # Get draw lines
        if config['lines']:
            for startpoint in obj['lines']:
                    for endpoint in obj['lines'][startpoint]:  
                        
                        if perspective_points[startpoint].xyz[2] > 0 and perspective_points[endpoint].xyz[2] > 0:
                            lines.append(
                                (perspective_points[startpoint].xyz, perspective_points[endpoint].xyz)
                            )
        
        if config['faces']:
            for face in obj['faces']:
                
                # Position accounting for camera view/rotation
                vector_list2 = [perspective_points[x].vector for x in face]
                avg_vector2 = Vector3.average_vector(vector_list2)
                
                if abs(avg_vector2.z) < self.poly_clip_dist:
                    continue
                
                # Position to camera raw world position
                vector_list1 = [obj['points'][x] - self.camera.global_pos for x in face]
                avg_vector1 = Vector3.average_vector(vector_list1)
                
                draw_list = [perspective_points[i].xyz for i in face]
                distance_from_cam = self.camera.global_pos.distance(avg_vector1)
                
                all_points_past_cam_z = True
                for point in draw_list:
                    if point[2] <= 0:
                        all_points_past_cam_z = False
                        break
                
                faces.append(([(int(x),int(y)) for x, y, z in draw_list], distance_from_cam, all_points_past_cam_z))
        
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