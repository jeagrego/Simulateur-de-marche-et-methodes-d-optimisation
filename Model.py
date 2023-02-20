import pymunk
import pymunk.pygame_util
from Environment import Environment
from Animal import *
from Genetic import *
import time


class Model:

    def __init__(self, mutation_prob, footNumber, weight, w_body, h_body, x_animal=150, y_animal=332.75):
        self.space = pymunk.Space()
        self.environment = Environment(self.space)
        self.genetic = Genetic(footNumber)
        self.population = []
        self.footnumber = footNumber
        self.weight = weight
        self.w_body = w_body
        self.h_body = h_body
        self.x_animal = x_animal
        self.y_animal = y_animal
        self.x_previous_body = x_animal
        self.y_previous_body = y_animal
        self.mutation_prob = mutation_prob

        if footNumber == 4:
            self.initPopulation()
    
        elif footNumber == 2:
            print("unavailable")

        else:
            raise Exception("Error : wrong foot numbers")

    def getSpace(self):
        return self.space

    def getPosition(self):
        return (self.x_animal, self.y_animal)

    def setAnimal(self, animal):
        for body in self.space.bodies:
            self.space.remove(body)
        for shape in self.space.shapes:
            self.space.remove(shape)
        for constraint in self.space.constraints:
            self.space.remove(constraint)
        self.environment.setGround()
        self.environment.addAnimal(animal)

    def getPopulation(self):
        return self.population

    def addToPopulation(self, new_population):
        self.population.extend(new_population)
        #print(self.population)
    
    def deleteAnimal(self, animal):
        self.population.remove(animal)

    def getNewPopulation(self):
        new_population = self.genetic.get_new_population(self.population, self.mutation_prob)
        new_population_1 = []
        for i in range(len(new_population)):
            animal = self.makeAnimal()
            animal.setMatrix(new_population[i])
            new_population_1.append(animal)
        return new_population_1

    def isMoving(self, start_time, topBody):
        current_time = time.time()
        diff_time = current_time - start_time 
        diff_x = self.x_previous_body - topBody.position[0]

        if abs(diff_x) < 20 and diff_time > 5:
            return False
        self.x_previous_body = topBody.position[0]
        #print(diff_time, diff_x)
        return True

    def isFalling(self, headBody):
        diff_y = self.y_previous_body - headBody.position[1]
        if  abs(diff_y) > 70:
            return False
        self.y_previous_body = headBody.position[0]
        return True


    def initPopulation(self):
        for i in range(2):
            animal = self.makeAnimal()
            self.population.append(animal)    
        self.genetic.updatePopulation(self.population)

    def makeAnimal(self):
        if self.footnumber == 4:
            animal = Cow(self.footnumber, self.weight, self.w_body, self.h_body, self.x_animal, self.y_animal)
            animal.setMatrix(self.makeMatrix())
        elif self.footnumber == 2:
            animal = Autruche(self.footnumber, self.weight, self.w_body, self.h_body, self.x_animal, self.y_animal)
            animal.setMatrix(self.makeMatrix())
        
        return animal

    def makeMatrix(self):
        matrix = []
        y = self.footnumber*2
        for i in range(y):
            x = [random.randint(0,y-1), random.uniform(-5.0, 5.0)]
            matrix.append(x)
        return matrix

    def moves(self, i, direction, animal):
        matrix = animal.getMatrix()
        self.smjoints = animal.getSmjoints()

        direction_1 = [1, -1 , -1, -1 , -1, -1 , -1, 1] #1
        direction_2 = [-1, -1, 1 ,1 ,1 ,1, -1, -1] #2
        direction_3 = [-1, 1, 1 ,1 ,1 ,1, 1, -1] #-1
        direction_4 = [1, 1 , -1, -1 , -1, -1 , 1, 1] #-2
        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
        
        if direction == 1:
            for i in range(len(matrix)):
                if i not in [1, 6]:
                    self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_1[i]
            
        elif direction == 2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_2[i]

        elif direction == -1:
            for i in range(len(matrix)):
                if i not in [1, 6]:
                    self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_3[i]
            
        elif direction == -2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_4[i]
        
        
    """def temp_moves(self, i, direction):
        self.legBodies[0][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[1][0].apply_impulse_at_world_point((0, 1), (0, 0))
        self.legBodies[0][2].apply_impulse_at_world_point((0, -6), (0, 0))
        self.legBodies[1][2].apply_impulse_at_world_point((0, -6), (0, 0
        weight = self.animal.getWeight()
        x, y = 50, -400
        if j+1 % 2 != 0:
            y = y - 5
        
        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
                
        j1 = abs((i-1)%8)
        j2 = abs((i-2)%8)
        j3 = abs((i-3)%8)
        j4 = abs((i-4)%8)
        rotate = 2
         if j1 < 0:
            j1 = 6
        if j2 < 0:
            j2 = 7
        if j3 < 0:
            j3 = 1
        if j4 < 0:
            j4 = 0
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
        #self.legBodies[i][j+1].apply_impulse_at_world_point((x, y), (0, 25))"""
    