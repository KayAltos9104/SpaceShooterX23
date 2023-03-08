import math
import pygame as pg
from engine_settings import *
from colors import *

delta_time = 0


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_module(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @staticmethod
    def scalar_mul(v, scalar):
        return Vector2(v.x * scalar, v.y * scalar)

    @staticmethod
    def distance(v1, v2):
        sub_vector = v2 - v1
        return sub_vector.get_module()

    def __str__(self):
        return f'Vector2 ({self.x}, {self.y})'

    # Арифметика векторов

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

# Инкапсулировать позицию


class Object:
    def __init__(self):
        self.__pos = Vector2(0, 0)
        self.screen = None
        self.speed = Vector2(0, 0)

    def update(self):
        global delta_time
        pos_new = Vector2.scalar_mul(self.speed, delta_time)
        self.move(self.__pos + pos_new)

    def draw(self):
        pass

    def move(self, v_new):
        self.__pos = v_new

    def get_pos(self):
        return Vector2(self.__pos.x, self.__pos.y)

# Example object class of a circle object


class Circle(Object):
    def __init__(self):
        super().__init__()
        self.a = 0

    def draw(self):
        pg.draw.circle(self.screen, GREEN, (self.pos.x, self.pos.y), 10)
        pg.draw.line(self.screen, GREEN, (400, 300), (self.pos.x, self.pos.y), 1)

    def update(self):
        self.pos = Vector2(400 + 200 * math.cos(math.radians(self.a)),
                            300 + 200 * math.sin(math.radians(self.a)))
        self.a += 0.01


class SolidObject (Object):
    def __init__(self, collider):
        super().__init__()
        self.collider = collider
        # Нет смысла, так как у нас объект всегда в точке появляется (0,0), а потом уже мы сдвигаем
        # self.collider.pos = self.__pos

    def move(self, v_new):
        super().move(v_new)
        self.collider.pos = v_new


class SolidBall (SolidObject):
    def draw(self):
        pg.draw.circle(self.screen, GREEN,
                       (self.get_pos().x, self.get_pos().y), self.collider.radius)
        pg.draw.circle(self.screen, WHITE,
                       (self.collider.pos.x, self.collider.pos.y), self.collider.radius, 2)


class Collider:
    def __init__(self, pos):
        # Геометрический центр коллайдера
        self.pos = pos

    @staticmethod
    def is_intersects(c1, c2):
        return False


class CircleCollider(Collider):
    def __init__(self, pos, radius):
        super().__init__(pos)
        self.radius = radius

    @staticmethod
    def is_intersects(c1, c2):
        return Vector2.distance(c1.pos, c2.pos) < c1.radius + c2.radius


class Engine:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.is_running = True
        self.objects = []
        pg.display.set_caption('Space Shooter X23')

    def run(self):
        global delta_time
        while self.is_running:
            self.read_events()
            for i in self.objects:
                i.update()
            self.draw()
            delta_time = self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(BLACK)
        for i in self.objects:
            i.draw()
        pg.display.flip()

    def read_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def add_object(self, obj):
        self.objects.append(obj)
        obj.screen = self.screen