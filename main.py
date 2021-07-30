import pygame
import numpy as np
import math
import os
import random
from mesh import *

#* Constants
WIDTH, HEIGHT = 800, 680
TITLE = "3d Engine"
FPS = 144

from environment import Environment
from vector3 import Vector3
from camera import Camera
from light import Light

class Gui:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.set_alpha(None)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def initialize(self):
        pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
        self.mesh_reader = MeshReader()
        
        self.initialize_environment()
        self.initialize_objects()
    
    def initialize_environment(self):
        
        camera_pos = Vector3(0,0,20*1)
        camera = Camera((WIDTH, HEIGHT))
        camera.global_pos = camera_pos
        
        light = Light(Vector3(0,0,0), (100,150,100), 5, 30)

        self.world = Environment(camera, light, (0,0,0))
        self.world.poly_clip_dist = 0.65
        
        self.move_speed = 0.02

    def initialize_objects(self):
        
        scale = 1
        
        self.world.add_object(
            "axis",
            [
                Vector3(0,0,0) * scale,
                Vector3(0,0,1) * scale,
                Vector3(1,0,0) * scale,
                Vector3(0,1,0) * scale
            ], 
            {
                0 : [1, 2, 3]
            },
            [
                [1, 0, 3],
                [2, 0, 3]
            ]
        )
        self.world.remove_object("axis")

        
        mesh = self.mesh_reader.read(os.path.dirname(os.path.realpath(__file__))+"/objects/amongus.obj", scale=scale)
        mesh.generate_random_colors(10)
        mesh.scale(0.25)
    
        self.world.add_object(
            "amongus",
            mesh.vertices,
            lines=mesh.generate_line(),
            faces=mesh.faces,
            mesh=mesh
        )  
        

    def run(self):
        self.playing = True
        
        self.initialize()
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # Controls update speed (FPS per second)
            self.events()
            self.update()
            self.draw()

    def close(self):
        pygame.quit()
        quit()

    def update_controls(self):
        self.mx, self.my = pygame.mouse.get_pos()
        pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
        pygame.mouse.set_visible(False)
        
        keys = pygame.key.get_pressed()
        cam = self.world.camera
        
        if keys[pygame.K_w]:
            
            forward = cam.forward_vector()
            cam.global_pos += forward * self.move_speed
        
        if keys[pygame.K_s]:
            
            forward = cam.forward_vector()
            cam.global_pos -= forward * self.move_speed
            
        if keys[pygame.K_d]:
            
            forward = cam.forward_vector(adjust=90, channel=1)
            cam.global_pos += forward * self.move_speed
            
        if keys[pygame.K_a]:
            
            forward = cam.forward_vector(adjust= -90, channel=1)
            cam.global_pos += forward * self.move_speed
            
        if keys[pygame.K_SPACE]:
        
            cam.global_pos.y += self.move_speed
        
        if keys[pygame.K_LSHIFT]:
            
            cam.global_pos.y -= self.move_speed

        if keys[pygame.K_o]:

            self.move_speed *= 1.1
        
        if keys[pygame.K_p]:

            self.move_speed /= 1.1
        
    def update(self):
        
        self.update_controls()
        
        # caption
        pygame.display.set_caption(f"{TITLE} | Speed {round(self.move_speed,2)} | Fps {round(self.clock.get_fps(),2)}")
    
        cam = self.world.camera
        cam.rotation.y -= (WIDTH//2 - self.mx) / 300
        cam.rotation.x -= (HEIGHT//2 - self.my) / 300
    
        # clamp up and down rotation view
        rot_x_deg = math.degrees(cam.rotation.x) % 360
        rot_x_deg_prime = 360 - rot_x_deg
        if rot_x_deg_prime > 65 and rot_x_deg_prime < 295:
            dist_65 = abs(rot_x_deg_prime-65)
            dist_295 = abs(rot_x_deg_prime-295)
            if dist_65 < dist_295:
                cam.rotation.x = math.radians(295)
            else:
                cam.rotation.x = math.radians(65)
            
    
    def draw(self):
        self.screen.fill(self.world.color)
        cam = self.world.camera      
        cam.orient_matrixes()

        distance_to_center = cam.global_pos.distance(Vector3(0,0,0))
        self.world.light_source.pos = cam.global_pos
        
        for obj in self.world.objects:
            
            if obj != 'axis':
                pass
            
            config = {'points':False, 'lines':False, 'faces':True, 'lighting':False}
            
            points, lines, faces = self.world.draw_object(id_=obj,config=config)

            faces = sorted(faces, key=lambda x: x[1], reverse=False)
            if self.world.objects[obj]['mesh'] != None:
                color_size = len(self.world.objects[obj]['mesh'].poly_palette)
            else:
                color_size = -1

            for face in faces:
                poly = face[0]
                
                flag = True
                for point in poly:
                    if not (point[0] > 0 and point[1] < WIDTH):
                        flag = False
                
                if flag:
                    if color_size == -1:
                        color = [130, 130, 130]
                    else:
                        color = list(self.world.objects[obj]['mesh'].poly_palette[face[2]%color_size])
                    
                    additive_color = face[4]
                    color[0] =  min((additive_color[0] + color[0], 255))
                    color[1] = min((additive_color[1] + color[1], 255))
                    color[2] = min((additive_color[2] + color[2], 255))
    
                    pygame.draw.polygon(self.screen, color , poly)
                
                
            for line in lines:
                start = line[0]
                end = line[1]
                
                flag = True
                for point in (start, end):
                    if not (point[0] > 0 and point[1] < WIDTH):
                        flag = False
                
                if flag:
                    pygame.draw.line(self.screen, (100,100,100), (start[0], start[1]), (end[0], end[1]), 1)
              
            for point in points:            
                x, y, z = int(point[0]), int(point[1]), point[2]
                if z > 0:
                    if (x > 0 and x < WIDTH) and (y > 0 and y < HEIGHT):
                        size = 20
                        pygame.draw.circle(self.screen, (0,0,0), (x, y), int(size/z)+1)
                
                
        pygame.display.flip()

    def events(self):
        # catch all events here
        
        cam = self.world.camera
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_r:
                    print("Resetting position ...")
                    cam.global_pos.set_as(0,0,0)
                    cam.rotation.set_as(0,0,0)
                if event.key == pygame.K_t:
                    
                    a = cam.global_pos
                    b = Vector3(0,0,0)

                    distance = a.distance(b)
                    print(f"Distance to center: {round(distance, 3)}")

# create the gui object
if __name__ == '__main__':
    g = Gui()
    g.run()