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
            for j in range(0,len(self.legBodies[0]),2):
                print("leg ")
                print(str(i) + "." + str(j) + " : " + str(self.legBodies[i][j].position.x) + ", " + str(self.legBodies[i][j].position.y))
                print(str(i) + "." + str(j+1) + " : " + str(self.legBodies[i][j+1].position.x) + ", " + str(self.legBodies[i][j+1].position.y))

    def getSpace(self):
        return self.space

    def moves(self, i, j):
   
        """self.legBodies[0][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[1][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[0][2].apply_impulse_at_world_point((0, -6), (0, 0))
        self.legBodies[1][2].apply_impulse_at_world_point((0, -6), (0, 0))"""
        weight = self.animal.getWeight()
        x, y = 50, -400
        if j+1 % 2 != 0:
            y = y - 5
        
        self.legBodies[i][j].apply_impulse_at_world_point((x, y), (0, 25))
        #self.legBodies[i][j+1].apply_impulse_at_world_point((x, y), (0, 25))
        


    