import pygame as pg
import enum


class Controls(enum.Enum):
    go_up = 1
    go_down = 2
    go_right = 3
    go_left = 4
    shoot = 5

# Keys


KEYBOARD = {
    Controls.go_up.value: pg.K_w,
    Controls.go_down.value: pg.K_s,
    Controls.go_right.value: pg.K_d,
    Controls.go_left.value: pg.K_a,
    Controls.shoot.value: pg.K_SPACE,
}
