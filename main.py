from sonya_engine import *

if __name__ == '__main__':
    game = Engine()
    #c = Circle()
    #c.pos += Vector2 (300, 200)

    c1 = SolidBall(CircleCollider(Vector2(0, 0), 20))
    c1.move(Vector2(400, 300))
    c1.speed = Vector2(0.1, 0.0)
    game.add_solid_object(c1)

    c2 = SolidBall(CircleCollider(Vector2(0, 0), 20))
    c2.move(Vector2(600, 300))
    c2.speed = Vector2(-0.1, -0.0)
    game.add_solid_object(c2)
    game.run()



