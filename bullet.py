import pygame


class Bullet:
    def __init__(self, x, y, vel, rad, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = vel
        self.rad = rad
        self.color = color

    def off_screen(self, window):
        return self.pos.x < 0 - self.rad or self.pos.x > window.get_width() + self.rad or self.pos.y < 0 - self.rad or self.pos.y > window.get_height() + self.rad

    def update(self):
        self.pos += self.vel

    def draw(self, window):
        pygame.draw.circle(window, self.color,
                           (int(self.pos.x), int(self.pos.y)), self.rad, 0)
