import math
import pygame as pg
import game_settings as gs

from engine_settings import *
from colors import *

delta_time = 0


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_module(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def reverse(self):
        self.x = -self.x
        self.y = -self.y

    @staticmethod
    def get_reversed(self):
        return Vector2(-self.x, -self.y)

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

    # Сравнение векторов
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __lt__(self, other):
        return self.get_module() < other.get_module()

    def __le__(self, other):
        return self.get_module() < other.get_module() or self == other

    def __gt__(self, other):
        return self.get_module() > other.get_module()

    def __ge__(self, other):
        return self.get_module() > other.get_module() or self == other


class Object:
    def __init__(self):
        self.__pos = Vector2(0, 0)
        self.prev_pos = Vector2(0, 0)
        self.screen = None
        self.speed = Vector2(0, 0)

    def update(self):
        global delta_time
        pos_new = Vector2.scalar_mul(self.speed, delta_time)
        self.prev_pos = self.__pos
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
        self.__id = 1
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.is_running = True
        self.objects = {}
        self.solid_objects = {}
        self.player_id = None
        pg.display.set_caption('Space Shooter X23')

    def run(self):
        global delta_time
        while self.is_running:
            self.read_events()
            pressed_keys = pg.key.get_pressed()

            if pressed_keys[gs.KEYBOARD[gs.Controls.go_up.value]]:
                self.objects[self.player_id].speed += Vector2(0, -0.1)
            if pressed_keys[gs.KEYBOARD[gs.Controls.go_down.value]]:
                self.objects[self.player_id].speed += Vector2(0, 0.1)
            if pressed_keys[gs.KEYBOARD[gs.Controls.go_right.value]]:
                self.objects[self.player_id].speed += Vector2(0.1, 0)
            if pressed_keys[gs.KEYBOARD[gs.Controls.go_left.value]]:
                self.objects[self.player_id].speed += Vector2(-0.1, 0)
            if pressed_keys[gs.KEYBOARD[gs.Controls.shoot.value]]:
                print('Пиф-паф!')


            for i in self.objects.values():
                i.update()

            Engine.process_bouncing(self.solid_objects.values())

            self.draw()
            delta_time = self.clock.tick(FPS)

            self.objects[self.player_id].speed = Vector2(0, 0)

    def draw(self):
        self.screen.fill(BLACK)
        for i in self.objects.values():
            i.draw()
        pg.display.flip()

    def read_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def add_object(self, obj):
        self.objects[self.__id] = obj
        obj.screen = self.screen
        self.__id += 1

    def add_solid_object(self, obj):
        self.add_object(obj)
        self.solid_objects[self.__id-1] = obj

    def add_player(self, obj):
        self.add_solid_object(obj)
        self.player_id = self.__id-1

    @staticmethod
    def process_bouncing(objects_list):
        for i in objects_list:
            for j in objects_list:
                if i == j:
                    continue
                else:
                    if Engine.process_collisions(i, j):
                        i.speed.reverse()
                        j.speed.reverse()

    @staticmethod
    def process_collisions(o1, o2):
        if CircleCollider.is_intersects(o1.collider, o2.collider):
            o1.move(o1.prev_pos)
            o2.move(o2.prev_pos)
            return True
        else:
            return False

