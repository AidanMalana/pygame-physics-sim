import pygame
from pygame.math import Vector2
from typing import List
import random
import math
from math import sin
from verlet import * 

pygame.init()

pygame.display.set_caption('Verlet Integration Simulation')
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

running = True
dt = 0
clock = pygame.time.Clock()

constraint = Constraint(Vector2(screen.width / 2, screen.height / 2), screen.height / 2 - 10)
solver = Solver(constraint)
solver.add_object(VerletObject(Vector2(screen.width/2 + 100, 50), Vector2(0, 0), 1, 10, "white"))
solver.add_object(VerletObject(Vector2(screen.width/2 - 150, 150), Vector2(0, 0), 2, 20, "white"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
    
    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
        solver.add_object(VerletObject(Vector2(screen.width/2, 50), Vector2(0, 0), 1, random.randint(5, 25), pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    solver.update(dt)

    pygame.draw.circle(screen, "black", constraint.position, constraint.radius + 2)
    for object in solver.objects:
        pygame.draw.circle(screen, object.color, object.p_current, object.radius)
    
    pygame.display.flip()
    screen.fill("gray")
    dt = clock.tick(60) / 1000
    print(1/dt)
pygame.quit()
