
import pymunk
import pymunk.pygame_util


class Environment:

    def __init__(self, space):
        self.space = space
        self.space.gravity = 0, 981
        self.handlerWithGround = self.space.add_collision_handler(1, 2)
        self.handlerWithBodies = self.space.add_collision_handler(1, 1)
        self.handlerWithBodies.begin = self.noCollision
        self.handlerWithGround.begin = self.collision
        self.setGround()

    def setGround(self):
        ground = pymunk.Segment(self.space.static_body, (-600, 600), (2400, 600), 100)
        ground.friction = 1.0
        # ground.group = 2
        ground.collision_type = 2
        self.space.add(ground)

    def noCollision(self, arbiter, space, data):
        return False

    def collision(self, arbiter, space, data):
        return True

    def addAnimal(self, animal):
        bodiesAndShapes, joints, rljoints = animal.makeBodyAndShape()

        for body, shape in bodiesAndShapes:
            shape.collision_type = 1
            self.space.add(body, shape)

        for i in range(len(joints)):
            self.space.add(joints[i])
        for i in range(len(rljoints)):
            self.space.add(rljoints[i])