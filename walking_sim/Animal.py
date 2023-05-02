import pymunk
from time import *
from constantes import *
from abc import abstractmethod


class Animal:

    def __init__(self, footNumber, weight, w_body, h_body, x_cow=150, y_cow=430.75):
        self.matrix = None
        self.footNumber = footNumber
        self.weight = weight
        self.score = 0
        self.body = None
        self.shape = None

        self.x_cow = x_cow
        self.y_cow = y_cow
        self.w_body = w_body
        self.h_body = h_body

        self.legBodies = []  # [leg1, leg3, leg2, leg4] leg1 et leg2 sont en arriere, leg3 et leg4 sont en avant
        self.footBodies = []
        self.bodiesAndShapes = []
        self.joints = []
        self.rljoints = []  # rotation limit
        self.smjoints = []
        self.topBody = None
        self.headBody = None

        self.w_leg = w_body * 0.15
        self.h_leg = h_body * 0.55
        self.w_hoof = w_body * 0.25
        self.h_hoof = h_body * 0.10

    def setScore(self, score):
        if score < 0:
            self.score = 0
        else:
            self.score = score

    def getFootNumber(self):
        return self.footNumber

    def getWeight(self):
        return self.weight

    def getScore(self):
        return self.score

    def getLegBodies(self):
        return self.legBodies

    def getSmjoints(self):
        return self.smjoints

    def getMatrix(self):
        return self.matrice

    def setMatrix(self, matrice):
        self.matrice = matrice

    def getPosition(self):
        return self.topBody.position

    def getBodyAndShape(self):
        return self.bodiesAndShapes

    @abstractmethod
    def makeBodyAndShape(self):
        pass

    @abstractmethod
    def makeBodies(self):
        pass

    @abstractmethod
    def makeshapes(self):
        pass

    @abstractmethod
    def makeJoints(self):
        pass

    @abstractmethod
    def getLegsPositions(self):
        pass

    @abstractmethod
    def getFootsPositions(self):
        pass

    """@abstractmethod
    def updatePositions(self):
        pass"""


class Autruche(Animal):
    def makeBodyAndShape(self):
        pass


class Cow(Animal):

    def __init__(self, footNumber, weight, w_body, h_body, x_cow=150, y_cow=430.75):
        super().__init__(footNumber, weight, w_body, h_body, x_cow=150, y_cow=430.75)

        self.leg_weight = weight * 0.05  # 8 leg members
        self.head_weight = weight * 0.025
        self.foot_weight = weight * 0.025  # 4 hoofs
        self.BackLeg_x = (self.x_cow - (self.w_body / 2)) + ((self.w_body * 0.1) + (self.w_leg / 2))
        self.upperLeg_y = (self.y_cow + (self.h_body / 2)) + self.h_leg / 2
        self.FrontLeg_x = (self.x_cow + (self.w_body / 2)) - ((self.w_body * 0.1) + (self.w_leg / 2))
        self.headBody = None
        self.time = 0
        self.derive_time = 0
        self.derive_x = 0
        self.x_previous_body = x_cow
        self.y_previous_body = y_cow
        self.x_cow = x_cow
        self.y_cow = y_cow

    def getHeadBody(self):
        return self.headBody

    def getInitPos(self):
        return self.x_cow, self.y_cow

    def getConstraints(self):
        constraint = []
        constraint.extend(self.joints)
        constraint.extend(self.smjoints)
        constraint.extend(self.rljoints)
        return constraint

    def setTime(self, time):
        self.time = time

    def updateTime(self):
        self.time += time() - self.derive_time
        self.derive_x += self.x_previous_body - self.topBody.position[0]
        self.x_previous_body = self.topBody.position[0]

    def isMoving(self, time):
        """if self.time // 5 == 1:
            self.time = 0
            self.derive_time = time()
            if abs(self.diff_x) < 80:
                self.diff_x = 0
                self.time = 0
                return False"""
        if  time > 10:
            return False
        return True

    def isNotFalling(self, time):
        diff_y = 900 - self.headBody.position[1]
        if time > 2:
            if diff_y < 360:
                return False
            if self.headBody.position[0] < 0 or self.headBody.position[0] > width:
                return False
            if self.topBody.position[1] + self.w_body / 2 > 890:
                return False
        return True

    def getTopBodyAndHeadBody(self):
        return self.topBody, self.headBody

    def makeBodyAndShape(self):
        self.makeBodies()
        self.makeshapes()
        self.makeJoints()
        return self.bodiesAndShapes, self.joints, self.rljoints, self.smjoints

    def makeBodies(self):
        positions_leg = self.getLegsPositions()
        positions_foot = self.getFootsPositions()

        self.headBody = pymunk.Body(self.head_weight,
                                    pymunk.moment_for_box(self.head_weight, (self.w_body, self.h_body)))
        self.headBody.position = (self.x_cow + (self.w_body * 0.5), self.y_cow - (self.h_body * 0.5))
        self.topBody = pymunk.Body(self.weight * 0.4,
                                   pymunk.moment_for_box(self.weight * 0.4, (self.w_body * 0.3, self.h_body * 0.5)))
        self.topBody.position = (self.x_cow, self.y_cow)

        self.BackLeg_x = (self.x_cow - (self.w_body / 2)) + ((self.w_body * 0.1) + (self.w_leg / 2))
        self.upperLeg_y = (self.y_cow + (self.h_body / 2)) + self.h_leg / 2
        self.FrontLeg_x = (self.x_cow + (self.w_body / 2)) - ((self.w_body * 0.1) + (self.w_leg / 2))

        for i in range(2):  # making leg
            leg = []
            for j in range(4):
                leg.append(
                    pymunk.Body(self.leg_weight, pymunk.moment_for_box(self.leg_weight, (self.w_leg, self.h_leg))))
            self.legBodies.append(leg)

        for i in range(2):
            foot = []
            for j in range(2):  # making foot
                foot.append(
                    pymunk.Body(self.foot_weight, pymunk.moment_for_box(self.foot_weight, (self.w_hoof, self.h_hoof))))
            self.footBodies.append(foot)

        for leg in self.legBodies:
            for i in range(4):
                leg[i].position = positions_leg[i]

        for foot in self.footBodies:
            for i in range(2):
                foot[i].position = positions_foot[i]

    def makeshapes(self):
        cow_color = (0, 0, 0, 255)
        body_shape = pymunk.Poly.create_box(self.topBody, (self.w_body, self.h_body))
        body_shape.color = cow_color
        self.bodiesAndShapes.append((self.topBody, body_shape))
        head_shape = pymunk.Poly.create_box(self.headBody, (self.w_body * 0.3, self.h_body * 0.5))
        head_shape.color = cow_color
        self.bodiesAndShapes.append((self.headBody, head_shape))

        for leg in self.legBodies:
            for body in leg:
                leg_shape = pymunk.Poly.create_box(body, (self.w_leg, self.h_leg))
                leg_shape.color = cow_color
                self.bodiesAndShapes.append((body, leg_shape))

        for foot in self.footBodies:
            for body in foot:
                foot_shape = pymunk.Poly.create_box(body, (self.w_hoof, self.h_hoof))
                foot_shape.color = cow_color
                foot_shape.friction = 0.5
                self.bodiesAndShapes.append((body, foot_shape))

    def makeJoints(self):
        cow_body_joint_x = (self.w_body / 2) - ((self.w_body * 0.1) + (self.w_leg / 2))
        cow_body_joint_y = self.h_body / 2
        cow_paw_joint_y = self.h_leg / 2
        cow_paw_joint_x = self.w_leg / 2
        cow_hoof_joint_y = self.h_hoof / 2
        mini = 0
        mini_top_body = -1
        mini_hoof = -1
        maxi = 1
        top_and_head = pymunk.PinJoint(self.topBody, self.headBody, (self.w_body * 0.5, - self.h_body * 0.5), (0, 0))
        self.joints.append(top_and_head)

        # 0 = foreground legs and 1 = background legs
        # backlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(self.legBodies[i][0], self.topBody, (0, -cow_paw_joint_y),
                                     (-cow_body_joint_x, cow_body_joint_y))
            smjoint1 = pymunk.constraints.SimpleMotor(self.legBodies[i][0], self.topBody, 0)
            smjoint1.max_force = 10000000
            rljoint1 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][0], self.topBody, mini_top_body, maxi)

            joint2 = pymunk.PinJoint(self.legBodies[i][0], self.legBodies[i][1], (0, cow_paw_joint_y),
                                     (0, -cow_paw_joint_y))
            smjoint2 = pymunk.constraints.SimpleMotor(self.legBodies[i][0], self.legBodies[i][1], 0)
            smjoint2.max_force = 10000000
            rljoint2 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][0], self.legBodies[i][1], mini, maxi)

            # changer les rotarylimitjoin pour les pieds
            joint3 = pymunk.PinJoint(self.legBodies[i][1], self.footBodies[i][0], (-cow_paw_joint_x, cow_paw_joint_y),
                                     (-cow_paw_joint_x, -cow_hoof_joint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][1], self.footBodies[i][0], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(self.legBodies[i][1], self.footBodies[i][0], (cow_paw_joint_x, cow_paw_joint_y),
                                     (cow_paw_joint_x, -cow_hoof_joint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][1], self.footBodies[i][0], mini_hoof, maxi)

            self.joints.extend((joint1, joint2, joint3, joint4))
            self.smjoints.extend((smjoint1, smjoint2))
            self.rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

        # hindlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(self.legBodies[i][2], self.topBody, (0, -cow_paw_joint_y),
                                     (cow_body_joint_x, cow_body_joint_y))
            smjoint1 = pymunk.constraints.SimpleMotor(self.legBodies[i][2], self.topBody, 0)
            smjoint1.max_force = 10000000
            rljoint1 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][2], self.topBody, mini_top_body, maxi)

            joint2 = pymunk.PinJoint(self.legBodies[i][2], self.legBodies[i][3], (0, cow_paw_joint_y),
                                     (0, -cow_paw_joint_y))
            smjoint2 = pymunk.constraints.SimpleMotor(self.legBodies[i][2], self.legBodies[i][3], 0)
            smjoint2.max_force = 10000000
            rljoint2 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][2], self.legBodies[i][3], mini, maxi)

            joint3 = pymunk.PinJoint(self.legBodies[i][3], self.footBodies[i][1], (-cow_paw_joint_x, cow_paw_joint_y),
                                     (-cow_paw_joint_x, -cow_hoof_joint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][3], self.footBodies[i][1], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(self.legBodies[i][3], self.footBodies[i][1], (cow_paw_joint_x, cow_paw_joint_y),
                                     (cow_paw_joint_x, -cow_hoof_joint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][3], self.footBodies[i][1], mini_hoof, maxi)

            self.joints.extend((joint1, joint2, joint3, joint4))
            self.smjoints.extend((smjoint1, smjoint2))
            self.rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

    def getLegsPositions(self):
        return [(self.BackLeg_x, self.upperLeg_y), (self.BackLeg_x, self.upperLeg_y + self.h_leg),
                (self.FrontLeg_x, self.upperLeg_y), (self.FrontLeg_x, self.upperLeg_y + self.h_leg)]

    def getFootsPositions(self):
        return [(self.BackLeg_x, self.upperLeg_y + (self.h_leg * (3 / 2)) + (self.h_hoof * 0.5)),
                (self.FrontLeg_x, self.upperLeg_y + (self.h_leg * (3 / 2)) + (self.h_hoof * 0.5))]
