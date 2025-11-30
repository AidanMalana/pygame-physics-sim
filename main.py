import sys, pygame
from pygame.math import Vector2
from typing import List

pygame.init()

pygame.display.set_caption('Verlet Integration Simulation')
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

running = True
dt = 0
clock = pygame.time.Clock()

GRAVITY = Vector2(0, 600)

container = {"position": Vector2(screen.width / 2, screen.height / 2), "radius": 340}

class VerletObject:
    def __init__(self, p_current: Vector2, vel: Vector2, mass, radius, color):
        self.p_current = p_current
        self.accel = Vector2()
        self.accel.xy = 0, 0
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.p_old = p_current - vel
        self.color = color

    def apply_force(self, sum_of_forces: Vector2):
        self.a = sum_of_forces/self.mass
            
    def update_position(self, dt):
        self.vel = self.p_current - self.p_old
        tmp = self.p_current
        self.p_current = self.p_current + self.vel + self.a * (dt ** 2)
        self.p_old = tmp

class Solver:
    def __init__(self):
        self.objects: List[VerletObject] = []

    def add_object(self, object):
        self.objects.append(object)

    def check_collisions(self):
        n = len(self.objects)
        for i in range(n):
            for j in range(i+1, n):
                min_dist = self.objects[i].radius + self.objects[j].radius
                diff_v = Vector2(self.objects[i].p_current - self.objects[j].p_current)
                dist = diff_v.length()
                if dist < min_dist:
                    self.objects[i].p_current -= 0.5 * diff_v.normalize() * (dist - min_dist)
                    self.objects[j].p_current += 0.5 * diff_v.normalize() * (dist - min_dist)

    def apply_constraints(self):
        for object in self.objects:
            if object.p_current.distance_to(container["position"]) > container["radius"] - object.radius:
                delta = Vector2((object.p_current - container["position"])[0], (object.p_current - container["position"])[1])
                delta.scale_to_length(container["radius"] - object.radius)
                object.p_current = delta + container["position"]

    def update(self, dt):
        for i in range (8):
            for object in self.objects:
                object.apply_force(GRAVITY)
                object.update_position(dt/8)
                self.check_collisions()
                self.apply_constraints()

solver = Solver()
solver.add_object(VerletObject(Vector2(screen.width/2 + 100, 50), Vector2(0, 0), 1, 10, "white"))
solver.add_object(VerletObject(Vector2(screen.width/2 - 150, 150), Vector2(0, 0), 1, 10, "white"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
    
    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
        solver.add_object(VerletObject(Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), Vector2(0, 0), 1, 10, "white"))

    solver.update(dt)

    pygame.draw.circle(screen, "black", container["position"], container["radius"] + 2)
    for object in solver.objects:
        pygame.draw.circle(screen, object.color, object.p_current, object.radius)
    
    pygame.display.flip()
    screen.fill("gray")
    dt = clock.tick(60) / 1000
pygame.quit()