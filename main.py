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

GRAVITY = Vector2(0, 10)

container = {"position": Vector2(screen.width / 2, screen.height / 2), "radius": 360}

class Ball:
    def __init__(self, p_current: Vector2, vel: Vector2, mass, radius):
        self.p_current = p_current
        self.accel = Vector2()
        self.accel.xy = 0, 0
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.p_old = p_current - vel

    def apply_force(self, sum_of_forces: Vector2):
        self.a = sum_of_forces/self.mass

    def update_position(self, dt):
        tmp = self.p_current
        self.p_current = self.p_current * 2 - self.p_old + self.a * (dt ** 2)
        self.p_old = tmp
        if ball.p_current.distance_to(container["position"]) > container["radius"]:
            delta = Vector2((ball.p_current - container["position"])[0], (ball.p_current - container["position"])[1])
            delta.scale_to_length(container["radius"])
            ball.p_current = delta + container["position"]
            ball.p_old = ball.p_current + ball.vel
        self.vel = self.p_current - self.p_old

balls: List[Ball] = []
balls.append(Ball(Vector2(screen.width/2, 20), Vector2(0, 0), 1, 10))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    for ball in balls:
        ball.apply_force(GRAVITY)
        ball.update_position(dt)

    screen.fill("black")

    pygame.draw.circle(screen, "white", container["position"], container["radius"], 2)
    for ball in balls:
        pygame.draw.circle(screen, "white", ball.p_current, ball.radius)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()