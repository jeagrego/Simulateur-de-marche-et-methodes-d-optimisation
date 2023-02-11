import pymunk
import pygame
import sys
import pymunk.pygame_util
import Environment

width, height = 1200, 700


class Display:

    def __init__(self, model):
        pygame.init()
        self.model = model
        self.space = model.getSpace()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 16)
        self.fps = 60
        self.dt = 1.0 / self.fps

    def show(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            self.model.moves() 
            self.screen.fill(pygame.Color("white"))
            self.space.debug_draw(draw_options)
            # Info and flip screen
            self.screen.blit(self.font.render("fps: " + str(self.clock.get_fps()), True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption("Simulation de marche")
            self.space.step(self.dt)
            self.clock.tick(self.fps)

    

    """def setCow(self, weight, x_cow, y_cow, w_body, h_body):
        legBodies = []  # [[leg1, leg3][leg2, leg4]] leg1 et leg2 sont en arriere, leg3 et leg4 sont en avant
        footBodies = []
        leg_shape = []
        hoofs_shape = []
        joints = []
        rljoints = []  # rotation limit

        w_leg = w_body * 0.15
        h_leg = h_body * 0.55
        w_hoof = w_body * 0.25
        h_hoof = h_body * 0.10

        BackLeg_x = (x_cow - (w_body / 2)) + ((w_body * 0.1) + (w_leg / 2))
        upperLeg_y = (y_cow + (h_body / 2)) + h_leg / 2
        FrontLeg_x = (x_cow + (w_body / 2)) - ((w_body * 0.1) + (w_leg / 2))

        positions_leg = [(BackLeg_x, upperLeg_y), (BackLeg_x, upperLeg_y + h_leg), 
                        (FrontLeg_x, upperLeg_y),(FrontLeg_x, upperLeg_y + h_leg)]
        positions_foot = [(BackLeg_x, upperLeg_y + (h_leg * (3 / 2)) + (h_hoof * 0.5)),
                            (FrontLeg_x, upperLeg_y + (h_leg * (3 / 2)) + (h_hoof * 0.5))]

        leg_weight = weight * 0.05  # 8 leg members
        head_weight = weight*0.1
        foot_weight = weight * 0.025  # 4 hoofs

        #mid part of cow body
        cowbody = pymunk.Body(weight * 0.4, pymunk.moment_for_box(weight * 0.4, (w_body, h_body)))
        cowbody.position = (x_cow, y_cow)
        cowshape = pymunk.Poly.create_box(cowbody, (w_body, h_body))
        cowshape.collision_type = 1
        self.space.add(cowbody, cowshape)
        #top part of head body
        headbody = pymunk.Body(head_weight, pymunk.moment_for_box(head_weight, (w_body*0.3, h_body*0.5)))
        headbody.position = (x_cow+(w_body*0.5), y_cow-(h_body*0.5))
        headshape = pymunk.Poly.create_box(headbody, (w_body*0.3, h_body*0.5))
        headshape.collision_type = 1
        self.space.add(headbody, headshape)

        self.space.add(pymunk.PinJoint(cowbody, headbody, (w_body*0.5, -h_body*0.5), (0, 0)))

        for i in range(2):
            paw = []
            for j in range(4):
                paw.append(pymunk.Body(leg_weight, pymunk.moment_for_box(leg_weight, (w_leg, h_leg))))
            legBodies.append(paw)

        for i in range(2):
            hoof = []
            for j in range(2):
                hoof.append(pymunk.Body(foot_weight, pymunk.moment_for_box(foot_weight, (w_hoof, h_hoof))))
            footBodies.append(hoof)

        for paw in legBodies:
            for i in range(4):
                paw[i].position = positions_leg[i]

        for hoof in footBodies:
            for i in range(2):
                hoof[i].position = positions_foot[i]

        for paw in legBodies:
            shape = []
            for body in paw:
                pawShape = pymunk.Poly.create_box(body, (w_leg, h_leg))
                pawShape.collision_type = 1
                shape.append(pawShape)
            leg_shape.append(shape)

        for hoof in footBodies:
            shape = []
            for body in hoof:
                ballShape = pymunk.Poly.create_box(body, (w_hoof, h_hoof))
                ballShape.collision_type = 1
                shape.append(ballShape)
            hoofs_shape.append(shape)

        cowBodyJoint_x = (w_body * 0.5) - ((w_body * 0.1) + (w_leg * 0.5))
        cowBodyJoint_y = h_body * 0.5
        cowPawJoint_y = h_leg * 0.5
        cowPawJoint_x = w_leg * 0.5
        cowHoofJoint_y = h_hoof / 2
        mini = 0
        mini_hoof = -1
        maxi = 1

        # 0 = foreground legs and 1 = background legs
        # backlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(legBodies[i][0], cowbody, (0, -cowPawJoint_y), (-cowBodyJoint_x, cowBodyJoint_y))
            rljoint1 = pymunk.constraints.RotaryLimitJoint(legBodies[i][0], cowbody, mini, maxi)

            joint2 = pymunk.PinJoint(legBodies[i][0], legBodies[i][1], (0, cowPawJoint_y), (0, -cowPawJoint_y))
            rljoint2 = pymunk.constraints.RotaryLimitJoint(legBodies[i][0], legBodies[i][1], mini, maxi)

            joint3 = pymunk.PinJoint(legBodies[i][1], footBodies[i][0], (-cowPawJoint_x, cowPawJoint_y),(-cowPawJoint_x, -cowHoofJoint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(legBodies[i][1], footBodies[i][0], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(legBodies[i][1], footBodies[i][0], (cowPawJoint_x, cowPawJoint_y),(cowPawJoint_x, -cowHoofJoint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(legBodies[i][1], footBodies[i][0], mini_hoof, maxi)

            joints.extend((joint1, joint2, joint3, joint4))
            rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

        # hindlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(legBodies[i][2], cowbody, (0, -cowPawJoint_y), (cowBodyJoint_x, cowBodyJoint_y))
            rljoint1 = pymunk.constraints.RotaryLimitJoint(legBodies[i][2], cowbody, mini, maxi)

            joint2 = pymunk.PinJoint(legBodies[i][2], legBodies[i][3], (0, cowPawJoint_y), (0, -cowPawJoint_y))
            rljoint2 = pymunk.constraints.RotaryLimitJoint(legBodies[i][2], legBodies[i][3], mini, maxi)

            joint3 = pymunk.PinJoint(legBodies[i][3], footBodies[i][1], (-cowPawJoint_x, cowPawJoint_y),(-cowPawJoint_x, -cowHoofJoint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(legBodies[i][3], footBodies[i][1], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(legBodies[i][3], footBodies[i][1], (cowPawJoint_x, cowPawJoint_y),(cowPawJoint_x, -cowHoofJoint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(legBodies[i][3], footBodies[i][1], mini_hoof, maxi)

            joints.extend((joint1, joint2, joint3, joint4))
            rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

        for i in range(len(legBodies)):
            for j in range(len(legBodies[i])):
                self.space.add(legBodies[i][j], leg_shape[i][j])

        for i in range(len(footBodies)):
            for j in range(len(footBodies[i])):
                self.space.add(footBodies[i][j], hoofs_shape[i][j])

        for i in range(len(joints)):
            self.space.add(joints[i])
            self.space.add(rljoints[i])
"""