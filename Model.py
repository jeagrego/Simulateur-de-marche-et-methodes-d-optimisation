import pymunk
import pymunk.pygame_util
import Environment
import Animal
from Genetic import *


class Model:

    def __init__(self, footNumber, weight, w_body, h_body, x_cow=150, y_cow=332.75):
        self.space = pymunk.Space()
        self.environment = Environment.Environment(self.space)
        self.population = []
        self.footnumber = footNumber
        self.weight = weight
        self.w_body = w_body
        self.h_body = h_body
        self.x_cow = x_cow
        self.y_cow = y_cow
        if footNumber == 4:
            self.animal = Animal.Cow(footNumber, weight, w_body, h_body, x_cow, y_cow)
        else:
            raise Exception("Error : wrong footnumber")
        self.environment.addAnimal(self.animal)
        self.smjoints = self.animal.getSmjoints()
        self.legBodies = self.animal.getLegBodies()
        for i in range(len(self.legBodies)):
            for j in range(0,len(self.legBodies[0]),2):
                print("leg ")
                print(str(i) + "." + str(j) + " : " + str(self.legBodies[i][j].position.x) + ", " + str(self.legBodies[i][j].position.y))
                print(str(i) + "." + str(j+1) + " : " + str(self.legBodies[i][j+1].position.x) + ", " + str(self.legBodies[i][j+1].position.y))

    def getSpace(self):
        return self.space

    def addToPopulation(self, animal):
        self.population.append(animal)
    
    def deleteAnimal(self, animal):
        self.population.remove(animal)

    def initPopulation(self):
        animal_1 = Animal.Animal(self.footnumber, self.weight, self.w_body, self.h_body, self.x_cow, self.y_cow)
        animal_1.setMatrix(self.makeMatrix())
        
        animal_2 = Animal.Animal(self.footnumber, self.weight, self.w_body, self.h_body, self.x_cow, self.y_cow)
        animal_2.setMatrix(self.makeMatrix())

        self.population.extend((animal_1, animal_2))

    def makeMatrix(self):
        matrix = []
        y = self.footnumber*2
        for i in range(y):
            x = [random.randint(0,y-1), random.uniform(-5.0, 5.0)]
            matrix.append(x)
        return matrix

    def getPopulation(self):
        return self.population

    def moves(self, i, direction):
   
        """self.legBodies[0][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[1][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[0][2].apply_impulse_at_world_point((0, -6), (0, 0))
        self.legBodies[1][2].apply_impulse_at_world_point((0, -6), (0, 0))"""
        """weight = self.animal.getWeight()
        x, y = 50, -400
        if j+1 % 2 != 0:
            y = y - 5"""
        
        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
                
        j1 = abs((i-1)%8)
        j2 = abs((i-2)%8)
        j3 = abs((i-3)%8)
        j4 = abs((i-4)%8)
        rotate = 5
        """ if j1 < 0:
            j1 = 6
        if j2 < 0:
            j2 = 7
        if j3 < 0:
            j3 = 1
        if j4 < 0:
            j4 = 0"""
        if direction == 1:
            self.smjoints[i].rate = rotate
            #self.smjoints[i+1].rate = -rotate
            self.smjoints[i+2].rate = -rotate
            self.smjoints[i+3].rate = -rotate
            self.smjoints[j1].rate = -rotate
            self.smjoints[j2].rate = -rotate
            #self.smjoints[j3].rate = -rotate
            self.smjoints[j4].rate = rotate
        elif direction == 2:
            self.smjoints[i].rate = -rotate
            self.smjoints[i+1].rate = -rotate
            self.smjoints[i+2].rate = rotate
            self.smjoints[i+3].rate = rotate
            self.smjoints[j1].rate = rotate
            self.smjoints[j2].rate = rotate
            self.smjoints[j3].rate = -rotate
            self.smjoints[j4].rate = -rotate
        elif direction == -1:
            self.smjoints[i].rate = -rotate
            #self.smjoints[i+1].rate = rotate
            self.smjoints[i+2].rate = rotate
            self.smjoints[i+3].rate = rotate
            self.smjoints[j1].rate = rotate
            self.smjoints[j2].rate = rotate
            #self.smjoints[j3].rate = rotate
            self.smjoints[j4].rate = -rotate

        elif direction == -2:
            self.smjoints[i].rate = rotate
            self.smjoints[i+1].rate = rotate
            self.smjoints[i+2].rate = -rotate
            self.smjoints[i+3].rate = -rotate
            self.smjoints[j1].rate = -rotate
            self.smjoints[j2].rate = -rotate
            self.smjoints[j3].rate = rotate
            self.smjoints[j4].rate = rotate
        
        print([i, i+1, i+2, i+3, j4, j3, j2, j1], direction)
        #self.legBodies[i][j+1].apply_impulse_at_world_point((x, y), (0, 25))
        
    def temp_moves(self, i, direction):
        """self.legBodies[0][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[1][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[0][2].apply_impulse_at_world_point((0, -6), (0, 0))
        self.legBodies[1][2].apply_impulse_at_world_point((0, -6), (0, 0))"""
        """weight = self.animal.getWeight()
        x, y = 50, -400
        if j+1 % 2 != 0:
            y = y - 5"""
        
        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
                
        j1 = abs((i-1)%8)
        j2 = abs((i-2)%8)
        j3 = abs((i-3)%8)
        j4 = abs((i-4)%8)
        rotate = 2
        """ if j1 < 0:
            j1 = 6
        if j2 < 0:
            j2 = 7
        if j3 < 0:
            j3 = 1
        if j4 < 0:
            j4 = 0"""
        if direction == 1:
            self.smjoints[i].rate = rotate
            #self.smjoints[i+1].rate = -rotate
            self.smjoints[i+2].rate = -rotate
            self.smjoints[i+3].rate = -rotate
            self.smjoints[j1].rate = -rotate
            self.smjoints[j2].rate = -rotate
            #self.smjoints[j3].rate = -rotate
            self.smjoints[j4].rate = rotate
        elif direction == 2:
            self.smjoints[i].rate = -rotate
            self.smjoints[i+1].rate = -rotate
            self.smjoints[i+2].rate = rotate
            self.smjoints[i+3].rate = rotate
            self.smjoints[j1].rate = rotate
            self.smjoints[j2].rate = rotate
            self.smjoints[j3].rate = -rotate
            self.smjoints[j4].rate = -rotate
        elif direction == -1:
            self.smjoints[i].rate = -rotate
            #self.smjoints[i+1].rate = rotate
            self.smjoints[i+2].rate = rotate
            self.smjoints[i+3].rate = rotate
            self.smjoints[j1].rate = rotate
            self.smjoints[j2].rate = rotate
            #self.smjoints[j3].rate = rotate
            self.smjoints[j4].rate = -rotate

        elif direction == -2:
            self.smjoints[i].rate = rotate
            self.smjoints[i+1].rate = rotate
            self.smjoints[i+2].rate = -rotate
            self.smjoints[i+3].rate = -rotate
            self.smjoints[j1].rate = -rotate
            self.smjoints[j2].rate = -rotate
            self.smjoints[j3].rate = rotate
            self.smjoints[j4].rate = rotate
        
        print([i, i+1, i+2, i+3, j4, j3, j2, j1], direction)
        #self.legBodies[i][j+1].apply_impulse_at_world_point((x, y), (0, 25))
    