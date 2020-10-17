import pygame
import math
from bullet import Bullet
import random


class Pod:
    def __init__(self, window, x, y, rad, color, b_color):
        self.win = window
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acl = pygame.Vector2(0, 0)
        self.rad = rad
        self.color = color
        self.b_color = b_color
        self.drag = 0.85

        self.bullet_speed = 5
        self.bullets = []

    def add_acl(self, force):
        self.acl += force

    def update(self):
        for b in self.bullets:
            b.update()

        self.vel += self.acl
        self.pos += self.vel

        if self.pos.x < self.rad:
            self.pos.x = self.rad
        if self.pos.x > self.win.get_width()-self.rad:
            self.pos.x = self.win.get_width()-self.rad
        if self.pos.y < self.rad:
            self.pos.y = self.rad
        if self.pos.y > self.win.get_height()-self.rad:
            self.pos.y = self.win.get_height()-self.rad

        self.vel *= self.drag
        self.acl *= self.drag

    def draw(self):
        for b in self.bullets:
            if b.off_screen(self.win):
                self.bullets.remove(b)
            else:
                b.draw(self.win)

        pygame.draw.circle(self.win, self.color,
                           (int(self.pos.x), int(self.pos.y)), self.rad, 0)

    def shoot(self, where):
        # a = where[0] - self.pos.x
        # o = where[1] - self.pos.y
        # h = math.sqrt((a**2)+(o**2))
        # ang = math.acos(a / h)
        # print(f"a:{a},  o:{o},  h:{h},  ang:{ang}")

        x = (where[0]-self.pos.x)
        y = (where[1]-self.pos.y)
        vel = pygame.Vector2(x, y)
        vel = vel.normalize() * self.bullet_speed

        self.bullets.append(
            Bullet(self.pos.x, self.pos.y, vel, 5, self.b_color))

    def bullet_count(self):
        return len(self.bullets)
