import pygame
from pod import Pod


class Player(Pod):
    def __init__(self, window, x, y, rad, color, b_color):
        super().__init__(window, x, y, rad, color, b_color)
        self.health = 100
        self.maxHealth = 100
        self.alive = True

    def takeDamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

    def draw(self):
        for b in self.bullets:
            if b.off_screen(self.win):
                self.bullets.remove(b)
            else:
                b.draw(self.win)

        pygame.draw.circle(self.win, self.color,
                           (int(self.pos.x), int(self.pos.y)), self.rad, 0)

        healthBarThickness = 10
        healthBarBack = pygame.Rect(self.pos.x - self.rad, self.pos.y +
                                    self.rad + 5, self.rad*2, healthBarThickness)
        pygame.draw.rect(self.win, (255, 0, 0), healthBarBack)

        healthBar = pygame.Rect(self.pos.x - self.rad, self.pos.y +
                                self.rad + 5, (self.rad*2)*(self.health/self.maxHealth), healthBarThickness)
        pygame.draw.rect(self.win, (0, 255, 0), healthBar)
