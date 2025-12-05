from pygame.math import Vector2

class Constraint:
    def __init__(self, position: Vector2, radius: int):
        self.position: Vector2 = position
        self.radius: int = radius

class VerletObject:
    def __init__(self, p_current: Vector2, vel: Vector2, mass, radius, color):
        self.p_current: Vector2 = p_current
        self.accel: Vector2 = Vector2()
        self.accel.xy = 0, 0
        self.vel: Vector2 = vel
        # The engine allows you to make your own mass, but right now it overrides it to make sense
        self.mass: int = (radius ** 2) / 100
        self.radius: int = radius
        self.p_old: Vector2 = p_current - vel
        self.color: pygame.Color = color
        self.constraints: List[Constraint] = []

    def apply_force(self, sum_of_forces: Vector2):
        self.accel = sum_of_forces
          
    def update_position(self, dt):
        self.vel = self.p_current - self.p_old
        tmp = self.p_current
        self.p_current = self.p_current + self.vel + self.accel * (dt ** 2)
        self.p_old = tmp

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def apply_constraints(self):
        for c in self.constraints:
            if self.p_current.distance_to(c.position) > c.radius - self.radius:
                delta = Vector2((self.p_current - c.position)[0], (self.p_current - c.position)[1])
                delta.scale_to_length(c.radius - self.radius)
                self.p_current = delta + c.position

class Solver:
    GRAVITY = Vector2(0, 600)

    def __init__(self, bounds: Constraint):
        self.objects: List[VerletObject] = []
        self.bounds = bounds

    def add_object(self, object):
        object.add_constraint(self.bounds)
        self.objects.append(object)

    def check_collisions(self):
        n = len(self.objects)
        for i in range(n):
            for j in range(i+1, n):
                min_dist = self.objects[i].radius + self.objects[j].radius
                diff_v = Vector2(self.objects[i].p_current - self.objects[j].p_current)
                dist = diff_v.length()
                if dist < min_dist:
                    mass_ratio_i = self.objects[i].mass / (self.objects[i].mass + self.objects[j].mass)
                    mass_ratio_j = self.objects[j].mass / (self.objects[i].mass + self.objects[j].mass)
                    self.objects[i].p_current -= 0.5 * diff_v.normalize() * (dist - min_dist) * mass_ratio_j
                    self.objects[j].p_current += 0.5 * diff_v.normalize() * (dist - min_dist) * mass_ratio_i

    def apply_constraints(self):
        for object in self.objects:
            object.apply_constraints()

    def update(self, dt):
        for i in range (8):
            for object in self.objects:
                object.apply_force(self.GRAVITY)
                object.update_position(dt/8)
                self.check_collisions()
                self.apply_constraints()
