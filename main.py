import pygame
import numpy as np
import math
import os
import random

WIDTH, HEIGHT = 800, 680
TITLE = "3d Engine"
FPS = 144

from environment import Environment
from vector3 import Vector3
from camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        
        pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
        camera_pos = Vector3(0,0,0)
        cam = Camera((WIDTH, HEIGHT))
        
        self.world = Environment(cam, (0,0,0))
        
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

        self.move_speed = 0.02

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # Controls update speed (FPS per second)
            self.events()
            self.update()
            self.draw()

    def close(self):
        pygame.quit()
        quit()

    def update(self):
        
        mx, my = pygame.mouse.get_pos()
        pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
        pygame.mouse.set_visible(False)

        # caption
        pygame.display.set_caption(f"{TITLE} | Speed {round(self.move_speed,2)}")

        cam = self.world.camera
        cam.rotation.y -= (WIDTH//2 - mx) / 300
        cam.rotation.x -= (HEIGHT//2 - my) / 300      
        
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
                
        keys = pygame.key.get_pressed()
        
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

    def draw(self):
        self.screen.fill(self.world.color)
        cam = self.world.camera
        
        for obj in self.world.get_points():
            break
            for point in obj:
                output = cam.orient_vector(point)
                x, y, z = int(output[0]), int(output[1]), output[2]
                if z > 0:
                    size = 10
                    dist = cam.global_pos.distance(point)
                    
                    if int(size/dist) == 0:
                        if x > 0 and x < WIDTH and y > 0 and y < HEIGHT:
                            self.screen.set_at((x, y), (255,255,255))
                    else:
                        pygame.draw.circle(self.screen, (255,255,255), (x, y), int(size/dist))
        
        lines = self.world.get_lines() 
        for shape in lines:
            break
            for pair in shape:
                point_a = cam.orient_vector(pair[0])
                point_b = cam.orient_vector(pair[1])
                
                x_a, y_a, z_a = int(point_a[0]), int(point_a[1]), point_a[2]
                x_b, y_b, z_b = int(point_b[0]), int(point_b[1]), point_b[2]
                if z_a > 0 and z_b > 0:
                    pygame.draw.line(self.screen, (235,235,235), (x_a, y_a), (x_b, y_b), 1)
        
        
        for face in self.world.objects['axis']['faces']:
            break
            points_in_face = []
            avg_point = Vector3(0,0,0)
            for point in face:
                vec = self.world.objects['axis']['points'][point]
                output = cam.orient_vector(vec)
                x, y, z = int(output[0]), int(output[1]), output[2]
                points_in_face.append((int(x), int(y)))
                avg_point += output
                
            avg_point /= len(points_in_face)
            if abs(avg_point.z) > self.world.poly_clip_dist:
                pygame.draw.polygon(self.screen, (0,0,255), points_in_face)
                
        
        for obj in self.world.objects:
            points, lines, faces = self.world.draw_object(id_='axis',config={'points':True, 'lines':True, 'faces':True} )
        
            faces = sorted(faces, key=lambda x: x[1], reverse=True)
            q =0 
            for face in faces:
                if face[2] == True:
                    poly = face[0]
                    
                    if q == 0:
                        col = (255,0,0)
                    else:
                        col = (0,255,255)
                    pygame.draw.polygon(self.screen, col, poly)
                q += 1
                    
            for line in lines:
                start = line[0]
                end = line[1]
                
                if start[2] > 0 and end[2] > 0:
                    pygame.draw.line(self.screen, (235,235,235), (start[0], start[1]), (end[0], end[1]), 1)
                    
            for point in points:                    
                x, y, z = int(point[0]), int(point[1]), point[2]
                if z > 0:
                    size = 10
                    pygame.draw.circle(self.screen, (255,255,255), (x, y), int(size))
                    
            
        

            
                
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


# create the game object
g = Game()
g.new()
g.run()