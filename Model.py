import pymunk
import pymunk.pygame_util
import Environment
import Animal



class Model:

    def __init__(self, footNumber, weight, w_body, h_body, x_cow=150, y_cow=332.75):
        self.space = pymunk.Space()
        self.environment = Environment.Environment(self.space)
        if footNumber == 4:
            self.animal = Animal.Cow(footNumber, weight, w_body, h_body, x_cow, y_cow)
        else:
            raise Exception("Error : wrong footnumber")
        self.environment.addAnimal(self.animal)
        self.legBodies = self.animal.getLegBodies()
        for i in range(len(self.legBodies)):
            for j in range(len(self.legBodies[0])):
                print("leg " + str(i) + "." + str(j) + " : " + str(self.legBodies[i][j].position.x) + ", " + str(self.legBodies[i][j].position.y))

    def getSpace(self):
        return self.space

    def moves(self):
        """for body in self.legBodies:
            for i in range(len(body)):
                if i % 2 == 0:"""        
        self.legBodies[0][0].apply_force_at_world_point((0, -40), (0, 0))
        self.legBodies[1][0].apply_force_at_world_point((10, -40), (0, 0))
        self.legBodies[0][2].apply_force_at_world_point((0, -305), (0, 0))
        self.legBodies[1][2].apply_force_at_world_point((0, -305), (0, 0))

    