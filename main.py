import sys, pygame
from pygame.math import Vector2
from typing import List

pygame.init()

pygame.display.set_caption('Verlet Integration Simulation')
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)

running = True
clock = pygame.time.Clock()

GRAVITY = 9.8

class Ball:
    def __init__(self, p_current: Vector2, vel: Vector2, mass, radius):
        self.p_current = p_current
        self.accel = Vector2()
        self.accel.xy = 0, 0
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.p_old = p_current - vel

    def applyForce(self, sum_of_forces: Vector2):
        self.a = sum_of_forces/self.mass

    def updatePosition(self):
        self.p_current += (0, 10)
        # update velocity

balls: List[Ball] = []
balls.append(Ball(Vector2(screen.width/2, 0), Vector2(0, 0), 1, 10))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    for ball in balls:
        ball.updatePosition()

    screen.fill("black")

    # pygame.draw.circle(screen, "white", (balls[0][0], balls[0][1]), 10)
    for ball in balls:
        pygame.draw.circle(screen, "white", ball.p_current, ball.radius)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()