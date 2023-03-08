from sonya_engine import *
from colors import *
import pygame as pg


class Ship (SolidObject):
    def __init__(self, collider):
        super().__init__(collider)
        self.health = 100
        self.is_alive = True

    def take_damage(self, value):
        self.health -= value

    def update(self):
        if self.health <= 0:
            self.is_alive = False
        if self.is_alive:
            super().update()

    def draw(self):
        pg.draw.circle(self.screen, GREY,
                       (self.get_pos().x, self.get_pos().y), self.collider.radius)
        pg.draw.circle(self.screen, WHITE,
                       (self.collider.pos.x, self.collider.pos.y), self.collider.radius, 2)
