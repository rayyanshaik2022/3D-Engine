import pyglet
from pyglet.window import key

print(pyglet)
import numpy as np
import math
import os
import random
from mesh import *

from environment import Environment
from vector3 import Vector3
from camera import Camera


WIDTH, HEIGHT = 800, 600

camera_pos = Vector3(0,0,0)
cam = Camera((WIDTH, HEIGHT))

world = Environment(cam, (255,255,255))

scale = 1

world.add_object(
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

a = MeshReader()
mesh = a.read("objects/low_sphere.obj", scale=1)

world.add_object(
    "cube",
    mesh.vertices,
    lines=mesh.generate_line(),
    faces=mesh.faces
)


move_speed = 0.02
        

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_exclusive_mouse(True)
batch = pyglet.graphics.Batch()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.R:
        print("Resetting position ...")
        world.camera.global_pos.set_as(0,0,0)
        world.camera.rotation.set_as(0,0,0)

@window.event
def on_draw():
    
    # udpates here
    
    window.set_caption(str(pyglet.clock.get_fps()))
    # draw
    window.clear()
    
    
    batch.draw()
    
    # ported
    bg = pyglet.shapes.Rectangle(0, 0, WIDTH, HEIGHT, color=world.color, batch=batch)
    cam = world.camera      
    
    for obj in world.objects:
        
        if obj != 'axis':
            pass
        
        points, lines, faces = world.draw_object(id_=obj,config={'points':False, 'lines':True, 'faces':True} )

        faces = sorted(faces, key=lambda x: x[1], reverse=True)

        for face in faces:
            if face[2] == True:
                poly = face[0]
                
                flag = True
                for point in poly:
                    if not (point[0] > 0 and point[1] < WIDTH):
                        flag = False
                
                if flag:
                    continue
                    ppoly = pyglet.shapes.Polygon(poly, color=(0,0,255), batch=batch)

            
        for line in lines:
            start = line[0]
            end = line[1]
            
            flag = True
            for point in (start, end):
                if not (point[0] > 0 and point[1] < WIDTH):
                    flag = False
            
            if flag:
                pyglet.shapes.Line(start[0], end[0], start[1], end[1], 1, color=(100,100,100), batch=batch)
                #pygame.draw.line(self.screen, (100,100,100), (start[0], start[1]), (end[0], end[1]), 1)
            
        for point in points:            
            x, y, z = int(point[0]), int(point[1]), point[2]
            if z > 0:
                if (x > 0 and x < WIDTH) and (y > 0 and y < HEIGHT):
                    size = 5
                    
                    pyglet.shapes.Circle(x, y, radius, segments=None, color=(0,0,0), batch=batch)
                    #pygame.draw.circle(self.screen, (0,0,0), (x, y), int(size))
    

@window.event
def on_mouse_motion(x, y, dx, dy):
    cam = world.camera
    cam.rotation.y -= (WIDTH//2 - dx) / 300
    cam.rotation.x -= (HEIGHT//2 - dy) / 300

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
                
pyglet.app.run()