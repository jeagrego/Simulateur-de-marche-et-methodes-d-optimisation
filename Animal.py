import pymunk
from abc import abstractmethod

class Animal:
    
    def __init__(self, footNumber, weight, w_body, h_body, x_cow=150, y_cow=332.75):
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

        self.w_leg = w_body * 0.15
        self.h_leg = h_body * 0.55
        self.w_hoof = w_body * 0.25
        self.h_hoof = h_body * 0.10



    def setScore(self, score):
        self.score = score
    
    def getFootNumber(self):
        return self.footNumber
    
    def getPoids(self):
        return self.weight

    def getScore(self):
        return self.score

    def getLegBodies(self):
        return self.legBodies
        
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


class Autruche(Animal):
    def makeBodyAndShape(self):
        pass
 
class Cow(Animal):

    def __init__(self, footNumber, weight, x_cow, y_cow, w_body, h_body):
        super().__init__(footNumber, weight, x_cow, y_cow, w_body, h_body)

        self.leg_weight = weight * 0.05  # 8 leg members
        self.head_weight = weight*0.1
        self.foot_weight = weight * 0.025  # 4 hoofs
        self.BackLeg_x = (self.x_cow - (self.w_body / 2)) + ((self.w_body * 0.1) + (self.w_leg / 2))
        self.upperLeg_y = (self.y_cow + (self.h_body / 2)) + self.h_leg / 2
        self.FrontLeg_x = (self.x_cow + (self.w_body / 2)) - ((self.w_body * 0.1) + (self.w_leg / 2))
        self.headBody = None
        self.topBody = None

    def makeBodyAndShape(self):
        self.__makeBodies()
        self.__makeshapes()
        self.__makeJoints()
        return self.bodiesAndShapes, self.joints, self.rljoints

    
    def __makeBodies(self):
        positions_leg = self.__getLegsPositions()
        positions_foot = self.__getFootsPositions()

        self.headBody = pymunk.Body(self.weight * 0.4, pymunk.moment_for_box(self.weight * 0.4, (self.w_body, self.h_body)))
        self.headBody.position = (self.x_cow+(self.w_body*0.5), self.y_cow-(self.h_body*0.5))
        self.topBody = pymunk.Body(self.head_weight, pymunk.moment_for_box(self.head_weight, (self.w_body*0.3, self.h_body*0.5)))
        self.topBody.position = (self.x_cow, self.y_cow)

        for i in range(2): #making leg
            leg = []
            for j in range(4):
                leg.append(pymunk.Body(self.leg_weight, pymunk.moment_for_box(self.leg_weight, (self.w_leg, self.h_leg))))
            self.legBodies.append(leg)

        for i in range(2):
            foot = []
            for j in range(2): #making foot
                foot.append(pymunk.Body(self.foot_weight, pymunk.moment_for_box(self.foot_weight, (self.w_hoof, self.h_hoof))))
            self.footBodies.append(foot)

        for leg in self.legBodies:
            for i in range(4):
                leg[i].position = positions_leg[i]

        for foot in self.footBodies:
            for i in range(2):
                foot[i].position = positions_foot[i]

   
    def __makeshapes(self):
        
        self.bodiesAndShapes.append((self.topBody, pymunk.Poly.create_box(self.topBody, (self.w_body, self.h_body))))
        self.bodiesAndShapes.append((self.headBody, pymunk.Poly.create_box(self.headBody, (self.w_body*0.3, self.h_body*0.5))))

        for leg in self.legBodies:
            for body in leg:
                legShape = pymunk.Poly.create_box(body, (self.w_leg, self.h_leg))
                self.bodiesAndShapes.append((body, legShape))

        for foot in self.footBodies:
            for body in foot:
                footShape = pymunk.Poly.create_box(body, (self.w_hoof, self.h_hoof))
                self.bodiesAndShapes.append((body, footShape))
    
    def __makeJoints(self):
        cowBodyJoint_x = (self.w_body * 0.5) - ((self.w_body * 0.1) + (self.w_leg * 0.5))
        cowBodyJoint_y = self.h_body * 0.5
        cowPawJoint_y = self.h_leg * 0.5
        cowPawJoint_x = self.w_leg * 0.5
        cowHoofJoint_y = self.h_hoof / 2
        mini = 0
        mini_hoof = -1
        maxi = 1
        topAndHead = pymunk.PinJoint(self.topBody, self.headBody, (self.w_body*0.5, - self.h_body*0.5), (0, 0))
        self.joints.append(topAndHead)

        # 0 = foreground legs and 1 = background legs
        # backlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(self.legBodies[i][0], self.topBody, (0, -cowPawJoint_y), (-cowBodyJoint_x, cowBodyJoint_y))
            rljoint1 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][0], self.topBody, mini, maxi)

            joint2 = pymunk.PinJoint(self.legBodies[i][0], self.legBodies[i][1], (0, cowPawJoint_y), (0, -cowPawJoint_y))
            rljoint2 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][0], self.legBodies[i][1], mini, maxi)

            joint3 = pymunk.PinJoint(self.legBodies[i][1], self.footBodies[i][0], (-cowPawJoint_x, cowPawJoint_y),(-cowPawJoint_x, -cowHoofJoint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][1], self.footBodies[i][0], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(self.legBodies[i][1], self.footBodies[i][0], (cowPawJoint_x, cowPawJoint_y),(cowPawJoint_x, -cowHoofJoint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][1], self.footBodies[i][0], mini_hoof, maxi)

            self.joints.extend((joint1, joint2, joint3, joint4))
            self.rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

        # hindlegs
        for i in range(2):
            joint1 = pymunk.PinJoint(self.legBodies[i][2], self.topBody, (0, -cowPawJoint_y), (cowBodyJoint_x, cowBodyJoint_y))
            rljoint1 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][2], self.topBody, mini, maxi)

            joint2 = pymunk.PinJoint(self.legBodies[i][2], self.legBodies[i][3], (0, cowPawJoint_y), (0, -cowPawJoint_y))
            rljoint2 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][2], self.legBodies[i][3], mini, maxi)

            joint3 = pymunk.PinJoint(self.legBodies[i][3], self.footBodies[i][1], (-cowPawJoint_x, cowPawJoint_y),(-cowPawJoint_x, -cowHoofJoint_y))
            rljoint3 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][3], self.footBodies[i][1], mini_hoof, maxi)

            joint4 = pymunk.PinJoint(self.legBodies[i][3], self.footBodies[i][1], (cowPawJoint_x, cowPawJoint_y),(cowPawJoint_x, -cowHoofJoint_y))
            rljoint4 = pymunk.constraints.RotaryLimitJoint(self.legBodies[i][3], self.footBodies[i][1], mini_hoof, maxi)

            self.joints.extend((joint1, joint2, joint3, joint4))
            self.rljoints.extend((rljoint1, rljoint2, rljoint3, rljoint4))

    
    def __getLegsPositions(self):
        return [(self.BackLeg_x, self.upperLeg_y), (self.BackLeg_x, self.upperLeg_y + self.h_leg), 
                (self.FrontLeg_x, self.upperLeg_y),(self.FrontLeg_x, self.upperLeg_y + self.h_leg)]
    
    def __getFootsPositions(self):
        return [(self.BackLeg_x, self.upperLeg_y + (self.h_leg * (3 / 2)) + (self.h_hoof * 0.5)),
                (self.FrontLeg_x, self.upperLeg_y + (self.h_leg * (3 / 2)) + (self.h_hoof * 0.5))]